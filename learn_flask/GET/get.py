import json
import requests
import psycopg2

from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)



def get_dep():
    r = requests.get('http://localhost:5002/get-dep')
    return json.loads(r.content)


def get_team():
    r = requests.get('http://localhost:5002/get-team')
    return json.loads(r.content)


def get_employee():
    r = requests.get('http://localhost:5002/get-employee')
    return json.loads(r.content)


def salary_employee(i):
    new_salary = i[3]
    if i[2] > 2 and i[2] <= 5:
        new_salary = int(i[3]) + 200
    elif i[2] > 5:
        new_salary = int(i[3]) * 1.2 + 500
    return new_salary


def salary_designer(i):
    new_salary = int(i[3]) * float(i[7])
    return new_salary


def salary_manager(emp, i):
    new_salary = i[3]
    id_team = i[4]
    if count_dev_of_team(emp, id_team)[0] > 5 and count_dev_of_team(emp, id_team)[0] <= 10 and count_dev_of_team(emp, id_team)[0] / count_dev_of_team(emp, id_team)[1] > 2:
        new_salary = i[3] + 200
    elif count_dev_of_team(emp, id_team)[0] > 10 and count_dev_of_team(emp, id_team)[0] / count_dev_of_team(emp, id_team)[1] > 2:
        new_salary = i[3] + 300
    elif count_dev_of_team(emp, id_team)[0] / count_dev_of_team(emp, id_team)[1] <= 2:
        new_salary = i[3] * 1.1
    return new_salary


def count_dev_of_team(emp, id_team):
    count_team = 0
    count_dev = 0
    for i in emp:
        if i[4] == id_team:
            count_team += 1
        if i[6].lower() == "developer":
            count_dev += 1
    return count_team, count_dev


def new_salary(L):
    data_list = []
    for i in L:
        new_sal = []
        if i[6].lower() != "designer" and i[6].lower() != "manager":
            new_sal.append(i[0])
            new_sal.append(i[1])
            new_sal.append(int(salary_employee(i)))
        elif i[6].lower() == "designer":
            new_sal.append(i[0])
            new_sal.append(i[1])
            new_sal.append(int(salary_designer(i)))
        elif i[6].lower() == "manager":
            new_sal.append(i[0])
            new_sal.append(i[1])
            new_sal.append(salary_manager(L, i))

        data_list.append(new_sal)
    return data_list


def repr_employee(emp, team):
    data_list = []
    for i in emp:
        data_employee = []
        manager = None
        if i[6].lower() != "manager":
            manager = emp[(team[i[4]-1][2])-1][1]
            data_employee.append(i[0])
            data_employee.append(i[1])
            data_employee.append(manager)
            data_employee.append(i[2])
        if i[6].lower() == "manager":
            data_employee.append(i[0])
            data_employee.append(i[1])
            data_employee.append("no manager")
            data_employee.append(i[2])
        data_list.append(data_employee)
    return data_list



@app.route('/get-info', methods=['GET'])
def get_info():
    res_salary = new_salary(get_employee())
    res_repr_employee = repr_employee(get_employee(), get_team())
    res = json.dumps([res_salary, res_repr_employee])
    return res