#!/usr/bin/env python
#coding:utf-8

import numpy as np
import time
import sys

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
# =============================================================================
#  
#  ROW = "ABCDEFGHI"
#  COL = "123456789"
#  
# =============================================================================

# =============================================================================
# def print_board(board):
#     """Helper function to print board in a square."""
#     print("-----------------")
#     for i in ROW:
#         row = ''
#         for j in COL:
#             row += (str(board[i + j]) + " ")
#         print(row)
#  
# def board_to_string(board):
#     """Helper function to convert board dictionary to string for writing."""
#     ordered_vals = []
#     for r in ROW:
#         for c in COL:
#             ordered_vals.append(str(board[r + c]))
#     return ''.join(ordered_vals)
# 
# =============================================================================
ALL_DOMAINS={1,2,3,4,5,6,7,8,9}
#failure_board={}
 
def board_to_string(twod_config_board):
    
    twod_config_board=twod_config_board.reshape(1,81).tolist()
# =============================================================================
#     ordered_vals = []
#     for i in range(len(twod_config_board)):
#         ordered_vals.append(str(twod_config_board[i]))
#     print(''.join(ordered_vals))
#     return ''.join(ordered_vals)
# 
# =============================================================================
    return (' '.join([str(elem) for elem in twod_config_board])).replace(',','').replace(' ','').replace('[','').replace(']','')


def twod_config(line):
    return np.array([int(l) for l in line]).reshape((9,9))

def operate_value_to_assignment(unassigned_var,domain_value,assignment,operation):
    row,col=unassigned_var
    if(operation=="add"):
        assignment[row][col] = domain_value
    else:
        assignment[row][col] = 0
    return assignment

def is_solved(board):
    if np.all(board):
        return True
    else:
        return False    
    
def get_each_variable_domain(position,twod_config_board):
    x,y=position
    row_values,col_values=get_same_row_values(x,twod_config_board),get_same_col_values(y,twod_config_board)
    tile_values=get_same_tile_values(x,y,twod_config_board)
    return ALL_DOMAINS.difference(row_values).difference(col_values).difference(tile_values)

def get_same_row_values(x,twod_config_board):
    return set(twod_config_board[x,:].flat)

def get_same_col_values(y,twod_config_board):
    return set(twod_config_board[:,y].flat)
     
def get_same_tile_values(x,y,twod_config_board):
    tiles= [slice(0,3),slice(3,6),slice(6,9)]
    return set(twod_config_board[tiles[int(x/3)], tiles[int(y/3)]].reshape(1,9).flat)
    
def get_all_unassigned_variables(twod_config_board):
    unassigned_variables=[]
    list_unassigned_variables=np.where(twod_config_board==0)
    for unassigned in np.transpose(list_unassigned_variables):
        temp=tuple(unassigned)
        unassigned_variables.append(temp)
    return unassigned_variables    

def select_unassigned_variable(twod_config_board):
    min_domain={1,2,3,4,5,6,7,8,9}
    all_domains_unassigned_dict={}
    min_key=(0,0)
    all_unassigned_variables = get_all_unassigned_variables(twod_config_board)
    for all_unassigned_variable in all_unassigned_variables:
        temp_domain=get_each_variable_domain(all_unassigned_variable,twod_config_board)
        all_domains_unassigned_dict[all_unassigned_variable] = temp_domain
        if(len(min_domain)>len(temp_domain)):
             min_domain=temp_domain
             min_key=all_unassigned_variable
    return  min_key,min_domain,all_domains_unassigned_dict     

def backtracking(line):
    return backtrack(twod_config(line))

def backtrack(twod_config_board):
    """Takes a board and returns solved board."""
    assignment= twod_config_board
    if(is_solved(assignment)):
        return assignment
    unassigned_var,domain_values,all_domains_unassigned_dict = select_unassigned_variable(twod_config_board)
