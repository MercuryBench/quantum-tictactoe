import random

# Huge parts of this code are stolen from Al Sweigart's sample code for Tic Tac Toe implementation on
# https://inventwithpython.com/chapter10.html

"""
Preliminary Marks (e.g. the two instances of "cross1" are called premarks, final marks (obtained after collaps) are called finmarks.

"""

class Board:
	def __init__(self): # Initialize Board with list of empty fields
		self.fields = [Field(n) for n in range(10)] # ignore index 0
		
	def copy(self): # make a (non-referential) copy of a board
		b = Board()
		b.fields = [f.copy() for f in self.fields]
		return b
	
	def addPreMark(self, letter, num, pos1, pos2): # add a premark with letter in {X,O} with its specific number at positions 1 and 2
		self.fields[pos1].addPreMark(PreMark(letter, num, pos1, pos2))
		m = PreMark(letter, num, pos2, pos1)
		self.fields[pos2].addPreMark(m)
		return m
	
	def addFinMark(self, letter, pos, num): # add a finmark with letter in {X, O} at position pos
		self.fields[pos].addFinMark(FinMark(letter, pos, num))
		
	def hasWon(self, letter): # check whether the letter (in {X, O}) has won the game and return the lowest max subscript (see wikipedia rules for quantum TTT)
		bo, nb = self.realBoard()
		le = letter
		ttt = [False for n in range(8)]
		maxind = [0 for n in range(8)]
		ttt[0] 		= (bo[7] == le and bo[8] == le and bo[9] == le) # across the top
		maxind[0]	= max(nb[7], nb[8], nb[9])
		ttt[1] 		= (bo[4] == le and bo[5] == le and bo[6] == le) # across the middle
		maxind[1]	= max(nb[4], nb[5], nb[6])
		ttt[2] 		= (bo[1] == le and bo[2] == le and bo[3] == le) # across the bottom
		maxind[2]	= max(nb[1], nb[2], nb[3])
		ttt[3] 		= (bo[7] == le and bo[4] == le and bo[1] == le) # down the left side
		maxind[3]	= max(nb[7], nb[4], nb[1])
		ttt[4] 		= (bo[8] == le and bo[5] == le and bo[2] == le) # down the middle
		maxind[4]	= max(nb[8], nb[5], nb[2])
		ttt[5] 		= (bo[9] == le and bo[6] == le and bo[3] == le) # down the right side
		maxind[5]	= max(nb[9], nb[6], nb[3])
		ttt[6] 		= (bo[7] == le and bo[5] == le and bo[3] == le) # diagonal
		maxind[6]	= max(nb[7], nb[5], nb[3])
		ttt[7] 		= (bo[1] == le and bo[5] == le and bo[9] == le) # diagonal
		maxind[7]	= max(nb[1], nb[5], nb[9])
		
		winningEvent = False
		for t in ttt:
			if t:
				winningEvent = True
		if winningEvent:
			lowermaxsubscript = min([mi for mi, t in zip(maxind, ttt) if t])
		else: 
			lowermaxsubscript = -1 # failsafe option
		return winningEvent, lowermaxsubscript
		

	def realBoard(self): # returns only the "real" board, i.e. measured fields
		bo = [' '] * 10
		num = [' '] * 10
		for f in self.fields:
			for m in f.contents:
				if isinstance(m, FinMark):		
					bo[f.num] = m.letter
					num[f.num] = m.num
		return bo, num
		
	def printBoard(self): # a crude representation of the board on screen
	    fs = self.fields
	    s7 = fs[7].fieldToString()
	    s8 = fs[8].fieldToString()
	    s9 = fs[9].fieldToString()
	    print(s7+" "*(12-len(s7)) + "|" + s8 + " "*(12-len(s8)) +"|" + s9)
	    print("------------------------------------------")
	    s4 = fs[4].fieldToString()
	    s5 = fs[5].fieldToString()
	    s6 = fs[6].fieldToString()
	    print(s4+" "*(12-len(s4)) + "|" +s5 + " "*(12-len(s5)) +"|" + s6)
	    
	    print("------------------------------------------")
	    s1 = fs[1].fieldToString()
	    s2 = fs[2].fieldToString()
	    s3 = fs[3].fieldToString()
	    print(s1+" "*(12-len(s1)) + "|" +s2 + " "*(12-len(s2)) +"|" + s3)
	    
	    print("------------------------------------------")
	    """
		for f in self.fields:
			print("Field" + str(f.num))
			print(f.fieldToString())"""
			
	def isSpaceFree(self, move):
		# Return true if the passed move is free on the passed board.
		board, num = self.realBoard()
		if str(move) not in '1 2 3 4 5 6 7 8 9'.split(' '):
		  return False
		return board[move] == ' '

	def getListOfMoves(self): # returns all possible moves
		listOfMoves = []
		for move in range(1, 10):
			if self.isSpaceFree(board, move):
				listOfMoves.append(move)
		return listOfMoves
		
	# the following function is the most difficult one: It is used recursively to find a cycle in the maze of premarks in order to 
	# find out whether a collaps will take place
	def makeSteps(self, currentFieldNum, initialFieldNum):
		conts = self.fields[currentFieldNum].contents # all possible marks from the current position
		listOfNext = [c.copy() for c in conts]
		for m in listOfNext:
			if isinstance(m, FinMark):
				continue
			nextNum = m.otherpos
			cboard = self.copy()
			# delete the current mark from the copied board in order to not to use this connection as a path later
			cboard.fields[currentFieldNum].deletePreMark_(m.letter, m.num)
			cboard.fields[nextNum].deletePreMark_(m.letter, m.num)
			# in case we found our way back, we return this mark
			if nextNum == initialFieldNum: 
				return m
			else: # if we didn't make it yet, we go one step deeper
				res = cboard.makeSteps(nextNum, initialFieldNum)
				if res: 
				  return res
				else: # if "one step deeper" runs into a dead end, we take the other option in the list above
				  continue
		
	def findCycle(self, markStartingFrom):		
		copyBoard = self.copy()
		m = copyBoard.makeSteps(markStartingFrom, markStartingFrom)
		return m
	
	# this function collapses the entanglement starting with markletter,marknum at position [collapseAt], which has its second pos as [collapseNotAt]
	def collapse(self, markletter, marknum, collapseAt, collapseNotAt):
		currentField = self.fields[collapseAt]
		otherField = self.fields[collapseNotAt]
		currentField.deletePreMark_(markletter, marknum)
		otherField.deletePreMark_(markletter, marknum)
		listOfMarks = list(currentField.contents)
		currentField.addFinMark(FinMark(markletter, collapseAt, marknum))
		for markToBeReplaced in listOfMarks:
			m = markToBeReplaced
			if isinstance(m, FinMark):
				continue
		for markToBeReplaced in listOfMarks:
			m = markToBeReplaced
			if isinstance(m, FinMark):
				continue
			self.collapse(m.letter, m.num, m.otherpos, m.pos)
				
		
		
