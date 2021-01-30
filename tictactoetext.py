board_size = 3 # 3X3 보드의 한 변의 크기

# 게임을 위한 보드를 생성하고, 0으로 초기화해서 넘겨준다.
def make_board():
    board = [[0 for i in range(board_size)] for j in range(board_size)]
    return board

# 게임 진행을 위하여 마크할 위치의 번호와 이미 마크된 상태를 보여준다.
def show_board(board):
    player_list = [' ', 'X', 'O']
    str_board = "[1, 2, 3]\n"\
                "[4, 5, 6]\n"\
                "[7, 8, 9]\n"
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] != 0:
                player = board[i][j] 
                # 2차원 리스트의 좌표를 번호로 바꿔준다.
                value = i * board_size + j + 1
                # 숫자로된 번호를 마크로 바꿔준다.
                str_board = str_board.replace(str(value), player_list[player])
    print(str_board)

# 카보드로부터 유효한 값을 입력받기 위한 함수
def input_data(board, player):
    # 입력값을 체크하기 위한 문자열
    value_list = "123456789"
    while True:
        value = input("어떤 곳에 두시겠습니까? (1 ~ 9) : ")
        # 입력된 문자가 문자열에 포함되지 않았을 경우 -1을 리턴하므로 입력범위를 체크하기 편리하다.
        if value_list.find(value) < 0:
            print("입력이 잘못되었습니다. 1 ~ 9 사이의 숫자를 입력하세요.")
            continue
        value = int(value)
        # 1차원 리스트를 2차원 리스트로 변경하기 위한 절차.
        row = int((value - 1) / board_size) 
        col = int((value - 1) % board_size)
        if board[row][col] != 0:
            print("이미 놓인 자리입니다.")
        else:
            board[row][col] = player
            break
    show_board(board)

# 승리 여부를 체크하기 위한 함수
def is_win(board, player):
    # 행과 열 체크
    for y in range(3):
        if board[y][0] == player:
            # 행이 세개가 같은지 체크한다.
            if board[y][0] == board[y][1] and board[y][1] == board[y][2]:
                return True
        if board[0][y] == player:
            # 열이 세개가 같은지 체크한다.
            if board[0][y] == board[1][y] and board[1][y] == board[2][y]:
                return True
    # 왼쪽 상단에서 오른쪽 하단으로 된 대각선을 체크한다.
    if board[0][0] == player and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return True
    # 왼쪽 하단에서 오른쪽 상단으로 된 대각선을 체크한다.
    if board[2][0] == player and board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return True
    return False

# 보드가 다 채워졌는지 체그하기 위한 함수
def is_full(board):
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                return False
    return True

# 게임이 끝났을 때 화면에 메시지를 출력해주는 함수
def show_message(player):
    msg = ["Draw!!", "X Player won!!", "O Player won!!"]
    print(msg[player])
                
# 게임의 종료 여부를 판단하기 위한 함수
def is_finish(board, player):
    if is_win(board, player):
        show_message(player)
    elif is_full(board):
        show_message(0)
    else:
        return False
    return True

# 게임을 진행하기 위한 함수
def play_game(board, player):
    while True:
        input_data(board, player)
        # 한 수씩 둘 때마다 체크해야 된다.
        if is_finish(board, player):
            break
        # 한 수를 두게 되면 턴을 바꾸어 선수를 교체한다.
        # 선수는 1과 2이므로 3에서 빼주면 1 또는 2가 되어 선수가 교체되는 효과를 보인다.
        player = 3 - player

# 게임이 종료되었을 때 계속할것인지를 결정하기 위한 함수
def is_continue():
    while True:
        answer = input("계속 하시겠습니까? y/n : ")
        if answer.lower() == 'n':
            return False
        elif answer.lower() == 'y':
            break
    return True


def main():
    while True:
        # 게임이 끝나고 새로운 게임을 하기 위해서는 새로운 보드가 필요하므로 이곳에 있어야 한다.
        board = make_board()
        show_board(board)
        play_game(board, 1)
        if not is_continue():
            break


if __name__ == "__main__":
    main()    