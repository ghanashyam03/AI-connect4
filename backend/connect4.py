class Connect4Game:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[None] * self.cols for _ in range(self.rows)]
        self.turn = 1

    def drop_piece(self, column):  # Add the player argument
        if 0 <= column < self.cols and self.is_valid_move(column):
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][column] is None:
                    self.board[row][column] = 2  # Pass the player argument here
                    return True
            return False  # Column is full
        else:
            return False 
        
    def drop(self, column):  # Add the player argument
        if 0 <= column < self.cols and self.is_valid_move(column):
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][column] is None:
                    self.board[row][column] = 1  # Pass the player argument here
                    return True
            return False  # Column is full
        else:
            return False # Invalid move

    def is_valid_move(self, column):
        return self.board[0][column] is None

    def is_winner(self, player):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Check diagonal (top-left to bottom-right)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Check diagonal (bottom-left to top-right)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def is_game_over(self):
        return self.is_winner(1) or self.is_winner(2) or self.is_board_full()

    def is_board_full(self):
        return all(self.board[row][col] is not None for row in range(self.rows) for col in range(self.cols))
    
    def copy(self):
        new_game = Connect4Game()
        new_game.rows = self.rows
        new_game.cols = self.cols
        new_game.board = [row[:] for row in self.board]  # Deep copy of the board
        new_game.turn = self.turn
        return new_game
    
    def get_winner(self):
        for player in [1, 2]:
            if self.is_winner(player):
                return player
        return None