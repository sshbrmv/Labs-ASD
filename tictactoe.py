import tkinter as tk
from tkinter import messagebox
import copy
import random

root, board, current_player, game_mode, game_active, player_symbol = None, None, None, None, None, None
buttons, status_label, mode_frame, board_frame, restart_button, player_choice_frame, back_button = [], None, None, None, None, None, None
winning_combinations = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def create_widgets():
    global root, mode_frame, board_frame, status_label, restart_button, buttons, player_choice_frame, back_button
    root = tk.Tk()
    root.title("Крестики-Нолики")
    root.geometry("400x500")
    root.configure(bg="#f0f0f0")
    tk.Label(root, text="Крестики-Нолики", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=10)
    mode_frame = tk.Frame(root, bg="#f0f0f0")
    mode_frame.pack(pady=10)
    tk.Label(mode_frame, text="Выберите режим игры:", font=("Arial", 14), bg="#f0f0f0").pack()
    tk.Button(mode_frame, text="Играть с ботом", font=("Arial", 12), command=show_player_choice).pack(pady=5)
    tk.Button(mode_frame, text="Два игрока", font=("Arial", 12), command=lambda: start_game("two", "X")).pack(pady=5)
    player_choice_frame = tk.Frame(root, bg="#f0f0f0")
    tk.Label(player_choice_frame, text="Выберите очередность хода:", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
    tk.Button(player_choice_frame, text="Играть за X", font=("Arial", 12), command=lambda: start_game("bot", "X")).pack(pady=5)
    tk.Button(player_choice_frame, text="Играть за O", font=("Arial", 12), command=lambda: start_game("bot", "O")).pack(pady=5)
    tk.Button(player_choice_frame, text="Вернуться", font=("Arial", 12), command=reset_to_mode_selection).pack(pady=5)
    board_frame = tk.Frame(root, bg="#f0f0f0")
    for i in range(3):
        for j in range(3):
            btn = tk.Button(board_frame, text=" ", font=("Arial", 20, "bold"), width=5, height=2, command=lambda x=i, y=j: make_move(x*3+y))
            btn.grid(row=i, column=j, padx=5, pady=5)
            buttons.append(btn)
    status_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0", fg="#333333")
    status_label.pack(pady=10)
    restart_button = tk.Button(root, text="Начать заново", font=("Arial", 12), command=restart_game)
    back_button = tk.Button(root, text="Вернуться", font=("Arial", 12), command=reset_to_mode_selection)
    restart_button.pack(pady=10)
    restart_button.pack_forget()
    back_button.pack_forget()

def show_player_choice():
    mode_frame.pack_forget()
    player_choice_frame.pack(pady=10)

def start_game(mode, symbol):
    global board, current_player, game_mode, game_active, player_symbol
    game_mode, game_active, board, player_symbol = mode, True, [" "]*9, symbol
    current_player = "X" if symbol == "X" else "X"  # Бот всегда за X, если игрок выбрал O
    player_choice_frame.pack_forget()
    mode_frame.pack_forget()
    board_frame.pack(pady=10)
    restart_button.pack()
    back_button.pack()
    update_board()
    if mode == "bot" and symbol == "O" and game_active:
        root.after(500, bot_move)

def make_move(index):
    global current_player, game_active
    if not game_active or board[index] != " ": return
    board[index] = current_player
    update_board()
    if check_winner(current_player):
        if game_mode == "bot" and current_player == player_symbol:
            status_label.config(text="Вы победили!")
            messagebox.showinfo("Победа!", "Вы победили!")
        elif game_mode == "bot" and current_player != player_symbol:
            status_label.config(text="Победил Бот!")
            messagebox.showinfo("Поражение!", "Победил Бот!")
        else:
            status_label.config(text=f"Игрок {current_player} победил!")
            messagebox.showinfo("Победа!", f"Игрок {current_player} победил!")
        game_active = False
        return
    if all(cell != " " for cell in board):
        status_label.config(text="Ничья!")
        game_active = False
        messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
        return
    current_player = "O" if current_player == "X" else "X"
    if game_mode == "bot" and current_player != player_symbol and game_active:
        root.after(500, bot_move)

def bot_move():
    best_score, best_moves = -float('inf'), []
    for i in range(9):
        if board[i] == " ":
            board[i] = "O" if player_symbol == "X" else "X"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score, best_moves = score, [i]
            elif score == best_score:
                best_moves.append(i)
    if best_moves: make_move(random.choice(best_moves))

def minimax(temp_board, depth, is_maximizing):
    bot_symbol = "O" if player_symbol == "X" else "X"
    player_sym = "X" if player_symbol == "X" else "O"
    if check_winner(bot_symbol): return 10 - depth
    if check_winner(player_sym): return depth - 10
    if all(cell != " " for cell in temp_board): return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if temp_board[i] == " ":
                temp_board[i] = bot_symbol
                score = minimax(temp_board, depth + 1, False)
                temp_board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if temp_board[i] == " ":
                temp_board[i] = player_sym
                score = minimax(temp_board, depth + 1, True)
                temp_board[i] = " "
                best_score = min(score, best_score)
        return best_score

def check_winner(player):
    return any(all(board[i] == player for i in combo) for combo in winning_combinations)

def update_board():
    for i, btn in enumerate(buttons): btn.config(text=board[i])

def restart_game():
    global board, current_player, game_active
    board, game_active = [" "]*9, True
    current_player = "X" if player_symbol == "X" or game_mode == "two" else "X"
    status_label.config(text="")
    update_board()
    if game_mode == "bot" and player_symbol == "O" and game_active:
        root.after(500, bot_move)

def reset_to_mode_selection():
    global board, current_player, game_active
    board, current_player, game_active = [" "]*9, "X", False
    player_choice_frame.pack_forget()
    board_frame.pack_forget()
    restart_button.pack_forget()
    back_button.pack_forget()
    mode_frame.pack(pady=10)
    status_label.config(text="")
    update_board()

if __name__ == "__main__":
    create_widgets()
    root.mainloop()
