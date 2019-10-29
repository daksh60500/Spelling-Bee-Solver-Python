# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:39:03 2019

@author: DAKSH SHAMI
"""

# File: SpellingBee.py

"""
This program is a universal solver for the New York Times Spelling Bee Puzzle.
For any given 7 non-repeating letters, this program will generate the puzzle
layout as well as the word list for those letters, with first letter appearing in 
all words.
You have the choice to either randomly generate the puzzle letters or enter them 
yourselves!
Moreover, there's also the option of shuffling the outer letters of the puzzle
to help you see the combinations in a better way
Have fun!
"""

from english import ENGLISH_WORDS
from pgl import GWindow, GCompound, GPolygon, GLabel
import random

# Constants used in Milestone #1

GWINDOW_WIDTH = 1000            # These constants specify the width
GWINDOW_HEIGHT = 300            # and height of the graphics window

BEEHIVE_X = 150                 # These constants specify the center
BEEHIVE_Y = 150                 # of the beehive figure

HEX_SIDE = 40                   # The length of a hexagon side
HEX_SEP = 76                     # The distance between hexagon centers
HEX_LABEL_DY = 14           # Offset to the label baseline

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

# Main program
"""
No nonlocal variables or derived constants. All calculations have been done in functions
using their parameters to make them more versatile and reusable
"""
def SpellingBee():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT) 
    puzzle = choice()  #choice() is the function that checks whether you want to input the puzzle or generate it
    
    beehive = createBeehive(puzzle)
    gw.add(beehive, BEEHIVE_X, BEEHIVE_Y) #adding the puzzle in beehive form on the graphics window
    displayPuzzleWordList(gw, createWordList(puzzle), puzzle) #I created a bigger function than displayWordList to use puzzle without nonlocal declaration
    shuffler = input("Type Shuffle to shuffle the outer hexes: ") #Code to initiate shuffler starts
    while shuffler == "Shuffle":
        puzzle = Shuffle(puzzle)
        beehive = createBeehive(puzzle)
        gw.add(beehive, BEEHIVE_X, BEEHIVE_Y)
        print("Type anything other than Shuffle to stop")
        shuffler = input("Type Shuffle to shuffle the outer hexes: ")
        
        
    
    
def choice():
    randGen = input("Type A to use the random generator and type B to input the puzzle words: ")
    while randGen != "A" and randGen != "B": 
        print("This is not a legal input. Please try again.")
        randGen = input("Type A to use the random generator and type B to input the puzzle words: ")
    if randGen == "A":
        puzzle = randomGenerator()
        
    else:
        puzzle = userInput()
    return puzzle


def Shuffle(puzzleword):
    ShuffledWord = ""
    OriginalList = list(puzzleword.lower()).copy() #Using copy list to avoid using operations on the same assignment. Valuable in reusing code
    ShuffledList = [OriginalList[0]]
    OriginalList.remove(OriginalList[0])     
    while len(OriginalList) > 0:
        index = random.randint(0, len(OriginalList) - 1)
        ShuffledList.append(OriginalList[index])
        OriginalList.remove(OriginalList[index])
    for element in ShuffledList: #Converting list to string in this loop
        ShuffledWord += element
    return ShuffledWord.upper() #We do upper() because we want the letters in beehive to be uppercase and pretty


def randomGenerator():
    puzzle = ""
    while len(puzzle) != 7 or not legalInput(puzzle) or "s" in puzzle: 
        index = random.randint(0, len(ENGLISH_WORDS) - 1) #Using a random 7 lettered english word without s
        puzzle = ENGLISH_WORDS[index]
    return puzzle.upper()


def createBeehive(puzzle):
    
    #This function takes the parameter as string and outputs the beehive
    angle = 30
    figure = GCompound() #This will store the whole beehive and is the output of the function in the end
    figureinside = GCompound() #This will store the intermediate values to be put into figure
    hexagon = createHexagon(HEX_SIDE)
    hexagon.setFilled(True)
    hexagon.setColor(CENTER_HEX_COLOR)
    figureinside.add(hexagon)
    labelinside = GLabel(puzzle[0])
    
    labelinside.setFont(LABEL_FONT)
    figureinside.add(labelinside, -0.5*labelinside.getWidth(), HEX_LABEL_DY)    #Using -0.5 times label width tends to center the label more
    figure.add(figureinside)
   
    for i in range (1, 7):
        
        figureinside = GCompound()
        hexagon = createHexagon(HEX_SIDE)
        hexagon.setFilled(True)
        hexagon.setColor(OUTER_HEX_COLOR)
        figureinside.add(hexagon)
        labelinside = GLabel(puzzle[i])
        labelinside.setFont(LABEL_FONT)
        labelinside.setLocation(-0.5*labelinside.getWidth(), HEX_LABEL_DY)
        figureinside.add(labelinside)
        figureinside.movePolar(HEX_SEP, angle)
        angle += 60 
        figure.add(figureinside)
    
    return figure
        

    

def createHexagon(side):
    
    hex = GPolygon()
    hex.addVertex(-side, 0)
    angle = 60
    for i in range(6):
        hex.addPolarEdge(side, angle)
        angle -= 60
    return hex


def createWordList(puzzle):
    list1 = []
    for word in ENGLISH_WORDS:
        if isLegalEntry(word, puzzle):
            list1.append(word)
    return list1


def isLegalEntry(word, puzzle): #Outputs boolean form
   
    word1 = word.lower()
    puzzle1 = puzzle.lower()
    
    if len(word)<4: #Checking whether word is at least 4 letters long
        return False
    for i in range (0, len(word)):
        if word1[i] not in list(puzzle1): #Checking whether word contains only the puzzle letters
            return False
        elif puzzle1[0] not in list(word1): #Checking whether first letter is in the word
            return False
    return True


    
def displayPuzzleWordList(gw, wordlist, Puzzle):
    
    NumberOfWords = 0
    NumberOfPoints = 0
    NumberOfPangram = 0
    mainlist = wordlist
    MaxNumberOfRows = ((gw.getHeight() - WORDLIST_Y - SCORE_BASELINE - SCORE_WORDLIST_SEP) // WORDLIST_DY) + 1 #Rounding up
    
    while len(mainlist) % MaxNumberOfRows != 0:
        mainlist.append("")
        NumberOfWords -= 1 #Every empty entry should be worth zero words
        NumberOfPoints += 3 #Every empty entry should be worth a net of zero points
    
    #print("NumberOfWords for empty is " + str(NumberOfWords))
    #print("NumberOfPoints for empty is " + str(NumberOfPoints))
    
    MaxNumberOfColumns = (len(mainlist) // MaxNumberOfRows) + 1 #Floating fraction will be rounded up
    
    for c in range(MaxNumberOfColumns):
        for r in range(MaxNumberOfRows):
            if c == MaxNumberOfColumns - 1 and r >= len(mainlist) - len(wordlist):
                break
            xCoordinate = WORDLIST_X + c*WORDLIST_DX
            yCoordinate = WORDLIST_Y + r*WORDLIST_DY
            elementList = mainlist[c*MaxNumberOfRows: (c+1)*MaxNumberOfRows] #Getting elements in a column
                       
            if c == MaxNumberOfColumns - 1 and r >= len(mainlist) - len(wordlist): #To not go beyond the index of the list
                break
            
            element = elementList[r]    #From the column elementList, choosing the r'th entry
            label = GLabel(element, xCoordinate, yCoordinate)
            label.setFont(WORDLIST_FONT)
            NumberOfWords += 1
            
            if len(element) >= 7:    #From here, the code to assign points starts
                check = True
                NumberOfPoints += len(element) - 3
               
                for i in range(7):
                    if list(Puzzle.lower())[i] not in list(element):
                        check = False
                
                if check:        
                    label.setColor(PANGRAM_COLOR)
                    NumberOfPoints += 7
                    NumberOfPangram += 1#Here's the code for bonus pangram points
                    
                
            else:
                NumberOfPoints += len(element) - 3 #Code to assign points to less than 7 lettered words
            
            
            
           #The two lines below were part of the debugging process 
           
           # print("NumberOfWords for this step is " + str(NumberOfWords))
           # print("NumberOfPoints for this step is " + str(NumberOfPoints))
           
           #By printing out the values for these variables, I was able to see the problem in previous code
            gw.add(label)            
    print("Number of Pangrams are: " + str(NumberOfPangram))
    WordsAndPoints = str(NumberOfWords) + " words; " + str(NumberOfPoints) + " points"
    labelWordsAndPoints = GLabel(WordsAndPoints, WORDLIST_X, gw.getHeight() - SCORE_BASELINE)
    labelWordsAndPoints.setFont(WORDLIST_FONT)
    gw.add(labelWordsAndPoints)


def userInput():
    puzzle = input("Enter puzzle letters with center hex first: ")
    while not legalInput(puzzle):
        print("This is not a legal puzzle. Please try again.")
        puzzle = input("Enter puzzle letters with center hex first: ")
    return puzzle
    

def legalInput(puzzle):
    if len(puzzle)!= 7: #Input has to be 7 Lettered
        return False
    puzzlelower = puzzle.lower() #Used lower() just to avoid inconsistency. This made the code reusable for randomGenerator function
    listpuzzle = list(puzzlelower)
    for i in range(7):
        if listpuzzle.count(listpuzzle[i]) != 1: #Checks whether any element i.e. letter is repeated
            return False
    return True

#Startup code

if __name__ == "__main__":
    SpellingBee()
