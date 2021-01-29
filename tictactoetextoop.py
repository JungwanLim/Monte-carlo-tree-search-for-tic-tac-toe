import random
from abc import*

class Board:
    def __init__(self):
        self.board = None
        self.board_size = 3

    def set_board(self):
        self.board = [[0, 0, 0], [ 0, 0, 0], [ 0, 0, 0]]

    # def get_board(self):
    #     return self.board

    # def set_cell(self, row, col, player):
    #     self.board[row][col] = player

    # def get_cell(self, row, col):
    #     return self.board[row][col]

    # 3x3 board에서 빈 셀을 찾아서 넘겨주는 함수
    # def get_empty_cells(self):
    #     # 보드의 빈 공간들을 저장할 리스트
    #     empty_cells = []
    #     for row in range(self.board_size):
    #         for col in range(self.board_size):
    #             if self.board[row][col] == 0:
    #                 empty_cells.append([row, col])
    #     return empty_cells        

    def get_row_col(self, position):
        row = int(position / self.board_size)
        col = int(position % self.board_size)
        return row, col

    def set_cell(self, position, player):
        row, col = self.get_row_col(position)
        self.board[row][col] = player

    def get_cell(self, position):
        row, col = self.get_row_col(position)
        return self.board[row][col]

    # 3x3 board에서 빈 셀을 찾아서 넘겨주는 함수
    def get_empty_positions(self):
        # 보드의 빈 공간들을 저장할 리스트
        empty_positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 0:
                    empty_positions.append(row * self.board_size + col)
        return empty_positions        

    def get_count(self, player, point, dir_index):
        direction = [[1, 0], [-1, 0], [1, 1], [-1, -1], [0, 1], [0, -1], [-1, 1], [1, -1]]
        count = 1
        for i in range(2):
            dx, dy = direction[i + dir_index]
            x = point[0] + dx
            y = point[1] + dy
            while True:
                if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
                    break
                elif self.board[y][x] != player:
                    break
                else:
                    count += 1
                    x += dx
                    y += dy
        return count == self.board_size


class Display:
    def __init__(self, board):
        print("Tic Tac Toe v1.0")
        self.board = board
        self.player_list = [' ', 'X', 'O']
        self.str_board = None

    def set_str_board(self):
        self.str_board = "[1, 2, 3]\n"\
                         "[4, 5, 6]\n"\
                         "[7, 8, 9]\n"

    def print_str_board(self):
        print(self.str_board)

    # 게임 진행을 위하여 선택된 위치의 번호를 마크로 바꿔준다.
    def mark_str_board(self, position, player):
        self.str_board = self.str_board.replace(str(position), self.player_list[player])

    # 카보드로부터 유효한 값을 입력받기 위한 함수
    def input_data(self, player):
        # 입력값을 체크하기 위한 문자열
        value_list = "123456789"
        while True:
            value = input("어떤 곳에 두시겠습니까? (1 ~ 9) : ")
            # 입력된 문자가 문자열에 포함되지 않았을 경우 -1을 리턴.
            if value_list.find(value) < 0:
                print("입력이 잘못되었습니다. 1 ~ 9 사이의 숫자를 입력하세요.")
                continue
            value = int(value)
            if self.board.get_cell(value - 1) != 0:
                print("이미 놓인 자리입니다.")
            else:
                self.board.set_cell(value - 1, player)
                self.mark_str_board(value, player)
                self.print_str_board()
                return value - 1

    def show_message(self, player):
        msg = ["Draw!!", "X Player won!!", "O Player won!!"]
        print(msg[player])
                
    def is_continue(self):
        while True:
            answer = input("계속 하시겠습니까? y/n : ")
            if answer.lower() == 'n':
                return False
            elif answer.lower() == 'y':
                break
        return True


class Player(metaclass = ABCMeta):
    @abstractmethod
    def action(self):
        pass

class User(Player):
    def __init__(self, display):
        self.ID = 1
        self.display = display

    def action(self):
        return self.display.input_data(self.ID)

    def show_me(self):
        print("User 차례입니다.")


class AI(Player):
    def __init__(self, board, display):
        self.ID = 2
        self.board = board
        self.display = display

    def action(self):
        position = random.choice(self.board.get_empty_positions())
        self.board.set_cell(position, self.ID)
        self.display.mark_str_board(position + 1, self.ID)
        self.display.print_str_board()
        return position

    def show_me(self):
        print("AI 차례입니다.")


class Tictactoe:
    def __init__(self):
        self.board = Board()
        self.display = Display(self.board)
        self.user = User(self.display)
        self.computer = AI(self.board, self.display)
        self.player = [self.user, self.computer]

    def init_game(self):
        self.board.set_board()
        self.display.set_str_board()
        self.display.print_str_board()

    def is_win(self, player, point):
        dir_index = 0
        for i in range(4):
            if self.board.get_count(player, point, dir_index):
                return True
            dir_index += 2
        return False

    def is_draw(self):
        if self.board.get_empty_positions() == []:
            return True
        return False

    def is_finish(self, player, point):
        if self.is_win(player, point):
            self.display.show_message(player)
        elif self.is_draw():
            self.display.show_message(0)
        else:
            return False
        return True

    def is_continue(self):
        return self.display.is_continue()

    def play_game(self):
        player = random.choice(self.player)
        while True:
            player.show_me()
            position = player.action()
            row, col = self.board.get_row_col(position)
            if self.is_finish(player.ID, [col, row]):
                break
            player = self.player[3 - player.ID - 1]

def main():
    ttt = Tictactoe()
    while True:
        ttt.init_game()
        ttt.play_game()
        if not ttt.is_continue():
            break

if __name__ == "__main__":
    main()            