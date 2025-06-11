from flask import Flask, render_template, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "Tictactoe"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize or reset game
def init_game():
    session["board"] = [" "]*9
    session["current_player"] = "X"
    session["winner"] = None
    session["tie"] = False

def check_win(board, player):
    win_combo = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(board[i] == player for i in combo) for combo in win_combo)

@app.route("/")
def index():
    if "board" not in session:
        init_game()
    return  render_template("index.html", board=session["board"],
                                current_player=session["current_player"],
                                winner=session["winner"], tie=session["tie"],)

@app.route("/move/<int:position>")
def move(position):
    if session.get("winner") or session.get("tie"):
        return  redirect(url_for("index"))

    board = session["board"]
    player = session["current_player"]

    if board[position] == " ":
        board[position] = player
        if check_win(board, player):
            session["winner"] = player
        elif " " not in board:
            session["tie"] = True
        else:
            session['current_player'] = "O" if player == "X" else "X"

    session["board"] = board
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    init_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
