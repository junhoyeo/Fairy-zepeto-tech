from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('frame')
def received_frame(url):
    print(url)

if __name__ == '__main__':
    socketio.run(app)
