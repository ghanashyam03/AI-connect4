from flask import Flask, request, jsonify
from flask_cors import CORS
from connect4 import Connect4Game
from ai_player import AIPlayer

app = Flask(__name__)
CORS(app)

@app.route('/get_ai_move', methods=['POST'])
def get_ai_move():
    try:
        data = request.json
        print('Request received from frontend:', data)
        
        board_state = data['board_state']
        player = data['player']
        print('Board state received from frontend:', board_state)
        print(player)
        
        game = Connect4Game()
        game.board = board_state
        
        ai_player = AIPlayer()
        column = ai_player.get_move(game)
        print('AI move:', column)
        
        if column is not None:  # Check if the AI move is valid
            game.drop_piece(column, player)  # Update the game state with the AI move

        return jsonify({'column': column, 'updated_board_state': game.board})
    except Exception as e:
        print('Error processing request:', e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
