import pygame as p
import engine

#Constants
WIDTH = HEIGHT = 500
CELL_SIZE = WIDTH // 8
FPS = 80
White = (255, 255, 255)
Green = (0, 102, 54)
Yellow = (220, 220, 5)
Grey = (128, 128, 128)
IMAGES = {}

def main():
    p.init()
    WIN = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()

    board = engine.Board()
    loadImages()

    selections = []
    highlight = []
    run = True
    while (run):
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            elif event.type == p.MOUSEBUTTONDOWN:
                
                #Handles Mouse Behavior
                m_location = p.mouse.get_pos()
                m_location = [m_location[0] // CELL_SIZE, m_location[1] // CELL_SIZE]; 

                if selections:
                    highlight = []  
                    if m_location != selections[0]:
                        selections.append(m_location)
                        board.movePiece(selections[0], selections[1])
                    selections = []
                else:
                    if (board.checkEmpty(m_location) != True):
                        highlight = board.getMoves(m_location)
                        selections.append(m_location)

        clock.tick(FPS)
        drawBoard(WIN, highlight, board)
        drawPieces(WIN, board)
        p.display.flip()
    p.quit()


#Loads icons for game pieces
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (CELL_SIZE, CELL_SIZE))

#Draws 64 background tiles
def drawBoard(screen, highlight, board):
    for r in range(8):
        for c in range(8):
            color = Green
            if ((c+r) % 2 != 0):
                color = White
            p.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
    #Renders highlighted squares
    for xy in highlight:
        if (not board.checkEmpty(xy)):
            p.draw.rect(screen, Yellow, (xy[0]*CELL_SIZE, xy[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        else:
            p.draw.circle(screen, Grey, (xy[0]*CELL_SIZE + (CELL_SIZE//2), xy[1]*CELL_SIZE + (CELL_SIZE//2)), 10)

                            
#Draws each piece of board with icon
def drawPieces(screen, board):
    spots = board.getMap()
    for spot in spots:
        screen.blit(IMAGES[spot[2]], p.Rect(spot[0] * CELL_SIZE, spot[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


if __name__ == "__main__":
    main()
