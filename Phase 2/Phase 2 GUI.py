import numpy as np
import time
import tkinter as tk
from tkinter import messagebox
import threading
from typing import List, Tuple, Optional, Dict

class ConnectFour:
    
    def __init__(self, rows=6, cols=7):
        self.ROWS = rows
        self.COLS = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1  # Player 1 starts
        self.last_move = None
        self.move_history = []
        
    def copy(self):
        new_game = ConnectFour(self.ROWS, self.COLS)
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.last_move = self.last_move
        new_game.move_history = self.move_history.copy()
        return new_game
    
    def get_valid_moves(self) -> List[int]:
        valid_moves = []
        for col in range(self.COLS):
            if self.board[0][col] == 0:  # Top row is empty
                valid_moves.append(col)
        return valid_moves
    
    # Check if move is valid
    def is_valid_move(self, col: int) -> bool:
        if col < 0 or col >= self.COLS:
            return False
        return self.board[0][col] == 0
    
    # Get the next open row in a column
    def get_next_open_row(self, col: int) -> Optional[int]:
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return None
    
    # Make a move
    def make_move(self, col: int, player: Optional[int] = None) -> bool:
        if not self.is_valid_move(col):
            return False
        
        row = self.get_next_open_row(col)
        if row is None:
            return False
        
        if player is None:
            player = self.current_player
            
        self.board[row][col] = player
        self.last_move = (row, col)
        self.move_history.append(col)
        
        # Switch player
        self.current_player = 3 - self.current_player  # 1->2, 2->1
        
        return True
    
    # Check for a winner
    def check_winner(self) -> Optional[int]:
        # Check horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row][col+1] ==
                    self.board[row][col+2] == self.board[row][col+3]):
                    return self.board[row][col]
        
        # Check vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col] ==
                    self.board[row+2][col] == self.board[row+3][col]):
                    return self.board[row][col]
        
        # Check diagonal
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row-1][col+1] ==
                    self.board[row-2][col+2] == self.board[row-3][col+3]):
                    return self.board[row][col]
        
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col+1] ==
                    self.board[row+2][col+2] == self.board[row+3][col+3]):
                    return self.board[row][col]
        
        return None
    
    # Check if game is done
    def is_game_done(self) -> bool:
        # Check for winner
        if self.check_winner() is not None:
            return True
        
        # Check for draw
        if len(self.get_valid_moves()) == 0:
            return True
        
        return False
    
    
    # display board
    def display(self):
        print("\n" + " ".join([str(i) for i in range(self.COLS)]))
        print("-" * (self.COLS * 2 - 1))
        
        symbols = {0: ".", 1: "X", 2: "O"}
        for row in range(self.ROWS):
            print(" ".join([symbols[self.board[row][col]] for col in range(self.COLS)]))
        print()
    
    # string representation of the board
    def __str__(self):
        symbols = {0: ".", 1: "X", 2: "O"}
        result = []
        for row in range(self.ROWS):
            result.append(" ".join([symbols[self.board[row][col]] for col in range(self.COLS)]))
        return "\n".join(result)

