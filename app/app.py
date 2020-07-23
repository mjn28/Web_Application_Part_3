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
app.config['MYSQL_DATABASE_DB'] = 'oscarAges'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Female Oscar Winner Ages'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM femaleOscarAges ORDER BY fldyear')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, actress=result)


@app.route('/view/<int:age_id>', methods=['GET'])
def record_view(age_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM femaleOscarAges WHERE id=%s', age_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', age=result[0])


@app.route('/edit/<int:age_id>', methods=['GET'])
def form_edit_get(age_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM femaleOscarAges WHERE id=%s', age_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', age=result[0])


@app.route('/edit/<int:age_id>', methods=['POST'])
def form_update_post(age_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldAge'), request.form.get('fldName'),
                 request.form.get('fldFilm'), age_id)
    sql_update_query = """UPDATE femaleOscarAges t SET t.fldYear = %s, t.fldAge = %s, t.fldName = %s, t.fldFilm = 
    %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/actress/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Entry Form')


@app.route('/actress/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldAge'), request.form.get('fldName'),
                 request.form.get('fldFilm'))
    sql_insert_query = """INSERT INTO femaleOscarAges (fldYear,fldAge,fldName,fldFilm) VALUES (%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:age_id>', methods=['POST'])
def form_delete_post(age_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM femaleOscarAges WHERE id = %s """
    cursor.execute(sql_delete_query, age_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/actress', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM femaleOscarAges')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/actress/<int:age_id>', methods=['GET'])
def api_retrieve(age_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM femaleOscarAges WHERE id=%s', age_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/actress/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/actress/<int:age_id>', methods=['PUT'])
def api_edit(age_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/actress/<int:age_id>', methods=['DELETE'])
def api_delete(age_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