# the following classes Field, PreMark and FinMark are boring but contain a more compact description of the atomical objects Field, PreMark, FinMark in the game
class Field:
	def __init__(self, num):
		self.contents = []
		self.num = num
		
	def copy(self):
		f = Field(self.num)
		for m in self.contents:
			f.contents.append(m.copy())
		return f
		
	def addPreMark(self, pmark):
		if self.num != pmark.pos:
			print("Error: Wrong Mark position")
			return
		self.contents.append(pmark)
		
	def addFinMark(self, fmark):
		if self.num != fmark.pos:
			print("Error: Wrong Final Mark position")
			return
		self.contents.append(fmark)
	
	def deletePreMark(self, pmark):
		if pmark in self.contents:
			v.remove(pmark)
		else:
			print("Error: Pre Mark not in Field")
			
	def deletePreMark_(self, letter, num):
		for m in self.contents:
			if isinstance(m, PreMark):
				if m.num == num and m.letter == letter:
					self.contents.remove(m)
	
	def deleteFinMark(self, fmark):
		if fmark in self.contents:
			self.contents.remove(fmark)
		else:
			print("Error: Final Mark not in Field")
			
	def fieldToString(self):
		for m in self.contents:
			if isinstance(m, FinMark):
				return m.letter
		# so apparently there is no final mark
		s = ""
		for m in self.contents:
			s += (m.letter + str(m.num) + ", ")
		return s
			
