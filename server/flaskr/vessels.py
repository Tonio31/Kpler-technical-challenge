import functools

import datetime

from flask import (
    Blueprint, current_app, request, jsonify, abort
)


from flaskr.db import get_db
from dateutil import parser

bp = Blueprint('vessels', __name__, url_prefix='/vessels')


def is_iso_date(date_string):
    try:
        parser.parse(date_string)
        return True
    except ValueError:
        return False


def format_db_row_to_position(row):
    return {
        "id": row['id'],
        "vesselId": row['vessel_id'],
        "createdAt": row['received_time_utc'].isoformat() + 'Z',  # Adding 'Z' to denote UTC time
        "latitude": row['latitude'],
        "longitude": row['longitude']
    }


def format_position_to_ready_to_insert_db_row(payload):
    vessel_id = payload['vesselId']
    if not vessel_id:
        abort(400, description="vesselId is required")

    created_at = payload['createdAt']
    if not is_iso_date(created_at):
        abort(400, description=f"wrong format for createdAt: {created_at}")

    latitude = payload['latitude']
    if not latitude:
        abort(400, description="latitude is required")

    longitude = payload['longitude']
    if not longitude:
        abort(400, description="longitude is required")

    created_at_parsed = parser.parse(created_at)
    created_at_utc = created_at_parsed.astimezone(datetime.timezone.utc)
    created_at_utc_formatted_for_sql = created_at_utc.strftime('%Y-%m-%d %H:%M:%S')

    return {
        "vessel_id": payload['vesselId'],
        "received_time_utc": created_at_utc_formatted_for_sql,
        "latitude": latitude,
        "longitude": longitude
    }


def retrieve_all_positions():
    db = get_db()

    rows = db.execute(
        'SELECT * FROM vessel_position'
    ).fetchall()

    positions = [format_db_row_to_position(row) for row in rows]

    return positions


def delete_all_positions():
    db = get_db()

    db.execute(
        'DELETE FROM vessel_position'
    ).fetchall()

    db.commit()

    return


def insert_single_position(payload):
    row_dict = format_position_to_ready_to_insert_db_row(payload)

    db = get_db()

    try:
        cursor = db.execute(
            "INSERT INTO vessel_position (vessel_id, received_time_utc, latitude, longitude) VALUES (?, ?, ?, ?)",
            (row_dict['vessel_id'], row_dict['received_time_utc'], row_dict['latitude'], row_dict['longitude']),
        )

        db.commit()

        # Get the last inserted row ID
        last_id = cursor.lastrowid
        current_app.logger.info(f"last_id={last_id}   cursor={cursor}")

        cursor = db.execute(
            'SELECT * FROM vessel_position WHERE id = ?', (last_id,)
        )
        last_position_inserted = cursor.fetchone()

        return format_db_row_to_position(last_position_inserted)

    except db.IntegrityError:
        abort(400, description=f"position createdAt{row_dict['received_time_utc']} "
                               f"for vesselId {row_dict['vessel_id']} "
                               f"with longitude {row_dict['longitude']} "
                               f"and latitude {row_dict['latitude']} "
                               f"is already registered.")


def insert_bulk_position(payload):
    # Apply the formatting function to each position in the list
    formatted_positions = [format_position_to_ready_to_insert_db_row(position) for position in payload]

    db = get_db()

    try:
        cursor = db.executemany(
            'INSERT INTO vessel_position (vessel_id, received_time_utc, latitude, longitude) VALUES (?, ?, ?, ?)',
            [(pos['vessel_id'], pos['received_time_utc'], pos['latitude'], pos['longitude']) for pos in formatted_positions]
        )

        db.commit()

    except db.IntegrityError:
        abort(400, description=f"position already exists")


@bp.route('/position', methods=['POST'])
def add_position():
    if request.method == 'POST':
        current_app.logger.debug('Route /position - POST - START')
        payload = request.get_json()
        position_inserted = insert_single_position(payload)
        return jsonify(position_inserted)


@bp.route('/positions', methods=['POST'])
def add_positions_bulk():
    if request.method == 'POST':
        current_app.logger.debug('Route /positions - POST - START')

        payload = request.get_json()
        if not isinstance(payload, list):
            current_app.logger.error('Expected a list of positions but got a different type')
            abort(400, description=f"Wrong type received, expected an array")

        insert_bulk_position(payload)

        return jsonify(retrieve_all_positions())


@bp.route('/positions', methods=['DELETE'])
def delete_positions_bulk():
    if request.method == 'DELETE':
        current_app.logger.debug('Route /positions - DELETE - START')
        delete_all_positions()
        return jsonify({})


@bp.route('/positions', methods=['GET'])
def get_all_positions():
    if request.method == 'GET':
        current_app.logger.debug('Route /positions - GET - START')
        return jsonify(retrieve_all_positions())

