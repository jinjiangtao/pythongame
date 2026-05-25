import tkinter as tk
from tkinter import messagebox, ttk

class GameView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("五子棋")
        
        self.CELL_SIZE = 35
        self.PADDING = 30
        self.BOARD_SIZE = 15
        self.CANVAS_SIZE = self.PADDING * 2 + (self.BOARD_SIZE - 1) * self.CELL_SIZE
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.status_label = ttk.Label(main_frame, text="当前回合：黑棋", 
                                     font=("微软雅黑", 14, "bold"))
        self.status_label.grid(row=0, column=0, pady=10, sticky=tk.N)
        
        self.canvas = tk.Canvas(main_frame, width=self.CANVAS_SIZE, height=self.CANVAS_SIZE, 
                                bg="#DEB887")
        self.canvas.grid(row=1, column=0, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        self.restart_btn = ttk.Button(button_frame, text="重新开局", 
                                      command=self.controller.handle_restart)
        self.restart_btn.grid(row=0, column=0, padx=5)
        
        self.undo_btn = ttk.Button(button_frame, text="悔棋", 
                                   command=self.controller.handle_undo)
        self.undo_btn.grid(row=0, column=1, padx=5)
        
        self.exit_btn = ttk.Button(button_frame, text="退出游戏", 
                                   command=self.controller.handle_exit)
        self.exit_btn.grid(row=0, column=2, padx=5)
        
        self.draw_board()
    
    def draw_board(self):
        self.canvas.delete("all")
        
        for i in range(self.BOARD_SIZE):
            x = self.PADDING + i * self.CELL_SIZE
            self.canvas.create_line(x, self.PADDING, x, self.CANVAS_SIZE - self.PADDING, 
                                   fill="#8B4513", width=1)
        
        for i in range(self.BOARD_SIZE):
            y = self.PADDING + i * self.CELL_SIZE
            self.canvas.create_line(self.PADDING, y, self.CANVAS_SIZE - self.PADDING, y, 
                                   fill="#8B4513", width=1)
        
        star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for row, col in star_points:
            x = self.PADDING + col * self.CELL_SIZE
            y = self.PADDING + row * self.CELL_SIZE
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#8B4513")
    
    def draw_piece(self, row, col, player, is_winning=False):
        x = self.PADDING + col * self.CELL_SIZE
        y = self.PADDING + row * self.CELL_SIZE
        radius = 15
        
        if player == 1:
            if is_winning:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                                       fill="#FFD700", outline="#000000", width=2)
            else:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                                       fill="#000000", outline="#000000", width=1)
                self.canvas.create_oval(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, 
                                       fill="#333333", outline="")
        else:
            if is_winning:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                                       fill="#FFD700", outline="#000000", width=2)
            else:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                                       fill="#FFFFFF", outline="#000000", width=1)
                self.canvas.create_oval(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, 
                                       fill="#EEEEEE", outline="")
    
    def update_board(self, board, winning_line=None):
        self.draw_board()
        
        if winning_line is None:
            winning_line = []
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                player = board[row][col]
                if player != 0:
                    is_winning = (row, col) in winning_line
                    self.draw_piece(row, col, player, is_winning)
    
    def update_status(self, player, game_over, winner):
        if game_over:
            if winner == 0:
                self.status_label.config(text="对局结束：平局")
            elif winner == 1:
                self.status_label.config(text="对局结束：黑棋获胜！")
            else:
                self.status_label.config(text="对局结束：白棋获胜！")
        else:
            if player == 1:
                self.status_label.config(text="当前回合：黑棋")
            else:
                self.status_label.config(text="当前回合：白棋")
    
    def on_canvas_click(self, event):
        x = event.x
        y = event.y
        
        col = round((x - self.PADDING) / self.CELL_SIZE)
        row = round((y - self.PADDING) / self.CELL_SIZE)
        
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            self.controller.handle_move(row, col)
    
    def show_message(self, title, message):
        messagebox.showinfo(title, message)
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")