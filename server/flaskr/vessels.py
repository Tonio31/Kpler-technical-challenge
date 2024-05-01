import functools

import datetime

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from dateutil import parser

bp = Blueprint('vessels', __name__, url_prefix='/vessels')


def format_position(row):
    """Format a database row into a predefined dictionary format."""
    return {
        "id": row['id'],
        "vesselId": row['vessel_id'],
        "createdAt": row['received_time_utc'].isoformat() + 'Z',  # Adding 'Z' to denote UTC time
        "latitude": row['latitude'],
        "longitude": row['longitude']
    }


def insert_single_position(payload):
    """Format a database row into a predefined dictionary format."""
    vesselId = payload['vesselId']
    createdAt = payload['createdAt']
    longitude = payload['longitude']
    latitude = payload['latitude']

    current_app.logger.info(
        f"vesselId {vesselId} with longitude {longitude} and  latitude {latitude}  createdAt={createdAt}.")

    received_time = parser.parse(createdAt)
    received_time_utc = received_time.astimezone(datetime.timezone.utc)
    received_time_utc_formatted_for_sql = received_time_utc.strftime('%Y-%m-%d %H:%M:%S')

    error = ''
    if not vesselId:
        error += 'VesselId is required.'

    if not createdAt:
        error += ' createdAt is required.'

    if not longitude:
        error += ' longitude is required.'

    if not latitude:
        error += ' latitude is required.'

    db = get_db()

    if error == '':
        try:
            cursor = db.execute(
                "INSERT INTO vessel_position (vessel_id, received_time_utc, latitude, longitude) VALUES (?, ?, ?, ?)",
                (vesselId, received_time_utc_formatted_for_sql, longitude, latitude),
            )

            db.commit()

            # Get the last inserted row ID
            last_id = cursor.lastrowid
            current_app.logger.info(f"last_id={last_id}   cursor={cursor}")

            cursor = db.execute(
                'SELECT * FROM vessel_position WHERE id = ?', (last_id,)
            )
            last_position_inserted = cursor.fetchone()

            row_position_dict = {
                "id": last_position_inserted['id'],
                "vesselId": last_position_inserted['vessel_id'],
                "createdAt": last_position_inserted['received_time_utc'].isoformat() + 'Z',
                # Adding 'Z' to denote UTC time
                "latitude": last_position_inserted['latitude'],
                "longitude": last_position_inserted['longitude']
            }

            current_app.logger.info(f"last_position_inserted={jsonify(row_position_dict)}")

            return row_position_dict

        except db.IntegrityError:
            error = f"position for vesselId {vesselId} with longitude {longitude} and latitude {latitude} is already registered."

    flash(error)


@bp.route('/position', methods=['POST'])
def position():
    if request.method == 'POST':
        current_app.logger.debug('This is a DEBUG message')
        current_app.logger.info('This is an INFO message and its amazing')
        current_app.logger.warning('This is a WARNING message')
        current_app.logger.error('This is an ERROR message')
        current_app.logger.critical('This is a CRITICAL message FUCK')

        payload = request.get_json()
        position_inserted = insert_single_position(payload)

        return jsonify(position_inserted)

        # error = ''
        # vesselId = payload['vesselId']
        # createdAt = payload['createdAt']
        # longitude = payload['longitude']
        # latitude = payload['latitude']
        #
        # current_app.logger.info(f"vesselId {vesselId} with longitude {longitude} and  latitude {latitude}  createdAt={createdAt}.")
        #
        # received_time = parser.parse(createdAt)
        # received_time_utc = received_time.astimezone(datetime.timezone.utc)
        # received_time_utc_formatted_for_sql = received_time_utc.strftime('%Y-%m-%d %H:%M:%S')
        #
        # if not vesselId:
        #     error += 'VesselId is required.'
        #
        # if not createdAt:
        #     error += ' createdAt is required.'
        #
        # if not longitude:
        #     error += ' longitude is required.'
        #
        # if not latitude:
        #     error += ' latitude is required.'
        #
        # db = get_db()
        #
        # if error == '':
        #     try:
        #         cursor = db.execute(
        #             "INSERT INTO vessel_position (vessel_id, received_time_utc, latitude, longitude) VALUES (?, ?, ?, ?)",
        #             (vesselId, received_time_utc_formatted_for_sql, longitude, latitude),
        #         )
        #
        #         db.commit()
        #
        #         # Get the last inserted row ID
        #         last_id = cursor.lastrowid
        #         current_app.logger.info(f"last_id={last_id}   cursor={cursor}")
        #
        #         cursor = db.execute(
        #             'SELECT * FROM vessel_position WHERE id = ?', (last_id,)
        #         )
        #         last_position_inserted = cursor.fetchone()
        #
        #         row_dict = {
        #             "id": last_position_inserted['id'],
        #             "vesselId": last_position_inserted['vessel_id'],
        #             "createdAt": last_position_inserted['received_time_utc'].isoformat() + 'Z',  # Adding 'Z' to denote UTC time
        #             "latitude": last_position_inserted['latitude'],
        #             "longitude": last_position_inserted['longitude']
        #         }
        #
        #         current_app.logger.info(f"last_position_inserted={jsonify(row_dict)}")
        #
        #         return jsonify(row_dict)
        #
        #     except db.IntegrityError:
        #         error = f"position for vesselId {vesselId} with longitude {longitude} and latitude {latitude} is already registered."
        #     else:
        #         return jsonify(status="ok")
        #
        #
        # flash(error)

@bp.route('/positions', methods=['GET'])
def positions():
    db = get_db()

    rows = db.execute(
        'SELECT * FROM vessel_position'
    ).fetchall()

    positions = [format_position(row) for row in rows]

    return jsonify(positions)


@bp.route('/test', methods=['POST'])
def logout():
    payload = request.get_json()
    # username = payload['bob']
    current_app.logger.debug('This is a DEBUG payload=%s', payload)
    return jsonify(test="HURGGGGGHHHHH")