class PreMark:
	def __init__(self, letter, num, pos, otherpos):
		self.letter = letter
		self.num = num
		self.pos = pos
		self.otherpos = otherpos
	def copy(self):
		pm = PreMark(self.letter, self.num, self.pos, self.otherpos)
		return pm
		
class FinMark:
	def __init__(self, letter, pos, num):
		self.letter = letter
		self.pos = pos
		self.num = num
	def copy(self):
		fm = FinMark(self.letter, self.pos, self.num)
		return fm
	
def getPlayerMove(board):
	# Let the player type in their move.
	move = ' '
	move2 = ' '
	while ((move not in '1 2 3 4 5 6 7 8 9'.split() or move2 not in '1 2 3 4 5 6 7 8 9'.split()) and move == move2) or not board.isSpaceFree(int(move)) or not board.isSpaceFree(int(move2)):
		print('What is your next move? (1-9)')
		move = raw_input()
		print('Second field? (1-9)')
		move2 = raw_input()
	return int(move), int(move2)
      
def getPlayerCollapse(board, lastMark):
    # Let the player type in their preferred collapse target
    print("You may collapse letter {0}{1} on field {2} or {3}".format(lastMark.letter, lastMark.num, lastMark.pos, lastMark.otherpos))
    choice = None
    while (not choice or choice not in [lastMark.pos, lastMark.otherpos]):
      print('What choice do you want to make? ({0}, {1})'.format(lastMark.pos, lastMark.otherpos))
      choice = int(raw_input())
    if choice == lastMark.pos:
      return choice, lastMark.otherpos
    else:
      return choice, lastMark.pos
      
def getComputerMove_Random(board):
	l = []
	for n in range(1, 10):
		if board.isSpaceFree(n):
			l.append(n)
			
	if len(l) > 1:
		r1 = random.choice(l)
		l.remove(r1)
		r2 = random.choice(l)
		return r1, r2
	else: 
		return None

def getComputerCollapse_Random(board, lastMark):
	l = [lastMark.pos, lastMark.otherpos]
	r = random.choice(l)
	l.remove(r)
	r2 = l[0]
	return r, r2
      
#######################################
def isBoardFull(b):
	# Return True if every space on the board has been taken. Otherwise return False.
	for i in range(1, 10):
		if b.isSpaceFree(i):
			return False
	return True

def getGameMode():
	print("Do you want to play against the computer or against another player? Enter (c/p)")
	inp = ''
	while inp not in ['c', 'C', 'p', 'P']:
		inp = raw_input()
	if inp == 'c' or inp == 'C':
		return 'pvc'
	else:
		return 'pvp'

def inputPlayerLetter():
   # Lets the player type which letter they want to be.
   # Returns a list with the player letter as the first item and the computer letter as the # second.
	letter = ''
	while not (letter == 'X' or letter == 'O'):
		print('Do you want to be X or O?')
		letter = raw_input().upper()
		# the first element in the list is the player letter, the second is the #computer letter.
	if letter == 'X':
		return ['X', 'O']
	else:
		return ['O', 'X']

def whoGoesFirst():
	# Randomly choose the player who goes first.
	if random.randint(0, 1) == 0:
		return 'player 2'
	else:
		return 'player 1'

def playAgain():
	# This function returns True if the player wants to play again, otherwise it returns False.
	print('Do you want to play again? (yes or no)')
	return raw_input().lower().startswith('y')

