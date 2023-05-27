import tkinter
import customtkinter as ctk
import time
import os
from PIL import Image, ImageTk
import numpy as np
from tabulate import tabulate
import threading

from tarotReader import Reader
from processors import Processors

pngs = r"png"
jpegs = r"tarotPnG"

welcome='Welcome To The Digital Tarot Realm! \n' \
        'Please enter a question for the cards and press ask.'

note = 'If the program appears to not be responding please give it a minute, the API can be slow. '

preLoaded = {}
cards = {'Ace of Cups': 'acecups.png', 'Ace of Wands': 'aceofwands.png', 'Ace of Pentacles': 'acepentacles.png', 'Ace of Swords': 'aceswords.png', 'The Chariot': 'chariot.png', 'Ten of Cups': 'cups10.png', 'Two of Cups': 'cups2.png', 'Three of Cups': 'cups3.png', 'Four of Cups': 'cups4.png', 'Five of Cups': 'cups5.png', 'Six of Cups': 'cups6.png', 'Seven of Cups': 'cups7.png', 'Eight of Cups': 'cups8.png', 'Nine of Cups': 'cups9.png', 'Death': 'death.png', 'The Devil': 'devil.png', 'The Emperor': 'emporer.png', 'The Empress': 'empress.png', 'The Fool': 'fool.png', 'The Hanged Man': 'hangedMan.png', 'The Hierophant': 'heirophant.png', 'The Hermit': 'hermit.png', 'The High Priestess': 'highPriestass.png', 'Judgement': 'judgement.png', 'Justice': 'justice.png', 'King of Cups': 'kingcups.png', 'King of Pentacles': 'kingpentacles.png', 'King of Swords': 'kingswords.png', 'King of Wands': 'kingwands.png', 'Knight of Cups': 'knightCups.png', 'Knight of Pentacles': 'knightpentacles.png', 'Knight of Swords': 'knightswords.png', 'Knight of Wands': 'knightwands.png', 'The Lovers': 'lovers.png', 'The Magician': 'magician.png', 'The Moon': 'moon.png', 'Page of Cups': 'pageCups.png', 'Page of Pentacles': 'pagepentacles.png', 'Page of Swords': 'pageswords.png', 'Page of Wands': 'pagewands.png', 'Ten of Pentacles': 'pentacles10.png', 'Two of Pentacles': 'pentacles2.png', 'Three of Pentacles': 'pentacles3.png', 'Four of Pentacles': 'pentacles4.png', 'Five of Pentacles': 'pentacles5.png', 'Six of Pentacles': 'pentacles6.png', 'Seven of Pentacles': 'pentacles7.png', 'Eight of Pentacles': 'pentacles8.png', 'Nine of Pentacles': 'pentacles9.png', 'Queen of Cups': 'queencups.png', 'Queen of Pentacles': 'queenpentacles.png', 'Queen of Swords': 'queenSwords.png', 'Queen of Wands': 'queenwands.png', 'The Star': 'star.png', 'Strength': 'strength.png', 'The Sun': 'sun.png', 'Ten of Swords': 'swords10.png', 'Two of Swords': 'swords2.png', 'Three of Swords': 'swords3.png', 'Four of Swords': 'swords4.png', 'Five of Swords': 'swords5.png', 'Six of Swords': 'swords6.png', 'Seven of Swords': 'swords7.png', 'Eight of Swords': 'swords8.png', 'Nine of Swords': 'swords9.png', 'Temperance': 'temperance.png', 'The Tower': 'tower.png', 'Two of Wands': 'wands2.png', 'Three of Wands': 'wands3.png', 'Four of Wands': 'wands4.png', 'Five of Wands': 'wands5.png', 'Six of Wands': 'wands6.png', 'Seven of Wands': 'wands7.png', 'Eight of Wands': 'wands8.png', 'Nine of Wands': 'wands9.png', 'Ten of Wands': 'wands10.png', 'Wheel of Fortune': 'wheelofFortune.png', 'The World': 'world.png',
'Ace of Cups Reverse': 'racecups.png',
    'Ace of Wands Reverse': 'raceofwands.png',
    'Ace of Pentacles Reverse': 'racepentacles.png',
    'Ace of Swords Reverse': 'raceswords.png',
    'The Chariot Reverse': 'rchariot.png',
    'Ten of Cups Reverse': 'rcups10.png',
    'Two of Cups Reverse': 'rcups2.png',
    'Three of Cups Reverse': 'rcups3.png',
    'Four of Cups Reverse': 'rcups4.png',
    'Five of Cups Reverse': 'rcups5.png',
    'Six of Cups Reverse': 'rcups6.png',
    'Seven of Cups Reverse': 'rcups7.png',
    'Eight of Cups Reverse': 'rcups8.png',
    'Nine of Cups Reverse': 'rcups9.png',
    'Death Reverse': 'rdeath.png',
    'The Devil Reverse': 'rdevil.png',
    'The Emperor Reverse': 'remporer.png',
    'The Empress Reverse': 'rempress.png',
    'The Fool Reverse': 'rfool.png',
    'The Hanged Man Reverse': 'rhangedMan.png',
    'The Hierophant Reverse': 'rheirophant.png',
    'The Hermit Reverse': 'rhermit.png',
    'The High Priestess Reverse': 'rhighPriestass.png',
    'Judgement Reverse': 'rjudgement.png',
    'Justice Reverse': 'rjustice.png',
    'King of Cups Reverse': 'rkingcups.png',
    'King of Pentacles Reverse': 'rkingpentacles.png',
    'King of Swords Reverse': 'rkingswords.png',
    'King of Wands Reverse': 'rkingwands.png',
    'Knight of Cups Reverse': 'rknightCups.png',
    'Knight of Pentacles Reverse': 'rknightpentacles.png',
    'Knight of Swords Reverse': 'rknightswords.png',
    'Knight of Wands Reverse': 'rknightwands.png',
    'The Lovers Reverse': 'rlovers.png',
    'The Magician Reverse': 'rmagician.png',
    'The Moon Reverse': 'rmoon.png',
    'Page of Cups Reverse': 'rpageCups.png',
    'Page of Pentacles Reverse': 'rpagepentacles.png',
    'Page of Swords Reverse': 'rpageswords.png',
    'Page of Wands Reverse': 'rpagewands.png',
    'Ten of Pentacles Reverse': 'rpentacles10.png',
    'Two of Pentacles Reverse': 'rpentacles2.png',
    'Three of Pentacles Reverse': 'rpentacles3.png',
    'Four of Pentacles Reverse': 'rpentacles4.png',
    'Five of Pentacles Reverse': 'rpentacles5.png',
    'Six of Pentacles Reverse': 'rpentacles6.png',
    'Seven of Pentacles Reverse': 'rpentacles7.png',
    'Eight of Pentacles Reverse': 'rpentacles8.png',
    'Nine of Pentacles Reverse': 'rpentacles9.png',
    'Queen of Cups Reverse': 'rqueencups.png',
    'Queen of Pentacles Reverse': 'rqueenpentacles.png',
    'Queen of Swords Reverse': 'rqueenSwords.png',
    'Queen of Wands Reverse': 'rqueenwands.png',
    'The Star Reverse': 'rstar.png',
    'Strength Reverse': 'rstrength.png',
    'The Sun Reverse': 'rsun.png',
    'Ten of Swords Reverse': 'rswords10.png',
    'Two of Swords Reverse': 'rswords2.png',
    'Three of Swords Reverse': 'rswords3.png',
    'Four of Swords Reverse': 'rswords4.png',
    'Five of Swords Reverse': 'rswords5.png',
    'Six of Swords Reverse': 'rswords6.png',
    'Seven of Swords Reverse': 'rswords7.png',
    'Eight of Swords Reverse': 'rswords8.png',
    'Nine of Swords Reverse': 'rswords9.png',
    'Temperance Reverse': 'rtemperance.png',
    'The Tower Reverse': 'rtower.png',
    'Two of Wands Reverse': 'rwands2.png',
    'Three of Wands Reverse': 'rwands3.png',
    'Four of Wands Reverse': 'rwands4.png',
    'Five of Wands Reverse': 'rwands5.png',
    'Six of Wands Reverse': 'rwands6.png',
    'Seven of Wands Reverse': 'rwands7.png',
    'Eight of Wands Reverse': 'rwands8.png',
    'Nine of Wands Reverse': 'rwands9.png',
    'Ten of Wands Reverse': 'rwands10.png',
    'Wheel of Fortune Reverse': 'rwheelofFortune.png',
    'The World Reverse': 'rworld.png'
}

