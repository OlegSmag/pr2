import json
import requests
import psycopg2

from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)


@app.route('/posting', methods=['POST'])
def posting():
    all_data = json.loads(request.get_data())
    print(all_data)

    data_dep = json.dumps(all_data['department'], indent=2, ensure_ascii=False)
    data_team = json.dumps(all_data['team'], indent=2, ensure_ascii=False)
    data_employee = json.dumps(all_data['employee'], indent=2, ensure_ascii=False)
    requests.post('http://localhost:5002/set-dep', data_dep)
    requests.post('http://localhost:5002/set-team', data_team)
    requests.post('http://localhost:5002/set-employee', data_employee)
    return ""