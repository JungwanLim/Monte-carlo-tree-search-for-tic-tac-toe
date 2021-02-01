import random
from abc import*

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)
LEFT_UP = (-1, 1)
RIGHT_DOWN = (1, -1)
LEFT_DOWN = (-1, -1)
RIGHT_UP = (1, 1)

ROW = [LEFT, RIGHT]
COLUMN = [UP, DOWN]
DIAGONAL1 = [LEFT_UP, RIGHT_DOWN]
DIAGONAL2 = [LEFT_DOWN, RIGHT_UP]

# Board의 상태를 저장하고, 관리한다.
class Board:
    def __init__(self):
        self.board = None
        self.board_size = 3
        self.current_position = 0
        self.count = 0
        
    def set_board(self):
        self.board = [[0, 0, 0], [ 0, 0, 0], [ 0, 0, 0]]
        self.count = 0

    def get_row_col(self, position):
        row = int(position / self.board_size)
        col = int(position % self.board_size)
        return row, col

    def set_cell(self, position, player):
        row, col = self.get_row_col(position)
        self.board[row][col] = player
        self.current_position = position
        self.count += 1

    def set_zero(self, position):
        row, col = self.get_row_col(position)
        self.board[row][col] = 0
        self.count -= 1

    def get_cell_count(self):
        return self.count

    def get_xy_point(self, position):
        y, x = self.get_row_col(position)
        return [x, y]

    def get_xy_value(self, position, dx, dy):
        y, x = self.get_row_col(position)
        return x + dx, y + dy

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

    # 행, 열 또는 두 대각선을 검사하여 같은 모양의 개수를 count하여 리턴
    def get_count(self, player,direction):
        count = 1 #처음 한 수를 둔 자리를 기준으로 검사
        for dir in direction: # ROW, COLUMN등 한 방향
            dx, dy = dir[0], dir[1] # LEFT(-1, 0) 등
            x, y = self.get_xy_value(self.current_position, dx, dy)
            while True:
                # 보드의 범위를 벗어났나 검사
                if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
                    break
                # 같은 모양이 아니면 탈출
                elif self.board[y][x] != player:
                    break
                else:
                    count += 1 #같은 모양이면 count 증가하고
                    x, y = x + dx, y + dy # 또 한칸을 이동
        return count == self.board_size

# 화면에 출력하는 역할을 하는 class
class Display:
    def __init__(self):
        print("Tic Tac Toe v1.0")
        self.player_list = [' ', 'X', 'O']
        self.str_board = None # 여러 게임을 하기 위하여 별도의 초기화 함수를 둠

    def set_str_board(self):
        self.str_board = "[1, 2, 3]\n"\
                         "[4, 5, 6]\n"\
                         "[7, 8, 9]\n"

    # 현재 두어진 상태를 화면에 표시
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
            # 보드는 (0,0)으로 시작하므로 1을 빼줘야 정확한 좌표계산이 가능
            # 착수한 위치의 번호를 넘겨준다.
            return int(value) - 1

    # 화면에 필요한 message를 출력해준다.
    def show_message(self, player = 3):
        msg = ["Draw!!", "X Player won!!", "O Player won!!", "이미 놓인 자리입니다."]
        print(msg[player])

    def show_order(self, player):
        order = ["User 차례입니다.", "AI 차례입니다."]
        print(order[player - 1])
                
    def is_continue(self):
        while True:
            answer = input("계속 하시겠습니까? y/n : ")
            if answer.lower() == 'n':
                return False
            elif answer.lower() == 'y':
                break
        return True

