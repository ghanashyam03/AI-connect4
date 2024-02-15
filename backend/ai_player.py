import random

class AIPlayer:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
    
    def get_move(self, game):
        best_move = self.alpha_beta_search(game, self.max_depth, float('-inf'), float('inf'), True)[0]
        return best_move if best_move is not None else self.random_move(game)

    def random_move(self, game):
        valid_moves = [col for col in range(game.cols) if game.is_valid_move(col)]
        return random.choice(valid_moves) if valid_moves else None
    
    def alpha_beta_search(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_game_over():
            return None, self.evaluate(game)
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for column in self.shuffle_columns(game):
                if game.is_valid_move(column):
                    game_copy = game.copy()
                    game_copy.drop_piece(column)  # Simulate AI move
                    _, eval_value = self.alpha_beta_search(game_copy, depth - 1, alpha, beta, False)
                    if eval_value > max_eval:
                        max_eval = eval_value
                        best_move = column
                        if max_eval == float('inf'):  # If winning move found, no need to search further
                            break
                    alpha = max(alpha, eval_value)
                    if beta <= alpha:
                        break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for column in self.shuffle_columns(game):
                if game.is_valid_move(column):
                    game_copy = game.copy()
                    game_copy.drop(column)  # Simulate opponent move
                    _, eval_value = self.alpha_beta_search(game_copy, depth - 1, alpha, beta, True)
                    if eval_value < min_eval:
                        min_eval = eval_value
                        best_move = column
                        if min_eval == -float('inf'):  # If losing move found, no need to search further
                            break
                    beta = min(beta, eval_value)
                    if beta <= alpha:
                        break
            return best_move, min_eval
    
    def evaluate(self, game):
        if game.is_winner(2):
            return float('inf')  # AI wins
        elif game.is_winner(1):
            return -float('inf')  # Opponent wins
        else:
            score_player_1 = self.count_connected_sequences(game, 1)
            score_player_2 = self.count_connected_sequences(game, 2)
            return score_player_2 - score_player_1  # Advantage for AI
    
    def count_connected_sequences(self, game, player):
        count = 0
        for row in range(game.rows):
            for col in range(game.cols):
                if game.board[row][col] == player:
                    # Check horizontal
                    if col + 3 < game.cols:
                        if game.board[row][col+1] == game.board[row][col+2] == game.board[row][col+3] == player:
                            count += 1
                    # Check vertical
                    if row + 3 < game.rows:
                        if game.board[row+1][col] == game.board[row+2][col] == game.board[row+3][col] == player:
                            count += 1
                    # Check diagonal (top-left to bottom-right)
                    if col + 3 < game.cols and row + 3 < game.rows:
                        if game.board[row+1][col+1] == game.board[row+2][col+2] == game.board[row+3][col+3] == player:
                            count += 1
                    # Check diagonal (bottom-left to top-right)
                    if col + 3 < game.cols and row - 3 >= 0:
                        if game.board[row-1][col+1] == game.board[row-2][col+2] == game.board[row-3][col+3] == player:
                            count += 1
        return count
    
    def shuffle_columns(self, game):
        columns = list(range(game.cols))
        random.shuffle(columns)
        return columns
