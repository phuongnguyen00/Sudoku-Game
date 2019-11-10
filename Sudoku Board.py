import copy
import time

class SudokuState:
    def __init__(self):

        self.size = 9
        self.num_placed = 0
        #number of valid numbers that have been put on the board
        self.board = []
     
        for r in range (self.size):
            row = []
            for c in range(self.size):
                row.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.board.append(row)
            
    def is_filled(self, row, column):
        return isinstance(self.board[row][column],int)
    
    def remove_conflict(self, row, column, number):
        if not(self.is_filled(row, column)):
            self[row][column].remove(number)
    
    def get_subgrid_number(self, row, col):
        """
        Returns a number between 1 and 9 representing the subgrid
        that this row, col is in.  The top left subgrid is 1, then
        2 to the right, then 3 in the upper right, etc.
        """
        row_q = int(row/3)
        col_q = int(col/3)
        return row_q * 3 + col_q + 1
    
    def remove_all_conflicts(self, row, column, number):
        #This method is called after number has been placed at entry row, col
        
        for r in range (self.size): #updating the column
            if not (self.is_filled(r, column)):
                if number in self.board[r][column]:
                    self.board[r][column].remove(number)
        
        for c in range (self.size): #updating the row
            if not(self.is_filled(row, c)):
                if number in self.board[row][c]:
                    self.board[row][c].remove(number)
                
        num_subgrid = self.get_subgrid_number(row, column)
        
        #iterate through the whole board to check the subgrid
        for r in range (self.size):
            for c in range (self.size):
                if self.get_subgrid_number(r, c) == num_subgrid:
                    if not (self.is_filled(r, c)):
                        if number in self.board[r][c]:
                            self.board[r][c].remove(number)   
                        
    def add_number(self, row, column, number):
        #Return a new state
        new_state = copy.deepcopy(self)
        
        new_state.board[row][column] = number
        
        new_state.remove_all_conflicts(row, column, number)
        
        new_state.num_placed += 1
        
        return new_state
    
    def get_most_constrained_cell(self):
        #Heuristic function
        length = self.size
        min_row = 0
        min_col = 0      
        
        for r in range (self.size):
            for c in range (self.size):
                if not (self.is_filled(r, c)):
                    if len(self.board[r][c]) < length:
                        length = len(self.board[r][c])
                        min_row = r
                        min_col = c
                        
        return (min_row, min_col)
    
    def solution_is_possible(self):
        #Return False if there is at least one entry without any possible 
        #values it can take
        for entry in self.board:
            if entry == []:
                return False
        
        return True 
    
    def next_states(self):
        possible_next_states = []
        
        (cell_r, cell_c) = self.get_most_constrained_cell()
        cell = self.board[cell_r][cell_c]
        #cell is a list
        
        for i in range (len(cell)):
            if self.add_number(cell_r, cell_c, cell[i]).solution_is_possible():
                possible_next_states.\
                append(self.add_number(cell_r, cell_c, cell[i]))
        
        return possible_next_states
    
    def is_goal(self):
        return self.num_placed == 81
            
    def get_any_available_cell(self):
        """
        An uninformed cell finding variant.  If you use
        this instead of find_most_constrained_cell
        the search will perform a depth first search.
        """
        for r in range(self.size):
            for c in range(self.size):
                if not self.is_filled(r,c):                    
                    return (r, c)
    
    def get_raw_string(self):
        board_str = ""
  
        for r in self.board:
            board_str += str(r) + "\n"
      
        return "num placed: " + str(self.num_placed) + "\n" + board_str
      
    def __str__(self):
        """
        prints all numbers assigned to cells.  Unassigned cells (i.e.
        those with a list of options remaining are printed as blanks
        """
        board_string = ""
        
        for r in range(self.size):
            if r % 3 == 0:
                board_string += " " + "-" * (self.size * 2 + 5) + "\n"
      
            for c in range(self.size):
                entry = self.board[r][c]
        
                if c % 3 == 0:
                    board_string += "| "    
            
                if isinstance(entry, list):
                    board_string += "_ "
                else:
                    board_string += str(entry) + " "
                
            board_string += "|\n"
      
        board_string += " " + "-" * (self.size * 2 + 5) + "\n" 
        
        return "num placed: " + str(self.num_placed) + "\n" + board_string    


# -----------------------------------------------------------------------
# Make all of your changes to the SudokuState class above.
# only when you're running the last experiments will
# you need to change anything below here and then only
# the different problem inputs

