'''
TODO:
-instructions for en pessant and castling 
-random choice AI 
'''

#Converts from [x, y] <-> cell


def gridConvert(coord):
    return (coord[1] * 8) + coord[0]
def cellConvert(cell):
    coord = [int(cell //8), int(cell % 8)]
    return coord

#Returns true if coord is in bounds
def checkBounds(coord):
    return (-1 < coord[0] < 8 and -1 < coord[1] < 8)

#
class Board:
    #Initiates board into start state
    cells = [
    4, 2, 3, 5, 6, 3, 2, 4,
    1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    11, 11, 11, 11, 11, 11, 11, 11,
    14, 12, 13, 15, 16, 13, 12, 14
    ] 


    #Maps board into list for gui render
    def getMap(self):
        pieces = []
        cur = 0
        for r in range(8):
            for c in range(8):
                cell = self.cells[cur]
                if (cell != 0):
                    prefix = 'b'
                    if (cell > 10):
                        prefix = 'w'
                        cell -= 10
                    type = {1 : 'p', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K'}
                    pieces.append([c, r, prefix + type[cell]])
                cur += 1
        return pieces

    #Checks if there is a piece on given spot of board; returns true if empty
    def checkEmpty(self, input):
        return (self.cells[gridConvert(input)] == 0)

    #Checks if given input is black piece; returns true if so
    def isBlack(self, input):
        if self.cells[gridConvert(input)] == 0: return None
        return (self.cells[gridConvert(input)] > 10)


    #Returns different possible moves
    def getMoves(self, c):
        options = []
        color = self.isBlack(c)

        #Recursive function to get every valid cell
        def rCheck(x, y, a, r):
            if not checkBounds([x, y]) or [x, y] in a and c!= [x, y]: return 
            if not self.checkEmpty([x, y]) and c != [x, y]:
                if self.isBlack([x, y]) != color:
                    a.append([x, y])
                return
            if [x, y] != c: a.append([x, y])
            rCheck(x+r[0], y+r[1], a, r)

        #Moves for pawns
        def p(self):
            options = [c]
            spots = []
            if color:
                spots = [[c[0], c[1] - 1]]
            else: 
                spots = [[c[0], c[1] + 1]]
            if (c[1] == 6 and color): spots.append([c[0], c[1] - 2])
            if (c[1] == 1 and not color): spots.append([c[0], c[1] + 2])

            for choice in spots:
                if self.checkEmpty(choice):
                    options.append(choice)
                else:
                    break
            if color:
                if not self.checkEmpty([c[0] + 1, c[1] - 1]): options.append([c[0] + 1, c[1] - 1])
                if not self.checkEmpty([c[0] - 1, c[1] - 1]): options.append([c[0] - 1, c[1] - 1])
            else:
                if not self.checkEmpty([c[0] + 1, c[1] + 1]): options.append([c[0] + 1, c[1] + 1])
                if not self.checkEmpty([c[0] - 1, c[1] + 1]): options.append([c[0] - 1, c[1] + 1])

            return options

        #Moves for knights
        def N(self):
            options = [c,
            [c[0] - 1, c[1] - 2], [c[0] + 1, c[1] - 2],
            [c[0] - 1, c[1] + 2], [c[0] + 1, c[1] + 2],
            [c[0] - 2, c[1] + 1], [c[0] + 2, c[1] + 1],
            [c[0] - 2, c[1] - 1], [c[0] + 2, c[1] - 1],
            ]
            return options

        #Moves for bishops
        def B(self):
            options = [c]
            corners = [[1, -1], [-1, 1], [1, 1], [-1, -1]]
            for dir in corners:
                rCheck(c[0], c[1], options, dir)

            return options

        def R(self):
            options = [c]
            corners = [[0, -1], [0, 1], [1, 0], [-1, 0]]
            for dir in corners:
                rCheck(c[0], c[1], options, dir)

            return options

        def Q(self):    
            options = [c]
            corners = [[1, -1], [-1, 1], [1, 1], [-1, -1],
                        [0, -1], [0, 1], [1, 0], [-1, 0]]
            for dir in corners:
                rCheck(c[0], c[1], options, dir)
            
            return options

        def K(self):
            options = [c, [c[0]+1, c[1]], [c[0]-1, c[1]], [c[0], c[1]+1], [c[0], c[1]-1],
                        [c[0]+1, c[1]-1], [c[0]-1, c[1]+1], [c[0]+1, c[1]+1], [c[0]-1, c[1]-1]]
            #King can't capture enemy king
            for option in options:
                if checkBounds(option):
                    if self.cells[gridConvert(option)] == 6: options.remove(option)
            return options
           
        type = {11: p, 1: p, 12: N, 2: N, 13: B, 3: B, 14: R, 4: R, 15: Q, 5: Q, 16: K, 6: K}
        piece = self.cells[gridConvert(c)]
        options = type[piece](self)
        #Ensures each option is valid
        if options:
            for i in range(len(options)):
                if not checkBounds(options[i]) or color == self.isBlack(options[i]):
                    options[i] = c

        return options

    #Handles movement of pieces
    def movePiece(self, orgin, dest):
        moves = self.getMoves(orgin)
        if dest in moves:
            self.cells[gridConvert(dest)] = self.cells[gridConvert(orgin)]
            self.cells[gridConvert(orgin)] = 0
        
    



