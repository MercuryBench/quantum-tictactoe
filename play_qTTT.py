from qTTT import *
while(True):
  theBoard = Board()
  playerLetter, player2letter = inputPlayerLetter()
  turn = whoGoesFirst()
  print('The ' + turn + ' will go first.')
  gameIsPlaying = True
  lastMark = None
  numMark = 0
  while (gameIsPlaying):
    if turn == 'player':
      print("It's player 1's turn")
      # Player's turn.
      theBoard.printBoard()
      # Check whether there is entanglement
      if lastMark:
	if theBoard.findCycle(lastMark.pos):
	  col = getPlayerCollapse(theBoard, lastMark) # returns pos, then notpos
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
      
      pos1, pos2 = getPlayerMove(theBoard)
      
      lastMark = theBoard.addPreMark(playerLetter, numMark*2, pos1, pos2)
    else:
      
      print("It's player 2's turn")
      # Player 2's turn or computer.
      theBoard.printBoard()
      # Check whether there is entanglement
      if lastMark:
	if theBoard.findCycle(lastMark.pos):
	  col = getPlayerCollapse(theBoard, lastMark) # returns pos, then notpos
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
      pos1, pos2 = getPlayerMove(theBoard)
      lastMark = theBoard.addPreMark(player2letter, numMark*2+1, pos1, pos2)
      
      numMark += 1

  if not playAgain():
	break