# -----------------------------------
# Even though this is the same DFS code
# that we used last time, our next_states
# function is makeing an "informed" decision
# so this algorithm performs similarly to
# best first search.
def dfs(state):
    """
    Recursive depth first search implementation
  
    Input:
    Takes as input a state.  The state class MUST have the following
    methods implemented:
    - is_goal(): returns True if the state is a goal state, False otherwise
    - next_states(): returns a list of the VALID states that can be
    reached from the current state
    
    Output:
    Returns a list of ALL states that are solutions (i.e. is_goal
    returned True) that can be reached from the input state.
    """    
    #if the current state is a goal state, then return it in a list
    if state.is_goal():
        return [state]
    else:
        #make a list to accumulate the solutions in
        result = []
  
        for s in state.next_states():
            result += dfs(s)
      
        return result

# ------------------------------------
# three different board configurations:
# - problem1
# - problem2
# - heart (example from class notes)
def problem1():
    b = SudokuState()
    b = b.add_number(0, 1, 7)
    b = b.add_number(0, 7, 1)
    b = b.add_number(1, 2, 9)
    b = b.add_number(1, 3, 7)
    b = b.add_number(1, 5, 4)
    b = b.add_number(1, 6, 2)
    b = b.add_number(2, 2, 8)
    b = b.add_number(2, 3, 9)
    b = b.add_number(2, 6, 3)
    b = b.add_number(3, 1, 4)
    b = b.add_number(3, 2, 3)
    b = b.add_number(3, 4, 6)
    b = b.add_number(4, 1, 9)
    b = b.add_number(4, 3, 1)
    b = b.add_number(4, 5, 8)
    b = b.add_number(4, 7, 7)
    b = b.add_number(5, 4, 2)
    b = b.add_number(5, 6, 1)
    b = b.add_number(5, 7, 5)
    b = b.add_number(6, 2, 4)
    b = b.add_number(6, 5, 5)
    b = b.add_number(6, 6, 7)
    b = b.add_number(7, 2, 7)
    b = b.add_number(7, 3, 4)
    b = b.add_number(7, 5, 1)
    b = b.add_number(7, 6, 9)
    b = b.add_number(8, 1, 3)
    b = b.add_number(8, 7, 8)
    return b
    
def problem2():
    b = SudokuState()
    b = b.add_number(0, 1, 2) 
    b = b.add_number(0, 3, 3) 
    b = b.add_number(0, 5, 5)
    b = b.add_number(0, 7, 4)
    b = b.add_number(1, 6, 9)
    b = b.add_number(2, 1, 7)
    b = b.add_number(2, 4, 4)
    b = b.add_number(2, 7, 8)
    b = b.add_number(3, 0, 1)
    b = b.add_number(3, 2, 7)
    b = b.add_number(3, 5, 9)
    b = b.add_number(3, 8, 2)
    b = b.add_number(4, 1, 9)
    b = b.add_number(4, 4, 3)
    b = b.add_number(4, 7, 6)
    b = b.add_number(5, 0, 6)
    b = b.add_number(5, 3, 7)
    b = b.add_number(5, 6, 5)
    b = b.add_number(5, 8, 8)
    b = b.add_number(6, 1, 1)
    b = b.add_number(6, 4, 9)
    b = b.add_number(6, 7, 2)
    b = b.add_number(7, 2, 6)
    b = b.add_number(8, 1, 4)
    b = b.add_number(8, 3, 8)
    b = b.add_number(8, 5, 7)
    b = b.add_number(8, 7, 5)
    return b

def heart():
    b = SudokuState()
    b = b.add_number(1, 1, 4)
    b = b.add_number(1, 2, 3)
    b = b.add_number(1, 6, 6)
    b = b.add_number(1, 7, 7)
    b = b.add_number(2, 0, 5)
    b = b.add_number(2, 3, 4)
    b = b.add_number(2, 5, 2)
    b = b.add_number(2, 8, 8)
    b = b.add_number(3, 0, 8)
    b = b.add_number(3, 4, 6)
    b = b.add_number(3, 8, 1)
    b = b.add_number(4, 0, 2)
    b = b.add_number(4, 8, 5)
    b = b.add_number(5, 1, 5)
    b = b.add_number(5, 7, 4)
    b = b.add_number(6, 2, 6)
    b = b.add_number(6, 6, 7)
    b = b.add_number(7, 3, 5)
    b = b.add_number(7, 5, 1)
    b = b.add_number(8, 4, 8)
    return b


# --------------------------------
# Code that actual runs a sudoku problem, times it
# and prints out the solution.
# You can vary which problem your running on between 
# problem1(), problem2() and heart() by changing the line
# below
#
# Uncomment this code when you have everything implemented and you
# want to solve some of the sample problems!

problem = problem1()
print("Starting board:")
print(problem)

start_time = time.time()
solutions = dfs(problem)
search_time = time.time()-start_time

print("Search took " + str(round(search_time, 2)) + " seconds")
print("There was " + str(len(solutions)) + " solution.\n\n")
if len(solutions) > 0:
    print(solutions[0])
    
