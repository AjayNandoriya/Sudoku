import numpy as np
import os
import sys
if __package__ is None or __package__ == '':
    BASE_PATH = os.path.join(os.path.dirname(__file__), '..','..','..')
    sys.path.append(BASE_PATH) 
from sudoku.scripts.env.sudoku import SudokuEnv, calc_possible_cells, check_sub_row, check_sub_col

def check_action(possisble_cells, board, action):
    """
    Check if the action is valid."""
    if possisble_cells[action[0],action[1], action[2]-1] == False:
        return False

    
    new_stat = np.copy(possisble_cells)
    new_stat[action[0],:,action[2]-1] = False
    new_stat[:,action[1],action[2]-1] = False
    new_stat[action[0]//3*3:(action[0]//3*3+3),action[1]//3*3:(action[1]//3*3+3),action[2]-1] = False
    new_board = np.copy(board)
    new_board[action[0],action[1]] = action[2]
    for i in range(3):
        
        min_sub_row = np.sum(new_board[action[0], i*3:(i+1)*3] == 0)
        min_sub_col = np.sum(new_board[i*3:(i+1)*3, action[1]] == 0)
        sub_row = np.any(new_stat[action[0], i*3:i*3+3, :], axis=0)
        sub_col = np.any(new_stat[i*3:i*3+3, action[1], :], axis=0)
        if np.sum(sub_row)< min_sub_row or np.sum(sub_col)< min_sub_col:
            return False
    return True
    

def calc_action(board:np.ndarray)->np.ndarray:
    """
    Calculate the next action to take."""

    N = 9
    # calc row sets
    FULL_SET = set(range(1, N+1))
    cell_sets = [[set()]*N]*N
    row_sets = [set()]*N
    col_sets = [set()]*N
    block_sets = [set()]*N
    # calc cell sets
    for i in range(N):
        for j in range(N):
            cell_sets[i][j] = FULL_SET - set([board[i][j]])
    # calc row sets
    for i in range(N):
        row_sets[i] = set(board[i,:])-set([0])
        col_sets[i] = set(board[:,i])-set([0])
        block_sets[i] = set(board[i//3*3:i//3*3+3,i%3*3:i%3*3+3].flatten())-set([0])
    # find all empty cells
    empty_cells = np.argwhere(board == 0)
    # find all possible values for each empty cell

    possible_cells = calc_possible_cells(board)

    single_actions = []
    possible_actions = []
    for empty_cell in empty_cells:
        row_set = row_sets[empty_cell[0]]
        col_set = col_sets[empty_cell[1]]
        block_set = block_sets[empty_cell[0]//3*3+empty_cell[1]//3]
        possible_values = set(range(1,N+1))-row_set-col_set-block_set
        # if there is only one possible value, set it
        if len(possible_values) == 1:
            single_actions.append([empty_cell[0],empty_cell[1],list(possible_values)[0]])
        if len(possible_values)>0:
            possible_actions +=[[empty_cell[0],empty_cell[1],v] for v in list(possible_values)]
        else:
            pass
    if len(single_actions)>0:
        return np.array(single_actions[0])

    valid_actions = [] 
    possisble_cells = calc_possible_cells(board)
    for action in possible_actions:
        if check_action(possisble_cells, board, action):
            valid_actions.append(action)
    if len(valid_actions)>0:
        return np.array(valid_actions[0])
    return None


def test_traditional_agent():

    env = SudokuEnv()
    for i_episode in range(1):
        observation = env.reset()
        for t in range(100):
            env.render()
            # print(observation)
            action = env.action_space.sample()
            action = calc_action(observation)
            observation, reward, done, info = env.step(action)
            print(t, action, reward, done)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    env.close()

if __name__ == "__main__":
    test_traditional_agent()