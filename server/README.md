# Server for Kpler technical challenge

## Useful commands

1. Activate virtual environment

```virtualenv -p python3 .venv```

```. .venv/bin/activate```

2. Install requirements

```pip3 install -r requirements.txt```

3. put all requirements into requirement.txt

```pip3 freeze > requirements.txt```

4. Running the server

```python3 -m flask --app flaskr run --debug```

5. Initialize the database

```python3 -m flask --app flaskr init-db```

6. Leave the virtual environment

```deactivate```

