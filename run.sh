. .venv/bin/activate
# flask --app exuniverse run --debug
python3 _update.py
gunicorn -b 192.168.1.177:8000 exuniverse_app

# FOR LOCAL TESTING:
# gunicorn exuniverse_app