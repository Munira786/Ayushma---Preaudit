@echo off
REM Backend server launcher that handles the app.py main block

python -c "from backend.app import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