# 컴퓨터와 사람은 두는 방법이 다르므로 추상클래스와 상속을 통해 다형성 구현
class Player(metaclass = ABCMeta):
    # Board와 Display는 사람과 컴퓨터가 공유하여야 하기 때문에 클래스 멤버로 선언
    board = None
    display = None  
    winner = 0

    # 사람이나 컴퓨터나 착수를 하고나서 보드에 저장하고 화면에 출력하는 동작은 같으므로 부모 클래스에
    def show_result(self, position, player):
        self.board.set_cell(position, player) # 보드에 저장
        self.display.mark_str_board(position + 1, player) # 화면에 보여질 보드에 저장
        self.display.print_str_board() # 한 수 둔 결과를 보여줌
        return position

    # 승리를 검사하는 함수
    def is_win(self, player):
        # 가로 세로 대각선 순으로 검사한다.
        directions = [ROW, COLUMN, DIAGONAL1, DIAGONAL2]
        for direction in directions:
            if self.board.get_count(player, direction):
                return True
        return False

    def is_draw(self):
        if self.board.get_cell_count() == 9:
            return True
        return False

    def show_order(self, player):
        self.display.show_order(player)

    @abstractmethod
    def action(self):
        pass

class User(Player):
    def __init__(self):
        self.ID = 1

    def action(self):
        while True:
            position = self.display.input_data(self.ID)
            if self.board.get_cell(position) != 0:
                self.display.show_message()
            else:
                return self.show_result(position, self.ID)

class AI(Player):
    def __init__(self):
        self.first = False
        self.ID = 2
        self.depth = 7
        self.best_positions = []

    def get_best_position(self):
        max = self.best_positions[0][1]
        best_position = self.best_positions[0][0]
        for best in self.best_positions[1:]:
            if max < best[1]:
                max = best[1]
                best_position = best[0]
        return best_position

    def get_first_position(self):
        return random.randint(0, 8)

    def is_finish(self, player):
        if self.is_win(player):
            self.winner = player
        elif self.board.get_cell_count() == 9:
            self.winner = 0
        else:
            return False
        return True

    def evaluation(self):
        if self.winner == self.ID:
            self.winner = 0
            return 1
        elif self.winner == 0:
            return 0
        else:
            self.winner = 0
            return -1

    def action(self):
        if self.first:
            position = self.get_first_position()
            self.first = False
        else:
            self.minimax(self.depth, self.ID)
            position = self.get_best_position()
            self.best_positions = []
        return self.show_result(position, self.ID)

    def minimax(self, depth, player):
        if depth == 0 or self.is_finish(3 - player):
            return self.evaluation()

        positions = self.board.get_empty_positions()
        max_score = -100
        min_score = 100
        for position in positions:
            if player == self.ID:
                self.board.set_cell(position, player)
                score = self.minimax(depth - 1, 3 - self.ID)
                max_score = max(max_score, score)
                if depth == self.depth:
                    self.best_positions.append([position, max_score])
            else:
                self.board.set_cell(position, player)
                score = self.minimax(depth - 1, self.ID)
                min_score = min(min_score, score)
            self.board.set_zero(position)

        if player == self.ID:
            return max_score
        else:
            return min_score


class Tictactoe:
    def __init__(self):
        self.board = Board()
        self.display = Display()
        Player.board = self.board
        Player.display = self.display
        self.user = User()
        self.computer = AI()
        self.player = [self.user, self.computer]

    def init_game(self):
        self.board.set_board()
        self.display.set_str_board()
        self.display.print_str_board()

    def is_finish(self, player):
        if player.is_win(player.ID):
            self.display.show_message(player.ID)
        elif player.is_draw():
            self.display.show_message(0)
        else:
            return False
        return True

    def is_continue(self):
        return self.display.is_continue()

    def play_game(self):
        player = random.choice(self.player)
        if player.ID == 2:
            player.first = True
        while True:
            player.show_order(player.ID)
            position = player.action()
            if self.is_finish(player):
                break
            player = self.player[2 - player.ID]      


def main():
    # 게임을 관리하는 객체만 있으면 됨
    ttt = Tictactoe()
    while True:
        # 게임시 시작되면 필요한 데이터를 초기화
        ttt.init_game()
        ttt.play_game()
        if not ttt.is_continue():
            break

if __name__ == "__main__":
    main()  