# File: DrawHexagon.py

"""
This program draws a hexagon at the center of the window.
"""

from pgl import GWindow, GPolygon, GLabel, GCompound

# Constants 


GWINDOW_WIDTH = 1000            # These constants specify the width
GWINDOW_HEIGHT = 300            # and height of the graphics window

BEEHIVE_X = 150                 # These constants specify the center
BEEHIVE_Y = 150                 # of the beehive figure

HEX_SIDE = 40                   # The length of a hexagon side
HEX_SEP = 76                    # The distance between hexagon centers
HEX_LABEL_DY = 14               # Offset to the label baseline

LABEL_FONT = "36px bold 'Helvetica Neue','Sans-Serif'"
CENTER_HEX_COLOR = "#FFCC33"
OUTER_HEX_COLOR = "#DDDDDD"

# Constants used in Milestone #3

WORDLIST_X = 300                # Starting x coordinate of the wordlist
WORDLIST_Y = 20                 # Baseline of first word listed
WORDLIST_DX = 100               # Separation between wordlist columns
WORDLIST_DY = 17                # Separation between wordlist rows
SCORE_BASELINE = 10             # Distance from bottom to score baseline
SCORE_WORDLIST_SEP = 20         # Spacing between wordlist and scores

WORDLIST_FONT = "16px 'Helvetica Neue','Sans-Serif'"
PANGRAM_COLOR = "Blue"
 
gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)

def DrawHexagon(puzzle):
    angle = 30
    figure = GCompound()
    figureinside = GCompound()
    hexagon = createHexagon(HEX_SIDE)
    hexagon.setFilled(True)
    hexagon.setColor(CENTER_HEX_COLOR)
    figureinside.add(hexagon)
    labelinside = GLabel(puzzle[0])
    labelinside.setFont(LABEL_FONT)
    figureinside.add(labelinside, -0.38*labelinside.getWidth(), HEX_LABEL_DY)
    figure.add(figureinside)
   
    for i in range (1, 7):
        
        figureinside = GCompound()
        hexagon = createHexagon(HEX_SIDE)
        hexagon.setFilled(True)
        hexagon.setColor(OUTER_HEX_COLOR)
        figureinside.add(hexagon)
        labelinside = GLabel(puzzle[i])
        labelinside.setFont(LABEL_FONT)
        figureinside.add(labelinside, -0.38*labelinside.getWidth(), HEX_LABEL_DY)
        figureinside.movePolar(HEX_SEP, angle)
        angle += 60 
        figure.add(figureinside)
    gw.add(figure, GWINDOW_WIDTH/2, GWINDOW_HEIGHT/2)
        

def createHexagon(side):
    """
    Creates a GCompound representing a regular hexagon with the specified
    side length.  The reference point is the center.
    """
    hex = GPolygon()
    hex.addVertex(-side, 0)
    angle = 60
    for i in range(6):
        hex.addPolarEdge(side, angle)
        angle -= 60
    
    return hex

# Startup code

if __name__ == "__main__":
    DrawHexagon("ABCDEFG")
