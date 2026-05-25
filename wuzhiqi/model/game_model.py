import copy

class GameModel:
    def __init__(self):
        self.BOARD_SIZE = 15
        self.EMPTY = 0
        self.BLACK = 1
        self.WHITE = 2
        
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = self.BLACK
        self.history = []
        self.game_over = False
        self.winner = None
        self.winning_line = []
    
    def reset_game(self):
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = self.BLACK
        self.history = []
        self.game_over = False
        self.winner = None
        self.winning_line = []
    
    def get_board(self):
        return copy.deepcopy(self.board)
    
    def is_valid_move(self, row, col):
        if row < 0 or row >= self.BOARD_SIZE or col < 0 or col >= self.BOARD_SIZE:
            return False
        if self.board[row][col] != self.EMPTY:
            return False
        if self.game_over:
            return False
        return True
    
    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = self.current_player
        self.history.append((row, col, self.current_player))
        
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
        elif self.check_draw():
            self.game_over = True
            self.winner = 0
        else:
            self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK
        
        return True
    
    def check_win(self, row, col):
        directions = [
            [(0, 1), (0, -1)],
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]
        
        player = self.board[row][col]
        
        for dir_pair in directions:
            line = [(row, col)]
            
            for dx, dy in dir_pair:
                r, c = row + dx, col + dy
                while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == player:
                    line.append((r, c))
                    r += dx
                    c += dy
            
            if len(line) >= 5:
                self.winning_line = line[:5]
                return True
        
        return False
    
    def check_draw(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == self.EMPTY:
                    return False
        return True
    
    def undo_move(self):
        if len(self.history) == 0:
            return False
        
        row, col, player = self.history.pop()
        self.board[row][col] = self.EMPTY
        self.current_player = player
        self.game_over = False
        self.winner = None
        self.winning_line = []
        
        return True
    
    def get_history_count(self):
        return len(self.history)
    
    def get_current_player(self):
        return self.current_player
    
    def is_game_over(self):
        return self.game_over
    
    def get_winner(self):
        return self.winner
    
    def get_winning_line(self):
        return self.winning_line