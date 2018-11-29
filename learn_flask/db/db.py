import json
import requests
import psycopg2

from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)

connect = psycopg2.connect("dbname='structure_department' user='postgres' host='localhost' password='12345'")


@app.route('/get-dep', methods=['GET'])
def get_dep():
    cur = connect.cursor()
    cur.execute('SELECT * FROM structure_department.data.department')
    data_from_db = json.dumps(cur.fetchall())
    return data_from_db


@app.route('/get-team', methods=['GET'])
def get_team():
    cur = connect.cursor()
    cur.execute('SELECT * FROM structure_department.data.team')
    data_from_db = json.dumps(cur.fetchall())
    return data_from_db


@app.route('/get-employee', methods=['GET'])
def get_employee():
    cur = connect.cursor()
    cur.execute('SELECT * FROM structure_department.data.employee')
    data_from_db = json.dumps(cur.fetchall())
    return data_from_db


@app.route('/set-dep', methods=['POST'])
def set_dep():
    data_dep = json.loads(request.get_data())
    if len(data_dep) > 0:
        cur = connect.cursor()
        cur.execute("INSERT INTO structure_department.data.department(name_dep) VALUES (%s)", (data_dep,))
        connect.commit()
    else:
        pass
    return ""


@app.route('/set-team', methods=['POST'])
def set_team():
    data_team = json.loads(request.get_data())
    print(data_team[0])
    if len(data_team[0]) > 0:
        cur = connect.cursor()
        cur.execute("INSERT INTO structure_department.data.team (name_team, id_department, id_manager) VALUES (%s, %s, %s)", (data_team[0], int(data_team[1]), int(data_team[2]),))
        connect.commit()
    else:
        pass
    return ""


@app.route('/set-employee', methods=['POST'])
def set_employee():
    data_employee = json.loads(request.get_data())
    print(data_employee)
    if len(data_employee[0]) > 0:
        cur = connect.cursor()
        cur.execute("INSERT INTO structure_department.data.employee (name, sname, experience, salary, effectiveness_coefficient, position, id_team) VALUES (%s, %s, %s, %s, %s, %s, %s)", (data_employee[0], data_employee[1], int(data_employee[2]), int(data_employee[3]), data_employee[4], data_employee[5], int(data_employee[6]),))
        connect.commit()
    else:
        pass
    return ""

