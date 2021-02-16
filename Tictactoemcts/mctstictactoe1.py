import random
from abc import*
import copy
import math
import datetime

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
        self.board = None # 여러 게임을 하기 위해서 생성자에서 초기화 하지 않음
        self.player = 1
        self.position = -1
        self.total_count = 0
        self.board_size = 3

    # 새 게임이 시작되면 0으로 초기화 된다.    
    def set_board(self):
        self.board = [[0, 0, 0], [ 0, 0, 0], [ 0, 0, 0]]
        self.total_count = 0

    def set_player(self, player):
        self.player = player

    # def get_board(self):
    #     return self.board

    # def set_cell(self, row, col, player):
    #     self.board[row][col] = player

    # def get_cell(self, row, col):
    #     return self.board[row][col]
    
    # [1, 2, 3]
    # [4, 5, 6]
    # [7, 8, 9]
    # 사용자가 입력이 편리하도록 위처럼 보여지는데 
    # 위치의 번호를 보드의 형식인 좌표(0, 1)값으로 바꿔 주고 결과를 리턴한다.
    def get_row_col(self, position):
        row = int(position / self.board_size) 
        col = int(position % self.board_size)
        return row, col

    def get_point(self):
        row, col = self.get_row_col(self.position)
        return [col, row]

    # 좌표의 위치에 player(1 또는 2)를 저장
    def set_cell(self, position):
        self.position = position
        self.total_count += 1
        row, col = self.get_row_col(self.position)
        self.player = 3 - self.player
        self.board[row][col] = self.player

    def set_zero(self, position):
        row, col = self.get_row_col(position)
        self.board[row][col] = 0
        self.total_count -= 1
        self.player = 3 - self.player

    # 좌표의 위치에 저장된 값(0, 1, 2 중 어떤)을 리턴해준다.
    def get_cell(self, position):
        row, col = self.get_row_col(position)
        return self.board[row][col]

    # 컴퓨터가 매번 빈 셀을 선택하도록 빈 셀만을 골라 리턴해준다.
    def get_empty_positions(self):
        # 보드의 빈 공간들을 저장할 리스트
        empty_positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 0:
                    empty_positions.append(row * self.board_size + col)
        return empty_positions

    # 행, 열 또는 두 대각선을 검사하여 같은 모양의 개수를 count하여 리턴
    def get_count(self, direction):
        count = 1 #처음 한 수를 둔 자리를 기준으로 검사
        point = self.get_point()
        for dir in direction: # ROW, COLUMN등 한 방향
            dx, dy = dir[0], dir[1] # LEFT(-1, 0) 등
            x, y  = point[0] + dx, point[1] + dy # 한 칸 이동한 값
            while True:
                # 보드의 범위를 벗어났나 검사
                if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
                    break
                # 같은 모양이 아니면 탈출
                elif self.board[y][x] != self.player:
                    break
                else:
                    count += 1 #같은 모양이면 count 증가하고
                    x, y = x + dx, y + dy # 또 한칸을 이동
        return count == self.board_size

    def get_cell_count(self):
        return self.total_count

    # 승리를 검사하는 함수
    def is_win(self):
        # 가로 세로 대각선 순으로 검사한다.
        directions = [ROW, COLUMN, DIAGONAL1, DIAGONAL2]
        for direction in directions:
            if self.get_count(direction):
                return True
        return False

    # 비겼나 검사하는 함수
    def is_draw(self):
        return self.total_count == 9

    def is_finish(self):
        return self.is_win() or self.is_draw()

    def get_result(self, player):
        if self.is_win():
            if self.player == player:
                return 2
            else:
                return 0
        else:
            return 1


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
        self.board.set_cell(position) # 보드에 저장
        self.display.mark_str_board(position + 1, player) # 화면에 보여질 보드에 저장
        # self.display.print_str_board() # 한 수 둔 결과를 보여줌
        return position

    # 승리를 검사하는 함수
    def is_win(self, player):
        # 가로 세로 대각선 순으로 검사한다.
        directions = [ROW, COLUMN, DIAGONAL1, DIAGONAL2]
        for direction in directions:
            if self.board.get_count(direction):
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
    def __init__(self, mcts):
        self.ID = 1
        self.mcts = mcts

    def action(self):
        position = self.mcts.mcts(self.board, 1500)
        return self.show_result(position, self.ID)
        # while True:
        #     position = self.display.input_data(self.ID)
        #     if self.board.get_cell(position) != 0:
        #         self.display.show_message()
        #     else:
        #         return self.show_result(position, self.ID)

class AI(Player):
    def __init__(self, mcts):
        self.mcts = mcts
        self.first = False
        self.ID = 2
        self.depth = 9
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
            self.minimax(self.depth, self.ID, -1000, 1000)
            position = self.get_best_position()
        # position = self.mcts.mcts(self.ID, 500)
        self.best_positions = []
        return self.show_result(position, self.ID)

    def minimax(self, depth, player, alpha, beta):
        if depth == 0 or self.is_finish(3 - player):
            return self.evaluation()

        positions = self.board.get_empty_positions()
        max_score = -100
        min_score = 100
        for position in positions:
            if player == self.ID:
                self.board.set_cell(position)
                score = self.minimax(depth - 1, 3 - self.ID, alpha, beta)
                self.board.set_zero(position)
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if depth == self.depth:
                    self.best_positions.append([position, max_score])
                if alpha >= beta:
                    break
            else:
                self.board.set_cell(position)
                score = self.minimax(depth - 1, self.ID, alpha, beta)
                self.board.set_zero(position)
                min_score = min(min_score, score)
                beta = min(beta, min_score)
                if alpha >= beta:
                    break

        if player == self.ID:
            return max_score
        else:
            return min_score

        # 참고사이트 : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