class Evaluator:
    
    def __init__(self, game: ConnectFour):
        self.game = game
        self.ROWS = game.ROWS
        self.COLS = game.COLS
    
    def count_windows(self, board: np.ndarray, player: int) -> Dict[str, int]:
        counts = {
            'four': 0,      # Four in a row (win)
            'three': 0,     # Three with one empty
            'two': 0,       # Two with two empty
            'blocked': 0    # Opponent can block
        }
        
        opponent = 3 - player
        
        # Helper function to evaluate a window
        def evaluate_window(window):
            player_count = np.count_nonzero(window == player)
            opponent_count = np.count_nonzero(window == opponent)
            empty_count = np.count_nonzero(window == 0)
            
            if player_count == 4:
                counts['four'] += 1
            elif player_count == 3 and empty_count == 1:
                counts['three'] += 1
            elif player_count == 2 and empty_count == 2:
                counts['two'] += 1
            elif opponent_count > 0 and player_count > 0:
                counts['blocked'] += 1
        
        # Check horizontal windows
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                window = board[row, col:col+4]
                evaluate_window(window)
        
        # Check vertical windows
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                window = board[row:row+4, col]
                evaluate_window(window)
        
        # Check diagonal
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                window = np.array([board[row-i][col+i] for i in range(4)])
                evaluate_window(window)
        
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                window = np.array([board[row+i][col+i] for i in range(4)])
                evaluate_window(window)
        
        return counts
    
    def evaluate_center_control(self, board: np.ndarray, player: int) -> int:
        center_col = self.COLS // 2
        center_array = board[:, center_col]
        return np.count_nonzero(center_array == player) * 3
    
    def evaluate_position(self, board: np.ndarray, player: int) -> float:
        
        # Check for terminal state first
        temp_game = ConnectFour(self.ROWS, self.COLS)
        temp_game.board = board.copy()
        
        winner = temp_game.check_winner()
        if winner == player:
            return 1000  # Win
        elif winner == (3 - player):
            return -1000  # Loss
        
        # Non-terminal evaluation
        score = 0
        
        # Count windows for player
        player_windows = self.count_windows(board, player)
        score += player_windows['four'] * 1000
        score += player_windows['three'] * 10
        score += player_windows['two'] * 2
        
        # Count windows for opponent
        opponent = 3 - player
        opponent_windows = self.count_windows(board, opponent)
        score -= opponent_windows['four'] * 1000
        score -= opponent_windows['three'] * 10
        score -= opponent_windows['two'] * 2
        
        # Center control bonus
        score += self.evaluate_center_control(board, player)
        score -= self.evaluate_center_control(board, opponent)
        
        return score

class MinimaxAgent:
    
    def __init__(self, game: ConnectFour, max_depth: int = 6):
        self.game = game
        self.max_depth = max_depth
        self.evaluator = Evaluator(game)
        
        # Performance metrics
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.start_time = 0
        self.end_time = 0
        
    # Reset performance metrics
    def reset_metrics(self):
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.start_time = 0
        self.end_time = 0
    
    def minimax(self, game_state: ConnectFour, depth: int, 
                maximizing_player: bool, player: int) -> Tuple[float, Optional[int]]:

        # Update metrics
        self.nodes_explored += 1
        self.max_depth_reached = max(self.max_depth_reached, 
                                     self.max_depth - depth)
        
        # Get valid moves
        valid_moves = game_state.get_valid_moves()
        
        # Terminal state or depth limit reached
        if depth == 0 or game_state.is_game_done() or len(valid_moves) == 0:
            if game_state.is_game_done():
                winner = game_state.check_winner()
                if winner == player:
                    return (1000000, None)  # Win
                elif winner is not None:
                    return (-1000000, None)  # Loss
                else:
                    return (0, None)  # Draw
            else:
                # Evaluate non-terminal position
                score = self.evaluator.evaluate_position(game_state.board, player)
                return (score, None)
        
        # Order moves (center column first for better performance)
        center_col = game_state.COLS // 2
        valid_moves = sorted(valid_moves, 
                           key=lambda x: abs(x - center_col))
        
        if maximizing_player:
            # MAX player (trying to maximize score)
            max_eval = float('-inf')
            best_move = valid_moves[0]
            
            for move in valid_moves:
                # Create child state
                child = game_state.copy()
                child.make_move(move)
                
                # Recursive call
                eval_score, _ = self.minimax(child, depth - 1, False, player)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            
            return (max_eval, best_move)
        
        else:
            # MIN player (trying to minimize score)
            min_eval = float('inf')
            best_move = valid_moves[0]
            
            for move in valid_moves:
                # Create child state
                child = game_state.copy()
                child.make_move(move)
                
                # Recursive call
                eval_score, _ = self.minimax(child, depth - 1, True, player)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            
            return (min_eval, best_move)
    
    def get_best_move(self, game_state: ConnectFour, player: int) -> Tuple[int, Dict]:
        self.reset_metrics()
        self.start_time = time.time()
        
        # Determine if current player is maximizing
        maximizing = (player == 1)
        
        # Call minimax
        score, best_move = self.minimax(game_state, self.max_depth, 
                                       maximizing, player)
        
        self.end_time = time.time()
        
        # Compile metrics
        metrics = {
            'algorithm': 'Minimax',
            'nodes_explored': self.nodes_explored,
            'max_depth_reached': self.max_depth_reached,
            'time_taken': self.end_time - self.start_time,
            'best_score': score,
            'best_move': best_move
        }
        
        return best_move, metrics


