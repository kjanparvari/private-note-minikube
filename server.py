from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__, template_folder='./')
CORS(app)

server_port = int(os.environ.get('CC_SERVER_PORT', 5000))
server_address = os.environ.get('CC_SERVER_ADDRESS', "http://127.0.0.1")
database_address = os.environ.get('CC_DB_ADDRESS', "172.17.0.2")
database_username = os.environ.get('CC_DB_USERNAME', "ccapp")
database_password = os.environ.get('CC_DB_PASSWORD', "")
expiration_time = int(os.environ.get('CC_EXPIRATION', 2))

txt = "orem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."


@app.route("/")
def get_main_page():
    return render_template("index.html", server_port=server_port, server_address=server_address)


@app.route("/add", methods=['POST'])
def add_note():
    print(json.loads(request.data))
    response = jsonify({'url': f'{server_address}:{server_port}/show?note_id={"U4JF9H31F"}'})
    return response


@app.route("/show", methods=['GET'])
def get_note_page():
    note_id = request.args['note_id']
    print(note_id)
    return render_template("index2.html", note_id="note_id", server_port=server_port, server_address=server_address)


@app.route("/note", methods=['GET'])
def get_note():
    note_id = request.args['note_id']
    print(note_id)
    response = jsonify({'note': f"this is requested note for {note_id}.\n{txt}"})
    return response


def setup_db():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=server_port)
