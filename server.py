from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import redis
import hashlib
import logging

app = Flask(__name__, template_folder='./')
CORS(app)

server_port = int(os.environ.get('CC_SERVER_PORT', 5000))
server_address = os.environ.get('CC_SERVER_ADDRESS', "http://127.0.0.1")
database_address = os.environ.get('CC_DB_ADDRESS', "postgres://ccapp@postgres/ccdb")
database_name = os.environ.get('CC_DB_NAME', "ccdb")
database_user = os.environ.get('CC_DB_USER', "ccapp")
database_password = os.environ.get('CC_DB_PASS', "password")
database_port = int(os.environ.get('CC_DB_PORT', "6379"))
expiration_time = int(os.environ.get('CC_EXPIRATION', 10))


@app.route("/")
def get_main_page():
    return render_template("index.html", server_port=server_port, server_address=server_address)


@app.route("/add", methods=['POST'])
def add_note():
    text = json.loads(request.data)["text"]
    key = hashlib.sha256(text.encode('utf-8')).hexdigest()[:10]
    r = connect_db()
    r.set(key, text, ex=expiration_time)
    r.close()
    response = jsonify({'url': f'{server_address}:{server_port}/show?note_id={key}'})
    return response


@app.route("/show", methods=['GET'])
def get_note_page():
    note_id = request.args['note_id']
    print(note_id)
    return render_template("index2.html", note_id=note_id, server_port=server_port, server_address=server_address)


@app.route("/note", methods=['GET'])
def get_note():
    note_id = request.args['note_id']
    r = connect_db()
    txt = r.get(note_id)
    # r.delete(note_id)
    r.close()
    if txt is None:
        txt = "Note Does Not Exist!"
    else:
        txt = txt.decode('UTF-8')
    response = jsonify({'note': txt})
    return response


def connect_db():
    """ Connect to the PostgreSQL database server """
    _conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the Redis database...')
        _r = redis.Redis(
            host=database_address,
            port=database_port,
            password=database_password)
        return _r
    except (Exception, redis.RedisError) as error:
        print(error)


if __name__ == '__main__':
    connect_db()
    app.run(debug=True, host='0.0.0.0', port=server_port)