class AlphaBetaAgent:
    def __init__(self, game: ConnectFour, max_depth: int = 6):
        self.game = game
        self.max_depth = max_depth
        self.evaluator = Evaluator(game)
        
        # Performance metrics
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.pruning_count = 0  # Number of branches pruned
        self.start_time = 0
        self.end_time = 0
        
    def reset_metrics(self):
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.pruning_count = 0
        self.start_time = 0
        self.end_time = 0
    
    def alpha_beta(self, game_state: ConnectFour, depth: int, 
                   alpha: float, beta: float,
                   maximizing_player: bool, player: int) -> Tuple[float, Optional[int]]:
    
        # Update metrics
        self.nodes_explored += 1
        self.max_depth_reached = max(self.max_depth_reached, 
                                     self.max_depth - depth)
        
        # Get valid moves
        valid_moves = game_state.get_valid_moves()
        
        # Terminal state or depth limit reached
        if depth == 0 or game_state.is_game_done() or len(valid_moves) == 0:
            if game_state.is_game_done():
                winner = game_state.check_winner()
                if winner == player:
                    return (1000000, None)  # Win
                elif winner is not None:
                    return (-1000000, None)  # Loss
                else:
                    return (0, None)  # Draw
            else:
                # Evaluate non-terminal position
                score = self.evaluator.evaluate_position(game_state.board, player)
                return (score, None)
        
        # Order moves (center column first for better pruning)
        center_col = game_state.COLS // 2
        valid_moves = sorted(valid_moves, 
                           key=lambda x: abs(x - center_col))
        
        if maximizing_player:
            # MAX player (trying to maximize score)
            max_eval = float('-inf')
            best_move = valid_moves[0]
            
            for move in valid_moves:
                # Create child state
                child = game_state.copy()
                child.make_move(move)
                
                # Recursive call
                eval_score, _ = self.alpha_beta(child, depth - 1, 
                                               alpha, beta, False, player)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                # Update alpha
                alpha = max(alpha, eval_score)
                
                # Beta cutoff (pruning)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  # Prune remaining branches
            
            return (max_eval, best_move)
        
        else:
            # MIN player (trying to minimize score)
            min_eval = float('inf')
            best_move = valid_moves[0]
            
            for move in valid_moves:
                # Create child state
                child = game_state.copy()
                child.make_move(move)
                
                # Recursive call
                eval_score, _ = self.alpha_beta(child, depth - 1, 
                                               alpha, beta, True, player)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                # Update beta
                beta = min(beta, eval_score)
                
                # Alpha cutoff (pruning)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  # Prune remaining branches
            
            return (min_eval, best_move)
    
    def get_best_move(self, game_state: ConnectFour, player: int) -> Tuple[int, Dict]:
        self.reset_metrics()
        self.start_time = time.time()
        
        # Determine if current player is maximizing
        maximizing = (player == 1)
        
        # Call alpha-beta with initial alpha and beta values
        score, best_move = self.alpha_beta(game_state, self.max_depth,
                                          float('-inf'), float('inf'),
                                          maximizing, player)
        
        self.end_time = time.time()
        
        # Compile metrics
        metrics = {
            'algorithm': 'Alpha-Beta',
            'nodes_explored': self.nodes_explored,
            'max_depth_reached': self.max_depth_reached,
            'pruning_count': self.pruning_count,
            'time_taken': self.end_time - self.start_time,
            'best_score': score,
            'best_move': best_move
        }
        
        return best_move, metrics
    

