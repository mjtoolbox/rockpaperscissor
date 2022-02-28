from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

player1 = ''
player2 = ''
player1choice = ''
player2choice = ''
winningmsg = ''


@app.route('/')
def sessions():
    return render_template('chat.html')


@app.route('/reset')
def reset():
    global player1choice
    global player2choice
    global player1
    global player2

    player1choice = ''
    player2choice = ''
    player1 = ''
    player2 = ''
    return render_template('chat.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('echo')
def handle_chat_event(json, methods=['GET', 'POST']):
    print('Server side received on Chat: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('game')
def handle_game(data, methods=['GET', 'POST']):

    global player1choice
    global player2choice
    global player1
    global player2

    data = str(data).replace("\'", "\"")
    print("User submitted: " + str(data))
    entry = json.loads(str(data))
    choice = entry["message"]
    playerid = entry["user"]

    if player1choice == '':
        player1choice = choice
        player1 = playerid
        socketio.emit('choicemade', "Player " + playerid + " made a choice." , callback=messageReceived)
    else:
        player2choice = choice
        player2 = playerid

        print("1", player1choice)
        print("2", player2choice)

        if player1choice == player2choice:
            winningmsg = "Tie, try again"
        elif player1choice == 'rock' and player2choice == 'paper':
            winningmsg = player2 + " is a winner! Player1 " + player1choice + ", Player2 " + player2choice
        elif player1choice == 'rock' and player2choice == 'scissor':
            winningmsg = player1 + " is a winner! Player1 " + player1choice + ", Player2 " + player2choice
        elif player1choice == 'paper' and player2choice == 'rock':
            winningmsg = player1 + " is a winner! Player1 " + player1choice + ", Player2 " + player2choice
        elif player1choice == 'paper' and player2choice == 'scissor':
            winningmsg = player2 + " is a winner! Player1 " + player1choice + ", Player2 " + player2choice
        elif player1choice == 'scissor' and player2choice == 'rock':
            winningmsg = player2 + " is a winner! Player1 " + player1choice + ", Player2 " + player2choice
        elif player1choice == 'scissor' and player2choice == 'paper':
            winningmsg = player1 + " is a winner! Player1 " + player1choice + ", Player2 " + player2choice

        socketio.emit('choicemade', "Player " + playerid + " made a choice.", callback=messageReceived)
        socketio.emit('result', winningmsg, callback=messageReceived)


if __name__ == "__main__":
    # app.config['DEBUG'] = True
    # app.run()
    socketio.run(app, debug=True)