textcolor = '#E8C8E8'
labelColor = '#C0C0C0'
font = ('Helvetica', 13, 'bold')
biggerFont = ('Helvetica', 14)


class Card(ctk.CTkCanvas):
    def __init__(self, namo, parent, destination=None, isChosen=False, forcex=None, forcey=None):  # make a canvas
        super().__init__(parent)
        self.cardImgSize = (146, 200)
        self.parent = parent
        self.destination = destination
        self.cardid = None
        if namo == 'back.png':
            self.namo = namo
        else:
            self.namo = cards[namo]
        self.startTime = time.time()
        self.isChosen = isChosen
        self.x = 100
        self.y = 100

        if forcex and forcey is not None:
            self.x = forcex
            self.y = forcey

        if isChosen:
            self.x = np.random.randint(-500, -100)
            self.y = np.random.randint(1000, 1300)

        self.dxd = np.random.choice([-2, -1.5, -1.25, -1, -.7, .7, .70, 1, .75, .5, -.5])
        self.dyd = np.random.choice([-1, -.75, .5, -5, .6, .80, 1, 1.25, 1.5, 1.75])
        print(self.x, self.y)
        self.makeCard()

    def makeCard(self, borderSize=10):
      #  addy = preLoaded[self.namo]
        addy = os.path.join(pngs, self.namo)
        self.cardImg = Image.open(addy)

        self.width, self.height = self.cardImgSize
        self.cwidth, self.cheight = (self.width + borderSize), (self.height + borderSize)
        self.config(width=self.cwidth, height=self.cheight, highlightthickness=0)
        x, y = (self.cwidth / 2), (self.cheight / 2)
        self.config(width=self.cwidth, height=self.cheight, background='black') # size to be border width bigger than image
        self.realCardImg = ImageTk.PhotoImage(image=self.cardImg)
        self.create_image(x, y, image=self.realCardImg)
        return self

    def makeMovableCard(self):
        self.dxd, self.dyd = np.random.choice([-1, 1]), np.random.choice([-1, 1])
        self.card, self.cardFrame, self.dxd, self.dyd = MainWindow.placeCard(self.x, self.y, self.dxd, self.dyd)

    def moveCard(self):
        #print(self.dxd, self.dyd)
        self.dx = 7 * self.dxd
        self.dy = 7 * self.dyd
        if self.x + self.dx > 1100 or self.x + self.dx < 0:
            self.dxd = self.dxd * -1
            self.dx = 10 * self.dxd
           # print('Changing Directions, dxd = ', self.dxd)
        elif self.y + self.dy > 670 or self.y + self.dy < -3:
            self.dyd = self.dyd * -1
            self.dy = 10 * self.dyd
            #print('changing dir, dyd = ', self.dyd)
        self.x = self.dx + self.x
        self.y = self.dy + self.y

    def moveUp(self):
        self.dy = -5
        self.y = self.dy + self.y

    def chosenToFrame(self, stop=False):
        #print('chosentoframe')
        destx, desty, unused = self.destination
        if abs(self.x - destx) <= 2 and abs(self.y - desty) <= 2:
            stop = True
        #print(destx, desty)
        if self.x < destx:
            #print('dxd')
            self.dxd = 1
        elif self.x > destx:
            #print('dxd')
            self.dxd = -1
        if self.y < desty:
            #print('dyd')
            self.dyd = 1
        elif self.y >desty:
            #print('dyd')
            self.dyd = -1

        self.ldx = abs(destx - self.x) * self.dxd #long dx/dy = total to go
        self.ldy = abs(desty - self.y) * self.dyd

        self.x = self.x + self.dx
        self.y = self.y + self.dy
        vectorLength = np.sqrt((self.dx**2 + self.dy**2)) #distance formula

        self.dx = self.ldx / vectorLength
        self.dy = self.ldy / vectorLength

        if stop:
            print('STOPPING')
            self.x = destx
            self.y = desty

        xtogo = abs(destx - self.x)
        ytogo = abs(desty - self.y)
        table = []
        table.append((self.x, self.y, self.dxd, self.dyd, self.dx, self.dy, xtogo, ytogo, stop))
      #  print(tabulate(table, headers=('X', 'Y', 'XD', 'YD', 'DX', 'DY', 'XTOGO', 'YTOGO', 'STOP')))
        return stop

    def deleteCard(self):
        self.delete()

