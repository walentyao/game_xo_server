import websocket
from pyswip import Prolog


def move_bot(board_list):
    result_query = list(prolog.query(f"minimax([{board_list[0]},"
                                     f"{board_list[1]},{board_list[2]},"
                                     f"{board_list[3]},{board_list[4]},"
                                     f"{board_list[5]},{board_list[6]},"
                                     f"{board_list[7]},{board_list[8]}], NextMove)."))
    index = 0
    new_board_list = result_query[0]['NextMove']
    for i in range(len(new_board_list) - 1):
        if board_list[i] != str(new_board_list[i]):
            index = i
        board_list[i] = str(new_board_list[i])
    # print(index)
    return index


def move_player(position: int, board_list):
    board_list[position] = 'o'


def winning(board, player):
    if board[0] == player and board[1] == player and board[2] == player:
        return True
    if board[3] == player and board[4] == player and board[5] == player:
        return True
    if board[6] == player and board[7] == player and board[8] == player:
        return True
    if board[0] == player and board[3] == player and board[6] == player:
        return True
    if board[1] == player and board[4] == player and board[7] == player:
        return True
    if board[2] == player and board[5] == player and board[8] == player:
        return True
    if board[0] == player and board[4] == player and board[8] == player:
        return True
    if board[2] == player and board[4] == player and board[6] == player:
        return True
    return False


def check_winner(board):
    if winning(board, player_symbol):
        print("You win!")
        return 'you_win'

    if winning(board, bot_symbol):
        print("Sorry you loooser!")
        return 'yuo_loose'

    if board.count('n') == 0 and not winning(board, player_symbol) and not winning(board, bot_symbol):
        print("Ничья!")
        return 'neutral'

    return 'not_win'


def new_game():
    board = ["n", "n", "n", "n", "n", "n", "n", "n", "n"]
    return board


def update_state_game(state_game_dict, value):
    match value:
        case 'play':
            state_game_dict['status_game'] = 'play'
        case 'end':
            state_game_dict['status_game'] = 'end'
        case 'player':
            state_game_dict['first_hod'] = 'player'
            state_game_dict['hod'] = state_game_dict['first_hod']
        case 'bot':
            state_game_dict['first_hod'] = 'bot'
            state_game_dict['hod'] = state_game_dict['first_hod']


prolog = Prolog()
prolog.consult('minimax.pl')
bot_symbol = 'x'
player_symbol = 'o'
current_board = ["n", "n", "n", "n", "n", "n", "n", "n", "n"]
ws = websocket.WebSocket()
commands_move = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
state_game = {'first_hod': '', 'status_game': '', 'hod': ''}
ws.connect("ws://localhost:8000")

while True:
    response = str(ws.recv())
    command = response
    if response in commands_move:
        command = 'move'
    else:
        command = 'not-move'
    # print(response)

    update_state_game(state_game, response)

    if state_game['hod'] == 'player' and state_game['status_game'] == 'play':
        if command == 'move':
            move_player(int(response), current_board)
            print(state_game['hod'])
            print(current_board)
            state_game['hod'] = 'bot'

    if state_game['hod'] == 'bot' and state_game['status_game'] == 'play':
        index_move_bot = move_bot(current_board)
        ws.send(str(index_move_bot))
        print(state_game['hod'])
        print(current_board)
        state_game['hod'] = 'player'

    if response == 'new_game':
        current_board = new_game()

    check_win = check_winner(current_board)
    if check_win != 'not_win':
        state_game['status_game'] = 'end'
        ws.send(check_win)

    if response == 'disconnected':
        break
