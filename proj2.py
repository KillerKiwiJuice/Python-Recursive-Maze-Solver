# File: proj2.py
# Author: Eoin Fitzpatrick
# Date: 11/30/16
# Section: 21
# E-mail: efitz1@umbc.edu
# Description:
# Solves mazes recursively
# Collaboration:
# Collaboration was not allowed on this assignment.

# convertMaze(list, list) Completely converts the loaded maze into a maze that can be read by humans. 
# 						At this point, I think this function is more magical than the recursive one.
# Input:   premature maze, maze loaded by program
# Output:  final converted maze list
def convertMaze(maze, temp):
	# set up lists
	right = []
	bottom =[]
	left =[]
	top = []
	# add every single side from each square in the maze to their corresponding lists
	for a in range(len(temp)):
		right.append(temp[a][0])
		bottom.append(temp[a][1])
		left.append(temp[a][2])
		top.append(temp[a][3])
	# split each list's contents into groups of four - the squares. Each list below now has lists containing 4 sides.
	right = [right[i:i+4] for i in range(0, len(right), 4)]
	bottom = [bottom[i:i+4] for i in range(0, len(bottom), 4)]
	left = [left[i:i+4] for i in range(0, len(left), 4)]
	top = [top[i:i+4] for i in range(0, len(top), 4)]

	# flatten list (remove extra brackets so it can be manipulated more easily)
	bottom = [side for squarePart in bottom for side in squarePart]
	# convert every element into a group of three elements (essentially triple the length)
	# but if the element is zero then keep the zero in the middle.
	# this is needed to line up the columns with the following 'combined' list's columns.
	bottom = [[1, 1, 1] if side == 1 else [1, 0, 1] for side in bottom]
	# flatten once more
	bottom = [side for squarePart in bottom for side in squarePart]
	# split contents into groups of however many columns there are in the maze
	bottom = [bottom[i:i+3*numColumns] for i in range(0, len(bottom), 3*numColumns)]

	# the following is exactly the same procedure done on the 'top' list
	top = [side for squarePart in top for side in squarePart]
	top = [[1, 1, 1] if side == 1 else [1, 0, 1] for side in top]
	top = [side for squarePart in top for side in squarePart]
	top = [top[i:i+3*numColumns] for i in range(0, len(top), 3*numColumns)]

	# merge each left element with a middle-ground zero then with the right element
	combined = [[left[i][a], 0, right[i][a]] for i in range(len(left)) for a in range(len(left[i]))]
	# flatten list
	combined = [side for squarePart in combined for side in squarePart]
	# split contents into groups of however many columns there are in the maze
	combined = [combined[i:i+3*numColumns] for i in range(0, len(combined), 3*numColumns)]

	# merge each sublist into the final maze. 
	for a in range(0, len(maze), 3):
		maze[a].extend(top[int(a/3)])
	for a in range(1, len(maze), 3):
		maze[a].extend(combined[int(a/3)])
	for a in range(2, len(maze), 3):
		maze[a].extend(bottom[int(a/3)])
	# mark ending square by converting the user input to input that the new maze can handle
	maze[((finishSquare[0] + 1) * 3) - 2][((finishSquare[1] + 1) * 3) - 2] = 4
	return maze

# printMaze(list) Prints the converted maze to the terminal
# Input:   converted maze
# Output:  none
def printMaze(maze):
	OPEN = 0
	WALL = 1
	VISITED = 2
	START = 3
	END = 4
	FINAL = 5
	SPACE = " "
	for a in range(len(maze)):
		for b in range(len(maze[a])):
			if maze[a][b] == OPEN:
				print(" " + SPACE, end='')
			elif maze[a][b] == WALL:
				# I have no idea if this special character will show up on other OS's.
				print(u"\u2588" + u"\u2588", end='')
			elif maze[a][b] == VISITED:
				print("." + SPACE, end='')
			elif maze[a][b] == START:
				print("S" + SPACE, end='')
			elif maze[a][b] == END:
				print("E" + SPACE, end='')
			elif maze[a][b] == FINAL:
				print("*" + SPACE, end='')
		print()

