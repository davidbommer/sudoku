import random 
import numpy as np
import copy
import string
import time



class Game():
	def __init__(self):
		self.board = np.zeros((9,9), dtype=int)

	#This method helps to create the Sudoku board. Note that I break down the board into sections below.
	#And note that sections 1,5,9 are independent from one another, making them the easiest to fill. 
	def diag_generate(self, left, right):
		section = []
		for row in range(left, right):
			for col in range(left,right):
				r = list(range(1,10))
				random.shuffle(r)
				for val in r:
					if val not in section:
						section.append(val)
						self.board[row][col] = val
						break



#	1   2   3

#   4   5   6

#   7   8   9
#sections 1, 5, 9 are filled in diag_generate, the rest are filled in fill_box


	#this method fills the section with numbers following the rules of Sudoku 
	def fill_box(self, section):
		if section == 2:
			rowLeft = 0
			rowRight = 3
			colLeft = 3
			colRight = 6
		elif section == 3:
			rowLeft = 0
			rowRight = 3
			colLeft = 6
			colRight = 9
		elif section == 6:
			rowLeft = 3
			rowRight = 6
			colLeft = 6
			colRight = 9
		elif section == 4:
			rowLeft = 3
			rowRight = 6
			colLeft = 0
			colRight = 3
		elif section == 7:
			rowLeft = 6
			rowRight = 9
			colLeft = 0
			colRight = 3
		elif section == 8:
			rowLeft = 6
			rowRight = 9
			colLeft = 3
			colRight = 6

		
		square = []
		for row in range(rowLeft, rowRight):
			for col in range(colLeft, colRight):
				r = list(range(1,10))
				random.shuffle(r)
				column = []
				for i in range(9):
					column.append(self.board[i][col])
				for val in r:
					if val not in square and val not in self.board[row] and val not in column:
						self.board[row][col] = val
						square.append(val)
						break

	def check_box(self):
		for row in range(9):
			for col in range(9):
				if self.board[row][col] < 1 or self.board[row][col] > 9:
					return False
		return True 


	#theres is a chance that the randomely generated board will have some discrepencies. 
	#so we will keep generating a board until a proper board is made 
	def generate_board(self):

		while not self.check_box():
			self.board = np.zeros((9,9), dtype=int)
			self.diag_generate(0,3)
			self.diag_generate(3,6)
			self.diag_generate(6,9)
			self.fill_box(2)
			self.fill_box(3)
			self.fill_box(6)
			self.fill_box(4)
			self.fill_box(7)
			self.fill_box(8)
		

	def make_blanks(self):
		num = 40
		while num > 0:
			row = random.randint(0, 8)
			col = random.randint(0, 8)
			while self.board[row][col] == 0:
				row = random.randint(0, 8)
				col = random.randint(0, 8)
			backup = self.board[row][col]
			self.board[row][col] = 0
			boardCopy = copy.copy(self.board)
			if not self.solve_sudoku(boardCopy):
				self.board[row][col] = backup
				continue 
			num -= 1 
		return self.board

	
	def print_board(self, arr=None):
		if arr is None:
			print (arr)
			return arr
		print(self.board)
		return self.board 



	def find_empty_location(self, l, arr): 
	    for row in range(9): 
	        for col in range(9): 
	            if(arr[row][col]==0): 
	                l[0]=row 
	                l[1]=col 
	                return True
	    return False


	def check_location_is_safe(self, row, col, num, arr):
		if num in self.board[row]:
			return False
		for i in range(9):
			if num == arr[row][i]:
				return False 
		squareRow = row - (row % 3)
		squareCol = col - (col % 3)
		for i in range(3):
			for j in range(3):
				if arr[i+squareRow][j+squareCol] == num:
					return False
		return True



	# Takes a partially filled-in grid and attempts to assign values to 
	# all unassigned locations in such a way to meet the requirements 
	# for Sudoku solution (non-duplication across rows, columns, and boxes) 
	def solve_sudoku(self, arr): 
	    # 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
	    l=[0,0] 
	      
	    # If there is no unassigned location, we are done     
	    if(not self.find_empty_location(l, arr)): 
	        return True
	      
	    # Assigning list values to row and col that we got from the above Function  
	    row=l[0] 
	    col=l[1] 
	      
	    # consider digits 1 to 9 
	    for num in range(1,10): 
	          
	        # if looks promising 
	        if(self.check_location_is_safe(row,col,num, arr)): 
	              
	            # make tentative assignment 
	            arr[row][col]=num 
	  
	            # return, if success
	            if(self.solve_sudoku(arr)): 
	                return True
	  
	            # failure, unmake & try again 
	            arr[row][col] = 0
	              
	    # this triggers backtracking         
	    return False 




if __name__ == "__main__":
	print("Here is a randomly generated sudoku board:")
	game = Game()
	game.generate_board()
	board = game.make_blanks()
	game.print_board(board)
	response = input("Think you can solve it faster than my program? (type yes/no): ")
	if response.lower().translate(str.maketrans('','',string.punctuation)) == 'yes':
		print ("You're wrong, but I respect your confidence.")
	elif response.lower().translate(str.maketrans('','',string.punctuation)) == 'no':
		print ("I respect your honesty.")
	else:
		count = 0
		while response.lower().translate(str.maketrans('','',string.punctuation)) != 'yes' or response.lower().translate(str.maketrans('','',string.punctuation)) == 'no':
			if count == 5:
				print('wow... moving on.')
				break
			response = input("Just type 'yes' or 'no' and lets get this over with: ")
			count += 1

	time.sleep(1)
	print ('ready, set, solve!')
	time.sleep(1)
	game.solve_sudoku(board)
	game.print_board(board)
	print('beat you.')