class Window(ctk.CTk): #need ctk.CTk to be able to use if name main

    def __init__(self):
        super().__init__()
        self.geometry('500x500')

        self.structs = ctk.CTkLabel(self, text=welcome)
        self.structs.pack(pady=15)

        self.question = ctk.CTkTextbox(self, height=75, wrap='word')
        self.question.pack(pady=15)

        button = ctk.CTkButton(self, text='Ask', command=lambda: self.start(self.question))
        button.pack()

        self.note = ctk.CTkLabel(self, text=note, wraplength=300)
        self.note.pack(pady=15, anchor='n')

        self.toplevel_window = None

    def start(self, question):
            reader = Reader(question)
            cards = reader.chosen
            self.withdraw()
            self.toplevel_window = MainWindow(self, 1000, 700, cards, reader)  # create window if its None or destroyed


            self.toplevel_window.lift()
            self.toplevel_window.focus_force()

class MainWindow(ctk.CTkToplevel): #inits toplevel window
    processor = Processors(jpegs, pngs, preLoaded)
    processor.makeImages()
    #processor.preLoad()
    def __init__(self, parent, x, y, cards, reader):
        super().__init__()
        self.started = False
        geometryString = str(x)+'x'+str(y)
        self.xDim, self.yDim = x, y # dimensions of window
        self.geometry(geometryString)
        self.parent = parent
        self.protocol('WM_DELETE_WINDOW', self.on_close)
       # self.deiconify #focus if hidden

        self.madeItCount = 0

        self.stopstop = False

        self.choices = cards
        self.blocks = reader.blocks

        self.frameNumba = 1
        self.compensate = 0
        self.destFrames = []

        self.textFrameNumba = 0
        self.textFrames = []
        self.textFrameCoords = []

        self.mainCanvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.mainCanvas.pack(expand=True, fill='both')

        self.mainCanvasImage = Image.open(r'misc\background.png')
        self.cannySizo = self.mainCanvasImage.resize((1300, 1000))
        self.imy = ImageTk.PhotoImage(self.cannySizo)
        self.mainCanvas.create_image(0, 0, image=self.imy, anchor=tkinter.NW)

        self.mainWidth = self.xDim
        self.mainHeight = self.yDim

        self.labelNumba = 0

        for i in range(3):
            self.destFrames.append(self.placeDestinationFrames())

        for i in range(3):
            self.textFrameCoords.append(self.placeText())

        self.runCards()

    def placeLabels(self):
        print(self.choices)

        title = self.choices[self.labelNumba]
        info = self.destFrames[(self.labelNumba)]
        self.labelNumba +=1

        x = (info[0] + (146/2))
        y = info[1] + 220

        print(title, info, x, y, '============')

        self.mainCanvas.create_text(x, y, text=title, justify='center', fill=labelColor, font=biggerFont, width=200, anchor='n')
        #self.mainCanvas.itemconfig(labels, shadow=(0,0, 'white'))


        print('LABELS - ', x, y)

    def placeActualText(self):
        if self.blocks is not None:
            print(self.blocks)

            print('BLOCKS - ', self.blocks)
            i = 1
            for j in self.textFrameCoords:
                x, y = j
                if (i-1) <3:
                    x = x + 50
                elif (i-1) ==3:
                    x = x + 50
                y = y+10
                self.mainCanvas.create_text(x, y, text=self.blocks[i], width=230, fill=textcolor, font=font, anchor='nw')
                i = i + 1
            self.mainCanvas.create_text(300, 15, text=self.blocks[0], fill=textcolor, width=700, justify='center', anchor='nw', font=font)
            self.mainCanvas.create_text(300, 700, text=self.blocks[4], fill=textcolor, width=700, justify='center', anchor='nw', font=font)
        else:
            pass

    def placeDestinationFrames(self):
        cardWidth, cardHeight = 145, 195
        randShift = 30
        totalSeporator = self.mainWidth - (cardWidth * 3)
        y = (self.mainHeight / 8)
        interval = (totalSeporator / 3)
        x = (interval * self.frameNumba) + self.compensate + randShift
        self.compensate = self.compensate + cardWidth
        print(self.compensate)
        center = (x + 145) / 2
        info = (x, y, center)
        print(info)
        self.frameNumba = self.frameNumba + 1

        canny = ctk.CTkCanvas(master=self.mainCanvas, background='black', width=cardWidth, height=cardHeight)
        canny.place(x=x, y=y)
        return info

    def placeText(self):
        pad = 50
        offset = 100

        width = (1000 - (pad*4)) / 3

        x = (pad + (pad * len(self.textFrameCoords)) + (146 * len(self.textFrameCoords)) + .57* (width*len(self.textFrameCoords) - 1)) + offset
        y = 350
        info = (x, y)
        self.textFrameNumba += 1

        return info

    def placeCard(self, card, cardFrame):
        card.place(x=0, y=0) # places inside parent frame
        cardFrame.place(x=card.x, y=card.y) #place on main canvas
        return card, cardFrame

    def deleteCard(self, cardFrame):
        cardFrame.place_forget()
        #print(cardFrame)

    def cardLoop(self, card=None, cardFrame=None, path='back.png'):
        if cardFrame == None:
            cardFrame = ctk.CTkCanvas(self.mainCanvas)
            cardFrame.config(width=155, height=208, highlightthickness=0)
        else:
            pass

        if not self.started or card == None:
            card = Card(namo=path, parent=cardFrame)
            self.started = True
        else:
            pass
        card.moveCard()
        self.deleteCard(cardFrame)
        card, cardFrame = self.placeCard(card, cardFrame)
        self.mainCanvas.after(50, lambda: self.cardLoop(card=card, cardFrame=cardFrame))

    def chosenLoop(self, path, destination, fx=None, fy=None, card=None, cardFrame=None, stop=False):
        urcard = card
       # print('chosenloop')
        if cardFrame == None:
            cardFrame = ctk.CTkCanvas(self.mainCanvas)
            cardFrame.config(width=155, height=208, highlightthickness=0)
        else:
            pass
        if not self.started or card == None:
            #print('DIDNT RANDOMIZE')
            urcard = Card(namo='back.png', parent=cardFrame, destination=destination, isChosen=True)
            self.started = True
            print(urcard)
          #  print('started')
        else:
            #print('else past urcard making')
            pass
        elapsed = time.time() - urcard.startTime
       # print(elapsed)
        if elapsed < 3.0:
            #print('undertimelimit')
            urcard.moveCard()
            self.deleteCard(cardFrame)
            urcard, cardFrame = self.placeCard(urcard, cardFrame)
        stop = urcard.chosenToFrame()
        self.deleteCard(cardFrame)

        if stop:
            print('++++++++++++++++++++++++++++++++++++++')
            scard = Card(namo=path, parent=cardFrame, destination=destination, forcex=urcard.x, forcey=urcard.y)
            scard, cardFrame = self.placeCard(scard, cardFrame)
            print('MADE IT!!!!')
            self.stopstop=True
            self.madeItCount +=1
        urcard, cardFrame = self.placeCard(urcard, cardFrame)
        if not stop:
            self.mainCanvas.after(50, lambda: self.chosenLoop(card=urcard, cardFrame=cardFrame, path=path, destination=destination))

        if self.stopstop:
            print('dommedomedomeodomed')

        if self.madeItCount == 3:
            self.secondHalfManager()

    def secondHalfManager(self):
        for i in range(3):
            self.placeLabels()
        for i in range(3):
            self.placeActualText()

    def moveUp(self, card, cardFrame, path, started=False):
        if card.y > 250:
            card.moveUp()
            card, cardFrame = self.placeCard(card, cardFrame)
            self.mainCanvas.after(50, lambda: self.moveUp(card=card, cardFrame=cardFrame, path=path, started=True))
        elif card.y < 100:
            pass

    def runCards(self):
        threads = []
        for i in range(3):
            if i < 3:
                print('FRMAES', self.destFrames)
                tbo = threading.Thread(target=self.chosenLoop(path=self.choices[i], destination=self.destFrames[(i)], fx=(np.random.randint(-500, -100)), fy=(np.random.randint(1200, 2000))))
                threads.append(tbo)
                print(self.destFrames[i])
            else:
                print('else')
                tbo = threading.Thread(target=self.cardLoop())
                threads.append(tbo)
        for i in threads:
            i.start()
        print('got past')
        for i in threads:
            print('joined')
            i.join()
        print('FINISHED')

    def on_close(self):
        self.parent.deiconify()  # show the first window again
        self.withdraw()

if __name__ == '__main__':
    window = Window()
    window.mainloop()