class ConnectFourGUI:
        
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four - AI Challenge")
        self.root.resizable(False, False)
        
        # Game settings
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.PIECE_RADIUS = 30
        
        # Colors
        self.BG_COLOR = "#1e3a5f"
        self.BOARD_COLOR = "#2a5490"
        self.EMPTY_COLOR = "#ffffff"
        self.PLAYER_COLOR = "#ff4444"
        self.AI_COLOR = "#ffff44"
        self.HOVER_COLOR = "#aaffaa"
        self.GRID_COLOR = "#1a2f4a"
        
        # Game state
        self.game = None
        self.ai_agent = None
        self.ai_depth = 5
        self.use_alphabeta = True
        self.player_turn = True  # Player starts first
        self.game_over = False
        self.thinking = False
        
        # Statistics
        self.stats = {
            'player_wins': 0,
            'ai_wins': 0,
            'draws': 0,
            'total_games': 0
        }
        
        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):\
        # Main container
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Connect Four - AI Challenge",
            font=("Arial", 24, "bold"),
            bg=self.BG_COLOR,
            fg="white"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Controls
        control_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        control_frame.grid(row=1, column=0, padx=(0, 20), sticky="n")
        
        # # Settings Panel
        # settings_label = tk.Label(
        #     control_frame,
        #     text="⚙️ SETTINGS",
        #     font=("Arial", 16, "bold"),
        #     bg=self.BG_COLOR,
        #     fg="white"
        # )
        # settings_label.pack(pady=(0, 10))
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(
            control_frame,
            text="Algorithm",
            font=("Arial", 12, "bold"),
            bg=self.BG_COLOR,
            fg="white",
            padx=10,
            pady=10
        )
        algo_frame.pack(fill="x", pady=5)
        
        self.algo_var = tk.StringVar(value="alphabeta")
        
        tk.Radiobutton(
            algo_frame,
            text="Alpha-Beta Pruning (Fast)",
            variable=self.algo_var,
            value="alphabeta",
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg="white",
            selectcolor=self.BOARD_COLOR,
            command=self.update_algorithm
        ).pack(anchor="w")
        
        tk.Radiobutton(
            algo_frame,
            text="Minimax (Slower)",
            variable=self.algo_var,
            value="minimax",
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg="white",
            selectcolor=self.BOARD_COLOR,
            command=self.update_algorithm
        ).pack(anchor="w")
        
        # Difficulty selection
        difficulty_frame = tk.LabelFrame(
            control_frame,
            text="Difficulty",
            font=("Arial", 12, "bold"),
            bg=self.BG_COLOR,
            fg="white",
            padx=10,
            pady=10
        )
        difficulty_frame.pack(fill="x", pady=5)
        
        tk.Label(
            difficulty_frame,
            text="Search Depth:",
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg="white"
        ).pack()
        
        self.depth_var = tk.IntVar(value=5)
        depth_scale = tk.Scale(
            difficulty_frame,
            from_=3,
            to=7,
            orient="horizontal",
            variable=self.depth_var,
            command=self.update_depth,
            bg=self.BG_COLOR,
            fg="white",
            highlightbackground=self.BG_COLOR,
            length=200
        )
        depth_scale.pack()
        
        self.difficulty_label = tk.Label(
            difficulty_frame,
            text="Medium (Depth: 5)",
            font=("Arial", 10, "italic"),
            bg=self.BG_COLOR,
            fg="#aaffaa"
        )
        self.difficulty_label.pack()
        
        # Status Panel
        status_frame = tk.LabelFrame(
            control_frame,
            text="Status",
            font=("Arial", 12, "bold"),
            bg=self.BG_COLOR,
            fg="white",
            padx=10,
            pady=10
        )
        status_frame.pack(fill="x", pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Your Turn!",
            font=("Arial", 12, "bold"),
            bg=self.BG_COLOR,
            fg="#aaffaa",
            wraplength=200
        )
        self.status_label.pack()
        
        # Statistics Panel
        stats_frame = tk.LabelFrame(
            control_frame,
            text="📊 Statistics",
            font=("Arial", 12, "bold"),
            bg=self.BG_COLOR,
            fg="white",
            padx=10,
            pady=10
        )
        stats_frame.pack(fill="x", pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text=self.get_stats_text(),
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg="white",
            justify="left"
        )
        self.stats_label.pack()
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=20)
        
        self.new_game_btn = tk.Button(
            button_frame,
            text="🔄 New Game",
            command=self.new_game,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.new_game_btn.pack(pady=5)
        
        # self.hint_btn = tk.Button(
        #     button_frame,
        #     text="💡 Hint",
        #     command=self.show_hint,
        #     font=("Arial", 12, "bold"),
        #     bg="#2196F3",
        #     fg="white",
        #     padx=20,
        #     pady=10,
        #     cursor="hand2"
        # )
        # self.hint_btn.pack(pady=5)
        
        # Right panel - Game Board
        board_frame = tk.Frame(main_frame, bg=self.GRID_COLOR)
        board_frame.grid(row=1, column=1)
        
        # Canvas for game board
        canvas_width = self.COLS * self.CELL_SIZE
        canvas_height = self.ROWS * self.CELL_SIZE
        
        self.canvas = tk.Canvas(
            board_frame,
            width=canvas_width,
            height=canvas_height,
            bg=self.BOARD_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_hover)
        
        # Column labels
        label_frame = tk.Frame(board_frame, bg=self.GRID_COLOR)
        label_frame.pack()
        
        for col in range(self.COLS):
            tk.Label(
                label_frame,
                text=str(col),
                font=("Arial", 14, "bold"),
                bg=self.GRID_COLOR,
                fg="white",
                width=int(self.CELL_SIZE / 10)
            ).grid(row=0, column=col)
    
    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw grid and pieces
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = col * self.CELL_SIZE + self.CELL_SIZE // 2
                y = row * self.CELL_SIZE + self.CELL_SIZE // 2
                
                # Draw cell background
                self.canvas.create_rectangle(
                    col * self.CELL_SIZE,
                    row * self.CELL_SIZE,
                    (col + 1) * self.CELL_SIZE,
                    (row + 1) * self.CELL_SIZE,
                    fill=self.BOARD_COLOR,
                    outline=self.GRID_COLOR,
                    width=2
                )
                
                # Draw piece or empty hole
                if self.game.board[row][col] == 0:
                    color = self.EMPTY_COLOR
                elif self.game.board[row][col] == 1:
                    color = self.PLAYER_COLOR
                else:
                    color = self.AI_COLOR
                
                self.canvas.create_oval(
                    x - self.PIECE_RADIUS,
                    y - self.PIECE_RADIUS,
                    x + self.PIECE_RADIUS,
                    y + self.PIECE_RADIUS,
                    fill=color,
                    outline=self.GRID_COLOR,
                    width=2
                )
    
    def handle_hover(self, event):
        if self.game_over or self.thinking or not self.player_turn:
            return
        
        col = event.x // self.CELL_SIZE
        if 0 <= col < self.COLS and self.game.is_valid_move(col):
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.config(cursor="")
    
    def handle_click(self, event):
        if self.game_over or self.thinking or not self.player_turn:
            return
        
        col = event.x // self.CELL_SIZE
        
        if 0 <= col < self.COLS and self.game.is_valid_move(col):
            self.make_player_move(col)
    
    def make_player_move(self, col):
        self.game.make_move(col, 1)
        self.draw_board()
        
        if self.check_game_over():
            return
        
        self.player_turn = False
        self.update_status("AI is thinking...")
        
        # AI move in separate thread to keep GUI responsive
        threading.Thread(target=self.make_ai_move, daemon=True).start()
    
    def make_ai_move(self):
        self.thinking = True
        
        try:
            move, metrics = self.ai_agent.get_best_move(self.game, 2)
            
            # Update UI in main thread
            self.root.after(500, lambda: self.complete_ai_move(move, metrics))
        except Exception as e:
            print(f"AI Error: {e}")
            self.root.after(0, lambda: self.update_status("AI Error!"))
            self.thinking = False
    
    def complete_ai_move(self, move, metrics):
        self.game.make_move(move, 2)
        self.draw_board()
        
        nodes = metrics['nodes_explored']
        time_taken = metrics['time_taken']
        self.update_status(f"AI played column {move}\n({nodes} nodes, {time_taken:.2f}s)")
        
        if not self.check_game_over():
            self.player_turn = True
            self.update_status("Your Turn!")
        
        self.thinking = False
    
    def check_game_over(self):
        if not self.game.is_game_done():
            return False
        
        self.game_over = True
        winner = self.game.check_winner()
        
        if winner == 1:
            result = "You Win!"
            self.stats['player_wins'] += 1
        elif winner == 2:
            result = "AI Wins!"
            self.stats['ai_wins'] += 1
        else:
            result = "Draw!"
            self.stats['draws'] += 1
        
        self.stats['total_games'] += 1
        self.update_stats()
        self.update_status(result)
        
        # Show result dialog
        self.root.after(500, lambda: messagebox.showinfo("Game Over", result))
        
        return True
    
    def new_game(self):
        self.game = ConnectFour()
        self.update_algorithm()
        self.player_turn = True
        self.game_over = False
        self.thinking = False
        self.draw_board()
        self.update_status("Your Turn!")
    
    def update_algorithm(self):
        self.use_alphabeta = (self.algo_var.get() == "alphabeta")
        
        if self.use_alphabeta:
            self.ai_agent = AlphaBetaAgent(self.game, max_depth=self.ai_depth)
        else:
            self.ai_agent = MinimaxAgent(self.game, max_depth=self.ai_depth)
    
    def update_depth(self, value):
        self.ai_depth = int(value)
        
        difficulty_names = {
            3: "Easy",
            4: "Medium-Easy",
            5: "Medium",
            6: "Medium-Hard",
            7: "Hard"
        }
        
        self.difficulty_label.config(
            text=f"{difficulty_names.get(self.ai_depth, 'Custom')} (Depth: {self.ai_depth})"
        )
        
        self.update_algorithm()
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()
    
    def update_stats(self):
        self.stats_label.config(text=self.get_stats_text())
    
    def get_stats_text(self):
        return f"""Games Played: {self.stats['total_games']}
Player Wins: {self.stats['player_wins']}
AI Wins: {self.stats['ai_wins']}
Draws: {self.stats['draws']}

Win Rate: {self.get_win_rate():.1f}%"""
    
    def get_win_rate(self):
        total = self.stats['total_games']
        if total == 0:
            return 0.0
        return (self.stats['player_wins'] / total) * 100
    
    # def show_hint(self):
    #     """Show hint for best move."""
    #     if self.game_over or not self.player_turn or self.thinking:
    #         return
        
    #     self.update_status("Calculating hint...")
        
    #     # Calculate best move for player
    #     hint_agent = AlphaBetaAgent(self.game, max_depth=self.ai_depth)
    #     best_move, metrics = hint_agent.get_best_move(self.game, 1)
        
    #     score = metrics['best_score']
    #     self.update_status(f"💡 Try column {best_move}\n(Score: {score})")
        
    #     # Highlight hint column briefly
    #     self.highlight_column(best_move)
    
    # def highlight_column(self, col):
    #     """Highlight a column temporarily."""
    #     x1 = col * self.CELL_SIZE
    #     x2 = (col + 1) * self.CELL_SIZE
        
    #     highlight = self.canvas.create_rectangle(
    #         x1, 0, x2, self.ROWS * self.CELL_SIZE,
    #         fill="",
    #         outline=self.HOVER_COLOR,
    #         width=4
    #     )
        
    #     self.root.after(1500, lambda: self.canvas.delete(highlight))


def main():
    
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
