# Basic Flask Application

This project is a small Flask API with two REST endpoints, JSON validation, and automated tests.

## What it does

- `GET /hello` returns a JSON greeting. It accepts an optional `name` query parameter, removes extra spaces, and formats each word consistently.
- `POST /sum` accepts a JSON object with a `numbers` list and returns the total.
- Invalid names and requests to `/sum` return a JSON error and HTTP status `400`.

## Setup

These commands use Windows PowerShell.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source venv/bin/activate`.

## Run the server

```powershell
python app.py
```

The API starts locally at `http://127.0.0.1:5000`.

Try the greeting endpoint in a browser or PowerShell:

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/hello?name=Joshua"
```

Expected result:

```json
{"greeting":"Hello, Joshua!"}
```

In a second PowerShell window, test the sum endpoint:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/sum" -ContentType "application/json" -Body '{"numbers":[1,2,3]}'
```

Expected result:

```json
{"numbers":[1,2,3],"sum":6}
```

## Run the tests

```powershell
pytest test_app.py
```

The tests check successful requests, cleaned name input, length limits, and bad-input responses. A passing run should report `11 passed`.
