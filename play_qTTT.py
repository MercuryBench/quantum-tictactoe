from qTTT import *
while(True): # loop for games
  theBoard = Board()
  playerLetter, player2letter = inputPlayerLetter()
  turn = whoGoesFirst()
  print('The ' + turn + ' will go first.')
  lastMark = None # needed for keeping track of the last mark in order to facilitate collapse
  numMark = 0 # needed for numbering marks
  while (True): # loop for turns
    if turn == 'player':
      print("It's player 1's turn")
      # Player 1's turn.
      theBoard.printBoard()
      # Check whether there is entanglement after player 2's move
      if lastMark:
	if theBoard.findCycle(lastMark.pos):
	  col = getPlayerCollapse(theBoard, lastMark) # let player 1 decide where to put the last mark
	  theBoard.collapse(lastMark.letter, lastMark.num, col[0], col[1]) 
	  theBoard.printBoard()
      if theBoard.hasWon(playerLetter):
	print("\n")
	theBoard.printBoard()
	print("Player 1 has won the game!")
	break
      elif theBoard.hasWon(player2letter):
	print("\n")
	theBoard.printBoard()
	print("Player 2 has won the game")
	break
      else:
	if isBoardFull(theBoard):
	  print("\n")
	  theBoard.printBoard()
	  print("The game is a tie!")
	  break
	else:
	  turn = "player2"
      # if the game hasn't ended, make a move
      pos1, pos2 = getPlayerMove(theBoard)
      
      lastMark = theBoard.addPreMark(playerLetter, numMark*2, pos1, pos2)
    else:
      
      print("It's player 2's turn")
      # Player 2's turn or computer.
      theBoard.printBoard()
      # Check whether there is entanglement after player 1's move
      if lastMark:
	if theBoard.findCycle(lastMark.pos):
	  col = getPlayerCollapse(theBoard, lastMark) # let player 2 decide where to put the last mark
	  theBoard.collapse(lastMark.letter, lastMark.num, col[0], col[1])
	  theBoard.printBoard()
      if theBoard.hasWon(playerLetter):
	print("\n")
	theBoard.printBoard()
	print("Player 1 has won the game")
	break
      elif theBoard.hasWon(player2letter):
	print("\n")
	theBoard.printBoard()
	print("Player 2 has won the game")
	break
      else:
	if isBoardFull(theBoard):
	  print("\n")
	  theBoard.printBoard()
	  print("The game is a tie!")
	  break
	else:
	  turn = "player"
	  
      # if the game hasn't ended, make a move
      pos1, pos2 = getPlayerMove(theBoard)
      lastMark = theBoard.addPreMark(player2letter, numMark*2+1, pos1, pos2)
      
      numMark += 1

  if not playAgain():
	break


