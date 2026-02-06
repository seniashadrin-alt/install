import tkinter as tk
import random

# Настройки
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 60

# Цвета фигур (яркие оттенки)
COLORS = [
    '#FF6B6B',  # красный
    '#4ECDC4',  # бирюзовый
    '#45B7D1',  # голубой
    '#96CEB4',  # мятный
    '#D9534F',  # томатный
    '#5CB85C',  # зелёный
    '#FAD390',  # персиковый
    '#FFC312',  # оранжевый
    '#7F8FA6',  # серый
    '#A3CB38',  # салатовый
    '#1289A7',  # синий
    '#D980FA',  # фиолетовый
    '#F79F83',  # коралловый
    '#F5F0E1',  # бежевый
    '#341C99'   # темно-фиолетовый
]

# Формы фигур (7 классических + новые)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1]],  # одиночный квадратик
    [[1, 1, 1, 1, 1]],  # длинная палочка
    [[1, 1, 1], [0, 1, 1]],  # угол
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]],  # L с длинной ножкой
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],  # J с длинной ножкой
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # T с длинной ножкой
    [[1, 1, 1], [1, 1, 0], [0, 0, 1]],  # сложная фигура
    [[1, 1, 1], [0, 1, 1], [0, 1, 0]]  # сложная фигура
]

class Tetris:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Цветной Тетрис")
        
        # Экран старта
        self.start_screen()
    
    def start_screen(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack()
        
        title_label = tk.Label(self.start_frame, text="Тетрис", font=("Arial", 24), bg='#222', fg='white')
        title_label.pack(pady=20)
        
        play_button = tk.Button(self.start_frame, text="Play", command=self.start_game)
        play_button.pack(pady=10)
    
    def start_game(self):
        self.start_frame.destroy()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg='#222')
        self.canvas.pack()
        
        self.paused = False  # Переменная состояния паузы
        self.score = 0
        self.level = 1
        self.speed = 1000 // self.level
        
        self.board = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_piece = None
        self.game_over = False
        
        self.score_label = tk.Label(self.root, text="Счёт: 0", font=("Arial", 14), bg='#222', fg='white')
        self.score_label.pack(pady=5)
        
        # Добавляем кнопку паузы в верхний правый угол
        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side=tk.RIGHT, anchor=tk.N)
        
        self.new_piece()
        self.draw_board()
        self.root.after(self.speed, self.update)
        self.root.bind('<Key>', self.handle_key)
    
    def toggle_pause(self):
        """ Переключает состояние паузы """
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text="PAUSED", font=("Arial", 24, "bold"), fill="yellow")
        else:
            self.canvas.delete("all")  # Очистка экрана перед продолжением игры
            self.draw_board()          # Перерисовка доски
            self.root.after(self.speed, self.update)  # Продолжаем обновление игры
    
    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        x = COLUMNS // 2 - len(shape[0]) // 2
        y = 0
        self.current_piece = {'shape': shape, 'color': color, 'x': x, 'y': y}
    
    def draw_board(self):
        self.canvas.delete('all')  # Полностью очищаем экран
        # Рисуем сетку
        for y in range(ROWS):
            for x in range(COLUMNS):
                if self.board[y][x]:
                    self.draw_block(x, y, self.board[y][x])
                else:
                    self.canvas.create_rectangle(
                        x * GRID_SIZE, y * GRID_SIZE,
                        (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE,
                        outline='#333', width=1
                    )
        
        # Рисуем текущую фигуру
        if self.current_piece:
            shape = self.current_piece['shape']
            color = self.current_piece['color']
            x, y = self.current_piece['x'], self.current_piece['y']
            for dy, row in enumerate(shape):
                for dx, cell in enumerate(row):
                    if cell:
                        self.draw_block(x + dx, y + dy, color)
    
    def draw_block(self, x, y, color):
        self.canvas.create_rectangle(
            x * GRID_SIZE, y * GRID_SIZE,
            (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE,
            fill=color, outline='#FFF', width=2
        )
    
    def is_valid_move(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_piece['shape']
        x, y = self.current_piece['x'] + dx, self.current_piece['y'] + dy
        for dy_i, row in enumerate(shape):
            for dx_i, cell in enumerate(row):
                if cell:
                    nx, ny = x + dx_i, y + dy_i
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS or (ny >= 0 and self.board[ny][nx]):
                        return False
        return True
    
    def merge_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        x, y = self.current_piece['x'], self.current_piece['y']
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell and y + dy >= 0:
                    self.board[y + dy][x + dx] = color
    
    def clear_lines(self):
        lines_cleared = 0
        for y in reversed(range(ROWS)):
            if all(self.board[y]):
                del self.board[y]
                self.board.insert(0, [0] * COLUMNS)
                lines_cleared += 1
        if lines_cleared:
            self.score += lines_cleared * 100 * self.level
            self.level = (self.score // 1000) + 1
            self.speed = max(100, 1000 // self.level)
            self.score_label.config(text=f"Счёт: {self.score} | Уровень: {self.level}")
    
    def update(self):
        if not self.game_over and not self.paused:
            if self.is_valid_move(0, 1):
                self.current_piece['y'] += 1
            else:
                self.merge_piece()
                self.clear_lines()
                self.new_piece()
                if not self.is_valid_move(0, 0):
                    self.game_over = True
                    self.show_game_over()
            self.draw_board()
            self.root.after(self.speed, self.update)
    
    def handle_key(self, event):
        key = event.keysym
        if key == 'Escape':
            self.toggle_pause()  # Переключение состояния паузы
        elif not self.paused:
            if key == 'Left' and self.is_valid_move(-1, 0):
                self.current_piece['x'] -= 1
            elif key == 'Right' and self.is_valid_move(1, 0):
                self.current_piece['x'] += 1
            elif key == 'Down' and self.is_valid_move(0, 1):
                self.current_piece['y'] += 1
            elif key == 'Up':
                # Поворот фигуры (транспонирование матрицы)
                shape = self.current_piece['shape']
                rotated = [[shape[y][x] for y in reversed(range(len(shape)))] for x in range(len(shape[0]))]
                if self.is_valid_move(0, 0, rotated):
                    self.current_piece['shape'] = rotated
            self.draw_board()
    
    def show_game_over(self):
        game_over_frame = tk.Frame(self.root)
        game_over_frame.pack()
        
        game_over_label = tk.Label(game_over_frame, text="GAME OVER", font=("Arial", 24), bg='#222', fg='white')
        game_over_label.pack(pady=20)
        
        restart_button = tk.Button(game_over_frame, text="Restart", command=self.restart_game)
        restart_button.pack(pady=10)
    
    def restart_game(self):
        self.root.destroy()
        Tetris()

if __name__ == "__main__":
    Tetris()
    tk.mainloop()