class Node:
    def __init__(self, position = None, parent = None, board = None):
        self.position = position
        self.parent = parent
        self.player = board.player
        self.score = 0
        self.visit_number = 0
        self.child = []
        self.empty_positions = board.get_empty_positions()

    def add_child(self, pos, bd):
        node = Node(pos, self, copy.deepcopy(bd))
        self.empty_positions.remove(pos)
        self.child.append(node)
        return node

    def get_max_uct_index(self, ucts):
        index = 0
        i = 0
        max = ucts[0]
        for uct in ucts[1:]:
            i += 1
            if max <= uct:
                index = i
                max = uct
        return index

    def get_uct_value(self):
        ucts = []
        for node in self.child:
            uct = node.score / node.visit_number + math.sqrt(1.1 * math.log(self.visit_number) / node.visit_number)
            ucts.append(uct)
        index = self.get_max_uct_index(ucts)
        return self.child[index]        

    def __lt__(self, other):
        return self.visit_number < other.visit_number

class Monte_carlo_tree_search:
    def __init__(self):
        self.board = None
        self.node = None

    def mcts(self, b, iterate_number):
        node = Node(board = copy.deepcopy(b))
        if len(node.empty_positions) == 1:
            return node.empty_positions[0]

        for _ in range(iterate_number):
            self.board = copy.deepcopy(b)
            self.node = node
            self.selection()
            result = self.simulation()
            self.update_node(result)

        # for n in node.child:
        #     print(n.position + 1, n.score, n.visit_number)
        return self.get_best_position(node)

    def get_best_position(self, node):
        node.child.sort()
        return node.child[-1].position
    
    def selection(self):
        while self.node.empty_positions == [] and self.node.child:
            self.node = self.node.get_uct_value()
            self.board.set_cell(self.node.position)

        if self.node.empty_positions:
            self.expansion()

    def expansion(self):
        if not self.board.is_finish():
            pos = random.choice(self.node.empty_positions)
            self.board.set_cell(pos)
            self.node = self.node.add_child(pos, self.board)

    def simulation(self):
        while not self.board.is_finish():
            self.board.set_cell(random.choice(self.board.get_empty_positions()))
        return self.board.get_result(self.node.player)

    def update_node(self, result):
        while self.node != None:
            self.node.score += result
            self.node.visit_number += 1
            self.node = self.node.parent
            # result = (result + 1) % 2
            if result == 2:
                result = 0
            elif result == 0:
                result = 2

# 게임을 관리하고 진행하는 클래스
class Tictactoe:
    # 이곳에서 모든 객체를 생성한다.
    def __init__(self):
        self.board = Board()
        self.display = Display()
        Player.board = self.board
        Player.display = self.display
        self.mcts = Monte_carlo_tree_search()
        self.user = User(self.mcts)
        self.computer = AI(self.mcts)
        self.player = [self.user, self.computer] # if문을 생략하기 위해서 list사용
        self.win_count = [0, 0, 0]

    def init_game(self):
        self.board.set_board()
        self.display.set_str_board()
        # self.display.print_str_board()

    def is_continue(self):
        return self.display.is_continue()

    # 게임이 끝이났나 검사
    def is_finish(self, player):
        if self.board.is_win():
            # self.display.show_message(player)
            self.win_count[player] += 1
        elif self.board.is_draw():
            # self.display.show_message(0)
            self.win_count[0] += 1
        else:
            return False
        return True

    # 실제로 게임이 진행되는 곳
    def play_game(self):
        # 게임이 시작되면 선을 가린다.
        player = random.choice(self.player)
        self.board.set_player(3 - player.ID)
        while True: # 게임이 끝날 때까지 계속 반복
            # 누구 차례인지 화면에 출력
            # player.show_order(player.ID)
            position = player.action()
            if self.is_finish(player.ID):
                break
            # 선수 교체(Turn을 바꿈)
            # 2 - 1(User)은 1(self.computer)이 되고, 
            # 2 - 2(AI)는 0(self.user)이 되어 turn이 바뀌게 된다.
            player = self.player[2 - player.ID]       


def main():
    # 게임을 관리하는 객체만 있으면 됨
    ttt = Tictactoe()
    start = datetime.datetime.now()
    for i in range(1000):
        ttt.init_game()
        ttt.play_game()
    end = datetime.datetime.now()
    print("Draw : {0}, Mcts win : {1}, alpha beta win : {2}".format(ttt.win_count[0], ttt.win_count[1], ttt.win_count[2]))
    print("elipsed time = ", end - start)
    # while True:
    #     # 게임이 시작되면 필요한 데이터를 초기화
    #     ttt.init_game()
    #     ttt.play_game()
    #     if not ttt.is_continue():
    #         break

if __name__ == "__main__":
    main()  