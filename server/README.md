# Server for Kpler technical challenge

## Instruction during tutorial

1. When using a new terminal start by activating virtual environment

```. .venv/bin/activate```

2. put all requirements into requirement.txt

```pip3 freeze > requirements.txt```

2. Running the server

```python3 -m flask --app flaskr run --debug```

3. Initialize the database

```python3 -m flask --app flaskr init-db```