# =============================================================================
#      for domain_value in domain_values:
#         if(is_consistent(unassigned_var,domain_value,all_domains_unassigned_dict,assignment,twod_config_board)):
#              assignment=operate_value_to_assignment(unassigned_var,domain_value,assignment,"add")
#         else:
#              print("inconsistent")
#              value=set()
#              value.add(domain_value)
#              #print(all_domains_unassigned_dict[unassigned_var])
#              #print(all_domains_unassigned_dict[unassigned_var].difference(value))
#              all_domains_unassigned_dict[unassigned_var]=all_domains_unassigned_dict[unassigned_var].difference(value)
#              print(all_domains_unassigned_dict[unassigned_var])
#              print("\n")
#         result=backtrack(assignment)
#         if np.all(result):
#             return result
#         assignment=operate_value_to_assignment(unassigned_var,domain_value,assignment,"remove")
#     return assignment     
# =============================================================================
    for domain_value in domain_values:
        assignment=operate_value_to_assignment(unassigned_var,domain_value,assignment,"add")
        result=backtrack(assignment)
        if np.all(result):
            return result
        assignment=operate_value_to_assignment(unassigned_var,domain_value,assignment,"remove")
    return assignment       
  
def is_consistent(unassigned_var,domain_value,all_domains_unassigned_dict,assignment,twod_config_board):
    #print(list(all_domains_unassigned_dict.values()))
    value1=set()
    value1.add(domain_value)
    row,col=unassigned_var
    row_col_check=[None]*9
    for i in range(len(row_col_check)):
        if(i!=col):
            pos=(row,i)
            if(all_domains_unassigned_dict.get(pos) is not None):
                if(len(set(list(all_domains_unassigned_dict[pos])).difference(value1))==0):
                    return False
                
    for j in range(len(row_col_check)):
        if(j!=row):
            pos=(j,col)
            if(all_domains_unassigned_dict.get(pos) is not None):
                if(len(set(list(all_domains_unassigned_dict[pos])).difference(value1))==0):
                    return False    
    return True        


# =============================================================================
# if __name__ == '__main__':
#     #  Read boards from source.
#     src_filename = 'sudokus_start.txt'
#     i=0
#     try:
#         srcfile = open(src_filename, "r")
#         sudoku_list = srcfile.read()
#     except:
#         print("Error reading the sudoku file %s" % src_filename)
#         exit()
# 
#     # Setup output file
#     out_filename = 'output.txt'
#     outfile = open(out_filename, "w")
#     start_time=time.time()
# 
#     # Solve each board using backtracking
#     for line in sudoku_list.split("\n"):
# 
#         if len(line) < 9:
#             continue
# # =============================================================================
# # 
# #         # Parse boards to dict representation, scanning board L to R, Up to Down
# #         board = { ROW[r] + COL[c]: int(line[9*r+c])
# #                   for r in range(9) for c in range(9)}
# # 
# #         # Print starting board. TODO: Comment this out when timing runs.
# #         print_board(board)
# # 
# #         # Solve with backtracking
# #         solved_board = backtracking(board)
# # 
# # =============================================================================
#         # Print solved board. TODO: Comment this out when timing runs.
#         solved_board = backtracking(line)
#         if(len(solved_board)!=0):
#              outfile.write(board_to_string(solved_board))
#              outfile.write('\n')
# # =============================================================================
#     end_time = time.time()
#     print("Program completed in %.3f second(s)"%(end_time-start_time))
#     
#     
# =============================================================================
if __name__ == '__main__':
    #  Read boards from cmdpmt.
    line = sys.argv[1]
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    start_time=time.time()    
# =============================================================================
# 
#         # Parse boards to dict representation, scanning board L to R, Up to Down
#         board = { ROW[r] + COL[c]: int(line[9*r+c])
#                   for r in range(9) for c in range(9)}
# 
#         # Print starting board. TODO: Comment this out when timing runs.
#         print_board(board)
# 
#         # Solve with backtracking
#         solved_board = backtracking(board)
# 
# =============================================================================
          # Solve each board using backtracking
    if len(line)== 81:
          solved_board = backtracking(line)
    if(len(solved_board)!=0):
          outfile.write(board_to_string(solved_board))
    outfile.close()     
# =============================================================================
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))
        