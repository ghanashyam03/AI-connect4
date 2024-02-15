# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from connect4 import Connect4Game
from ai_player import AIPlayer

app = Flask(__name__)
CORS(app)

game = Connect4Game()
ai_player = AIPlayer()

@app.route('/get_ai_move', methods=['POST'])
def get_ai_move():
    try:
        data = request.json
        board_state = data['board_state']
        player = data['player']

        game.board = board_state

        column = ai_player.get_move(game)

        if column is not None:
            game.drop_piece(column)

        winner = game.get_winner()
        return jsonify({'column': column, 'updated_board_state': game.board, 'winner': winner})
    except Exception as e:
        print('Error processing request:', e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
