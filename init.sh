#!/bin/sh
sudo apt install -y python3.12 python3.12-venv
python3.12 -m venv .venv 
. .venv/bin/activate
pip install -r requirements.txt
flask --app exuniverse init-db