# readMaze(string) loads a maze and stores as a 2d list
# Input:   the filename string
# Output:  premature 2d list
def readMaze(filename):
	# global variables
	global numRows
	global numColumns
	global finishSquare
	file = open(filename, "r")
	# master holds ALL of the information
	master = []
	# temp is the temporary maze, which is converted to 3d later on
	temp = []
	# maze is the final maze that was converted to 3d
	maze = []
	# datalines is the number of lines to skip to append the squares
	DATALINES = 2
	# append all information to master
	for line in file:
		line = line.strip()
		master.append(line)
	# separate the first file line
	numRows, numColumns = master[0].split(" ")
	# convert to integer
	numRows = int(numRows)
	numColumns = int(numColumns)
	finishSquare = master[1].split()
	# convert the list elements to integers via list comprehension
	finishSquare = [int(a) for a in finishSquare]
	# create the temporary 2d maze
	for x in range(DATALINES, len(master)):
		temp.append(master[x])
	# convert all elements in the temporary maze to integers via list comprehension
	temp = [[int(number) for number in square.replace(" ", "")] for square in temp]
	# create the premature maze. This will be used later on in convertMaze()
	for a in range(numRows * 3):
		maze.append([])
	maze = convertMaze(maze, temp)
	return maze

# searchMaze(list, int, int) Recursive pathfinding algorithm. 
#  							 Recursively searches the converted maze, starting at the user-defined start point and finds the endpoint. 
# Input:   the filename string
# Output:  premature 2d list
def searchMaze(maze, row, column, dispMaze):
	# check for the endpoint
	if maze[row][column] == 4:
		print("Solution found!")
		dispMaze.append([row, column])
		return True
	# check for wall
	if maze[row][column] == 1:
		return False
	# check for previously visited path
	if maze[row][column] == 2:
		return False
	# mark as visited
	maze[row][column] = 2
	# search in every possible direction (north, east, south, west)
	# if the endpoint was found...
	if (row > 0 and searchMaze(maze, row - 1, column, dispMaze)) or (row != numRows * 3 - 2 and searchMaze(maze, row + 1, column, dispMaze)) \
			 or (column > 0 and searchMaze(maze, row, column - 1, dispMaze)) or (column != numColumns * 3 - 2 and searchMaze(maze, row, column + 1, dispMaze)):
		# don't overwrite the startpoint
		if maze[row][column] != 3:
			maze[row][column] = 5
		# add the solution indices 
		dispMaze.append([row, column])
		# return tuple
		return (maze, dispMaze)
	else:
		return False

# displayCorrectPath(list) prints the final path to the endpoint
# Input:   recursively-output list with the ordered solution indices
# Output:  none
def displayCorrectPath(dispMaze):
	print("Legend: \n  '*' = Final path\n  '.' = Complete path\n  'S' = Start point\n  'E' = End point")
	# this loop prints every third element in order to match the original maze output in the instructions.
	for a in range(len(dispMaze) - 1, 1, -3):
		# converts the index back down to the index used by the original maze (before loading)
		print("(" + str(int(((dispMaze[a][0] - 1) / 3) + 1)) + ", " + str(int(((dispMaze[a][1] - 1) / 3) + 1)) + ")")
	# print final endpoint, because it wasn't added in the recursion function
	print("(" + str(finishSquare[0] + 1) + ", " + str(finishSquare[1] + 1) + ")")

def main():
	dispMaze = []
	print("Welcome to Maze Solver 2000")
	filename = input("Please enter the filename of the maze: ")
	maze = readMaze(filename)
	printMaze(maze)
	# I am aware that the instructions' output starts at zero, but usually it is converted to "real world" input
	# AKA starts at 1
	row = int(input("Please enter the starting row (1 to " + str(numRows) + ", inclusive): "))
	# input validation
	while row < 1 or row > numRows:
		print("Invalid input! ")
		row = int(input("Please enter the starting row (1 to " + str(numRows) + ", inclusive): "))
	column = int(input("Please enter the starting column (1 to " + str(numColumns) + ", inclusive): "))
	while column < 1 or column > numColumns or (row == finishSquare[0] + 1 and column == finishSquare[1] + 1):
		if row == finishSquare[0] + 1 and column == finishSquare[1] + 1:
			print("The start point can't equal the end point!")
			column = int(input("Please enter the starting column (1 to " + str(numColumns) + ", inclusive): "))
		else:
			print("Invalid input!")
			column = int(input("Please enter the starting column (1 to " + str(numColumns) + ", inclusive): "))
	# convert user input to input that the converted maze can handle
	convertedRow = ((row) * 3) - 2
	convertedColumn = ((column) * 3) - 2
	# mark as starting index
	maze[convertedRow][convertedColumn] = 3
	output = searchMaze(maze, convertedRow, convertedColumn, dispMaze)
	if output != False:
		# mark starting point again, as it got overwritten
		output[0][convertedRow][convertedColumn] = 3
		printMaze(output[0])
		displayCorrectPath(output[1])
	else:
		print("Dead End! Pathfinding cannot escape.")
	print("Thanks for using Maze Solver 2000.")

main()
