import gym
from gym import spaces
import numpy as np

def get_sudoku_board(board_size=9):
    """
    Return a Sudoku board of the specified size.
    """
    board = np.zeros((board_size, board_size), dtype=np.int)
    for i in range(board_size):
        for j in range(board_size):
            board[i, j] = i * board_size + j + 1
    return board

def check_sudoku_board(board):
    """
    Check if the Sudoku board is valid.
    """
    board_size = board.shape[0]
    for i in range(board_size):
        for j in range(board_size):
            if board[i, j] != 0:
                if not check_sudoku_row(board, i, j):
                    return False
                if not check_sudoku_column(board, i, j):
                    return False
                if not check_sudoku_block(board, i, j):
                    return False
    return True

def check_sudoku_row(board, row, col):
    """
    Check if the Sudoku board is valid.
    """
    board_size = board.shape[0]
    gt = set(range(1, board_size + 1))
    r = set(board[row,:])
    if r != gt:
        return False
    return True

def check_sudoku_column(board, row, col):
    """
    Check if the Sudoku board is valid.
    """
    board_size = board.shape[0]
    gt = set(range(1, board_size + 1))
    r = set(board[:,col])
    if r != gt:
        return False
    return True

def check_sudoku_block(board, row, col):
    """
    Check if the Sudoku board is valid.
    """
    board_size = board.shape[0]
    block_size = int(np.sqrt(board_size))
    row_start = row - row % block_size
    col_start = col - col % block_size

    gt = set(range(1, board_size + 1))
    r = set(board[row_start:(row_start+block_size),col_start:(col_start+block_size)])
    if r != gt:
        return False
    return True

def is_valid_action(action, board):
    # if board[action[0],action[1]] ==0:
    #     return False
    if action[2] in board[action[0],:]:
        return False
    if action[2] in board[:,action[1]]:
        return False
    if action[2] in board[action[0]//3*3:(action[0]//3*3+3),action[1]//3*3:(action[1]//3*3+3)]:
        return False
    return True

class SudokuEnv(gym.Env):
    FILLED_ERROR_REWARD = -10
    VALID_STEP_REWARD = 0
    SUCCESS_REWARD = 10
    def __init__(self) -> None:
        super().__init__()
        # self.observation_space = spaces.MultiDiscrete([10]*81)
        self.action_space =spaces.MultiDiscrete([9,9,9]) # [ROW,COL,VAL]
        self.seed()
    def step(self, action):
        done = False
        info = {}
        reward = 0
        
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        # assert self.board[action[0],action[1]] ==0, f"({action[0]},{action[1]}) is already filled"
        if not is_valid_action(action, self.board):
            reward = SudokuEnv.FILLED_ERROR_REWARD
            return self.board, reward, done, info
        
        # update
        self.board[action[0],action[1]] = action[2]
        # check
        if check_sudoku_board(self.board):
            done = True
            reward = SudokuEnv.SUCCESS_REWARD
        else:
            reward = SudokuEnv.VALID_STEP_REWARD
            

        return self.board, reward, done, info
    def reset(self):
        self.board = np.random.randint(0,10,9*9).reshape((9,9))
        # row
        for r in range(9):
            vals=[]
            for c in range(9):
                if self.board[r,c] != 0:
                    if self.board[r,c] not in vals:
                        vals.append(self.board[r,c])
                    else:
                        print(f"{r},{c} is duplicated")
                        self.board[r,c] = 0
        # col
        for c in range(9):
            vals=[]
            for r in range(9):
                if self.board[r,c] != 0:
                    if self.board[r,c] not in vals:
                        vals.append(self.board[r,c])
                    else:
                        print(f"{r},{c} is duplicated")
                        self.board[r,c] = 0
        # block
        for r in range(0,9,3):
            for c in range(0,9,3):
                vals=[]
                for i in range(3):
                    for j in range(3):
                        if self.board[r+i,c+j] != 0:
                            if self.board[r+i,c+j] not in vals:
                                vals.append(self.board[r+i,c+j])
                            else:
                                print(f"{r+i},{c+j} is duplicated")
                                self.board[r+i,c+j] = 0
        return self.board
    def render(self, mode="human"):
        for r in range(9):
            if r%3==0:
                print("---------------------")
            for c in range(9):
                if c%3==0:
                    print("|", end="")
                print(self.board[r,c], end=" ")
                
            print("|\n")
        print("---------------------")
            
        pass
    

def test_sudokuEnv():
    env = SudokuEnv()
    env.reset()
    print('Initial board:')
    env.render()
    actions = []
    rewards= []
    for i in range(100):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        actions.append(action)
        rewards.append(reward)
        if reward == SudokuEnv.SUCCESS_REWARD:
            break
        if reward == SudokuEnv.VALID_STEP_REWARD:
            env.render()
            print(i, action, reward)
    print('final board:')
    env.render()
    # print(actions)
    print(rewards)
    pass


if __name__ == '__main__':
    test_sudokuEnv()