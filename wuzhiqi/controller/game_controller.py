import sys

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def handle_move(self, row, col):
        if self.model.is_game_over():
            self.view.show_message("提示", "游戏已结束，请重新开局！")
            return
        
        if not self.model.is_valid_move(row, col):
            if self.model.get_board()[row][col] != 0:
                self.view.show_message("提示", "该位置已有棋子，请选择其他位置！")
            return
        
        self.model.make_move(row, col)
        self.update_view()
        
        if self.model.is_game_over():
            winner = self.model.get_winner()
            if winner == 0:
                self.view.show_message("游戏结束", "平局！棋盘已满，无人获胜。")
            elif winner == 1:
                self.view.show_message("游戏结束", "黑棋获胜！")
            else:
                self.view.show_message("游戏结束", "白棋获胜！")
    
    def handle_restart(self):
        self.model.reset_game()
        self.view.update_board(self.model.get_board())
        self.view.update_status(self.model.get_current_player(), 
                               self.model.is_game_over(), 
                               self.model.get_winner())
        self.view.show_message("提示", "已重新开局！")
    
    def handle_undo(self):
        if self.model.get_history_count() == 0:
            self.view.show_message("提示", "没有可撤回的步骤！")
            return
        
        self.model.undo_move()
        self.view.update_board(self.model.get_board())
        self.view.update_status(self.model.get_current_player(), 
                               self.model.is_game_over(), 
                               self.model.get_winner())
    
    def handle_exit(self):
        if self.view.show_message("确认退出", "确定要退出游戏吗？"):
            sys.exit(0)
    
    def update_view(self):
        board = self.model.get_board()
        winning_line = self.model.get_winning_line()
        self.view.update_board(board, winning_line)
        self.view.update_status(self.model.get_current_player(), 
                               self.model.is_game_over(), 
                               self.model.get_winner())