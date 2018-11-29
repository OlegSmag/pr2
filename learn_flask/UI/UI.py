import json
import requests

from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form_pages.html')


@app.route('/salary', methods=['GET'])
def post_info():
    a = json.loads(requests.get('http://localhost:5003/get-info').content)
    salary = a[0]
    return render_template('salary.html', a=salary)


@app.route('/repr_employee', methods=['GET'])
def post_info_emp():
    a = json.loads(requests.get('http://localhost:5003/get-info').content)
    repr_emp = a[1]
    return render_template('repr_employee.html', a=repr_emp)


@app.route('/add_data', methods=['POST'])
def add_data():
    first_name = request.form['first_name']
    
    data_from_form = {'department':request.form['name_of_department'],
                      'team':[request.form['name_of_team'],
                              request.form['department_id'],
                              request.form['manager_id']],
                      'employee':[request.form['first_name'],
                                  request.form['surname'],
                                  request.form['experience'],
                                  request.form['salary'],
                                  request.form['effectiveness_coefficient'],
                                  request.form['position'],
                                  request.form['team_id']
                                  ]
                                }

    requests.post('http://localhost:5001/posting', json.dumps(data_from_form, indent=2, ensure_ascii=False))    
    return redirect(url_for('index'))
