from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'biometricData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Biometrics Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biometrics ORDER BY name')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, bios=result)


@app.route('/view/<int:bio_id>', methods=['GET'])
def record_view(bio_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biometrics WHERE id=%s', bio_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', bio=result[0])


@app.route('/edit/<int:bio_id>', methods=['GET'])
def form_edit_get(bio_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biometrics WHERE id=%s', bio_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', bio=result[0])


@app.route('/edit/<int:bio_id>', methods=['POST'])
def form_update_post(bio_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('name'), request.form.get('sex'), request.form.get('age'),
                 request.form.get('height_in'), request.form.get('weight_lbs'), bio_id)
    sql_update_query = """UPDATE biometrics t SET t.name = %s, t.sex = %s, t.age = %s, t.height_in = 
    %s, t.weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/bios/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Biometric Form')


@app.route('/bios/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('name'), request.form.get('sex'), request.form.get('age'),
                 request.form.get('height_in'), request.form.get('weight_lbs'))
    sql_insert_query = """INSERT INTO biometrics (name,sex,age,height_in,weight_lbs) VALUES (%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:bio_id>', methods=['POST'])
def form_delete_post(bio_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biometrics WHERE id = %s """
    cursor.execute(sql_delete_query, bio_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/bios', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biometrics')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/bios/<int:bio_id>', methods=['GET'])
def api_retrieve(bio_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biometrics WHERE id=%s', bio_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/bios/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/bios/<int:bio_id>', methods=['PUT'])
def api_edit(bio_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/bios/<int:bio_id>', methods=['DELETE'])
def api_delete(bio_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
