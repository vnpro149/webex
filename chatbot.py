from flask import Flask, request, json
import requests
from messenger import Messenger
 
app = Flask(__name__)
port = 5005
msg = Messenger()
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return f'Request received on local port {port}'
    elif request.method == 'POST':
        if 'application/json' in request.headers.get('Content-Type'):
            data = request.get_json()
 
            if msg.bot_id == data.get('data').get('personId'):
                return 'Message from self ignored'
            else:
                print(json.dumps(data,indent=4))
                msg.room_id = data.get('data').get('roomId')
                message_id = data.get('data').get('id')
                msg.get_message(message_id)
 
                if msg.message_text.startswith('/cards'):
                   reply = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').json()
                   msg.reply = reply['deck_id']
                   msg.post_message(msg.room_id, msg.reply)
                else:
                   msg.reply = f'Bot received message "{msg.message_text}"'
                   msg.post_message(msg.room_id, msg.reply)
 
                return data
        else: 
            return ('Wrong data format', 400)
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=False)