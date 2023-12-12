. .venv/bin/activate
# flask --app exuniverse run --debug
python3 _update.py
gunicorn -b 192.168.1.177:8000 exuniverse:app

# FOR LOCAL TESTING:
# gunicorn exuniverse:app 