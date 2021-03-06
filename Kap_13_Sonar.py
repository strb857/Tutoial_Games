def Run():

  #Sonar Treasure Hunt

  import random
  import math
  import sys

  def getNewBoard():
    #Create new 60x15 board data structure
    board = []
    for x in range(60): #Main list is a list of 60 lists
      board.append([])
      for y in range(15): #Each list in main list has 15 single char strings
        #Use different char for the ocean to make it more readable
        if random.randint(0, 1) == 0:
          board[x].append('~')
        else:
          board[x].append('`')
    return board

  def drawBoard(board):
    # Draw the board data structure
    tensDigitsLine = '    ' #Initial space for the numbers down left side of board
    for i in range(1, 6):
      tensDigitsLine += (' ' * 9) + str(i)

    #Print numbers across top of board
    print(tensDigitsLine)
    print('    ' + ('0123456789' * 6))
    print()

    #Print each of the 15 rows
    for row in range(15):
      #Single digit numbers need to be padded w/extra space
      if row < 10:
        extraSpace = ' '
      else:
        extraSpace = ''

      # Create the string for this row on the board
      boardRow = ''
      for column in range(60):
        boardRow += board[column][row]

      print('%s%s %s %s' % (extraSpace, row, boardRow, row))

    #Print the numbers across the bottom of the board
    print()
    print(' ' + ('0123456789' * 6))
    print(tensDigitsLine)

  def getRandomChests(numChests):
    #Create list of chest data structures (two-item lists of x, y coordinates)
    chests = []
    while len(chests) < numChests:
      newChest = [random.randint(0, 59), random.randint(0, 14)]
      if newChest not in chests: #checks for duplicate chests
        chests.append(newChest)
    return chests

  def isOnBoard(x, y):
    #Return True if coordinates are on the board
    return x >= 0 and x<=59 and y >= 0 and y <= 14

  def makeMove(board, chests, x, y):
    #Change board data structure with a sonar device char
    #Remove trasure chest from chests list as they are found
    #Returns False if move is invalid
    #Otherwise returns string of the result of this move

    smallestDistance = 100 #Any chest will be closer than 100
    for cx, cy in chests:
      distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))

      if distance < smallestDistance: #We want closest chest
        smallestDistance = distance

    smallestDistance = round(smallestDistance)

    if smallestDistance == 0:
      #xy on chest!
      chests.remove([x, y])
      return 'Du har s??nkt en ub??t!'
    else:
      if smallestDistance < 10:
        board[x][y] = str(smallestDistance)
        return 'Ub??t uppt??kt p?? ett avst??nd av %s fr??n sonarbojen.' % (smallestDistance)
      else:
        board[x][y] = '?'
        return 'Ingenting uppt??kt p?? sonar. Ub??tarna ??r f??r l??ngt borta.'

  def enterPlayerMove(previousMoves):
    #Let player enter move. Return a two-item list of int xy coordinates
    print('Var vill du sl??ppa n??sta sonarboj? (0-59 0-14) (eller skriv "avluta"')
    while True:
      move = input()
      if move.lower == 'avluta':
        print('Du gav upp. B??ttre lycka n??sta g??ng!')
        sys.exit()

      move = move.split()
      if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and isOnBoard(int(move[0]), int(move[1])):
        if [int(move[0]), int(move[1])] in previousMoves:
          print('Du har redan sl??ppt en boj d??r.')
          continue
        return [int(move[0]), int(move[1])]

      print('Skriv ett nummer 0-59, mellanslag, sen ett nummer 0-14')

  def showInstructions():
    print('''Instruktioner:
          
Du ??r kapten p?? Spaningsb??ten HMS Dj??rv, med uppdrag att spana efter och s??nka ryska ub??tar i Stockholms sk??rg??rd. Till din hj??lp har du sonarboj 111 och sjunkbomb m/33.
Sonarbojarna kan enbart ange avst??nd, inte b??ring.
Ange koordinaterna f??r att sl??ppa dina motmedel. Koordinaterna p?? kartan uppdateras med avst??nd till n??rmaste m??l, eller ett "X" om sjunkbomben tr??ffat r??tt.

          Tryck Enter f??r att forts??tta...''')
    input()

    print('''N??r du s??nkt en ub??t, uppdateras ??vriga bojar f??r att visa var den n??sta n??rmaste ub??ten ??r. Om n??rmaste ub??t ??r utom r??ckh??ll markeras bojen med "?".
Sonarbojarna har en r??ckvidd p?? 9 rutor.
F??rs??k s??nka alla ub??tar innan du f??r slut p?? bojar och bomber.
          
          Lycka till!
          
          Tryck Enter f??r att forts??tta...''')
    input()


  print('*** S O N A R - U B ?? T S J A K T ***')
  print()
  print('Vill du l??sa instruktionerna? (J/N)')
  if input().upper().startswith('J'):
    showInstructions()

  while True:
    #Game Setup
    sonarDevices = 20
    theBoard = getNewBoard()
    theChests = getRandomChests(3)
    drawBoard(theBoard)
    previousMoves = []

    while sonarDevices > 0:
      #Show sonar devices and chest status
      print('Du har %s bojar/bomber kvar. %s Ub??tar ??r fortfarande p?? fri fot!' % (sonarDevices, len(theChests)))
      x, y = enterPlayerMove(previousMoves)
      previousMoves.append([x, y]) #We must track all moves so that sonar devices can be updated

      moveResult= makeMove(theBoard, theChests, x, y)
      if moveResult == False:
        continue
      else:
        if moveResult == 'Du har s??nkt en ub??t!':
          #update all sonar devices on map
          for x, y in previousMoves:
            makeMove(theBoard, theChests, x, y)
        drawBoard(theBoard)
        print(moveResult)

      if len(theChests) == 0:
        print('Du har s??nkt alla ryska ub??tar i sk??rg??rden! Grattis och bra jobbat!')
        break

      sonarDevices -= 1

    if sonarDevices == 0:
      print('Du har slut p?? bojar och sjunkbomber. De kvarvarande ryska ub??tarna smet undan med svansen mellan benen. B??ttre lycka n??sta ag??ng')
      print('De sista ub??ten/ub??tarna var h??r:')
      for x, y in theChests:
        print('    %s, %s' % (x, y))

    print('Vill du spela igen? (J/N)')
    if not input().upper().startswith('J'):
      sys.exit()
      