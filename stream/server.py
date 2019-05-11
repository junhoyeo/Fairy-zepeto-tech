from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO

from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('frame')
def received_frame(url):
    url = url.replace('data:image/png;base64,', '')
    print(datetime.now(), 'Frame Received!')

    frame = Image.open(BytesIO(base64.b64decode(url)))
    
    frame = frame.convert('RGB') # get rid of alpha channel for JPEG format
    buffered = BytesIO()
    frame.save(buffered, format='JPEG')
    processed_url = base64.b64encode(buffered.getvalue())

    socketio.emit('processed', 'data:image/png;base64,' + str(processed_url.decode()))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8001)
