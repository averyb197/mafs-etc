from PIL import Image, ImageTk, ImageChops, ImageOps
import os


'''
All functions made by me except trim() which was taken from a stack exchange post listed in sources, these functions prepare the images for the 
card objects'''
preloaded = {}

class Processors:
    def __init__(self, jpegPath, pngPath, preLoaded):
        self.jpegs = jpegPath
        self.pngs = pngPath
        self.preLoaded = preLoaded

    def lazyNess(self):
        for i in os.listdir(self.jpegs):
            print(i)

    def preLoad(self):
        self.makeImages()
        for i in os.listdir(self.pngs):
          #  print('PRELOAD PATH = ', i)
            imy = os.path.join(self.pngs, i)
            image = Image.open(imy)
          #  image.show(image)
            if i == 'back.png':
                image = image.resize((146, 200))
                print('resized', image.size[0], image.size[1])
           # if i.endswith('.png'):
               # i = self.makeReverse(i)
            self.preLoaded[i] = image



        #print(preLoaded)

    def makePNGS(self):
        for i in os.listdir(self.jpegs):
            image = os.path.join(self.jpegs, i)
            with Image.open(image) as imy:
                pngName = os.path.splitext(i)[0] + '.png'
                #print(pngName)
                pngPath = os.path.join(self.pngs, pngName)
               # self.trim(imy)
                imy.save(pngPath)
            pngPath = os.path.dirname(pngPath)

    def makeReverse(self, i):
        image = os.path.join(self.jpegs, i)
        with Image.open(image) as imy:
            name = 'r' + os.path.splitext(i)[0] + '.png'
           # print('NAME THAT REVERSE WILL ASSIGN = ', name)
            path = os.path.join(self.pngs, name)
           # print('PATH IT IS USING = ', path)
            imy = imy.transpose(Image.FLIP_TOP_BOTTOM)
            imy.save(path)
        return name

    def trim(self, im):
        #path = im
       # im = Image.open(im)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
           # print('I AM TRYING TO USE THIS PATH = ', path)
            #print(bbox)
            trimmed = im.crop(bbox)
            #timmed = im.copy()
            return trimmed

    def addBorder(self, img):
       # img = Image.open(path)
        borderColor = 'black'
        bordered = ImageOps.expand(img, border=-3, fill=borderColor)
        return bordered

    def makeImages(self):
        self.makePNGS()
        reverse = False
        for i in os.listdir('tarotPnG'):
            self.makeReverse(i)
        for i in os.listdir(self.pngs):

            if i.startswith('r'):
                reverse = True
            path = os.path.join(self.pngs, i)
           # print('PATH = ', path)
            imy = Image.open(path)
            if i == 'back.png':
                image = imy.resize((146, 200))
                print('resized', image.size[0], image.size[1])
                imy = image
           # if not reverse:
            trimmed = self.trim(imy)
           # else:
           #     trimmed = imy
            bordered = self.addBorder(trimmed)
            bordered.save(path)



    def randy(self):
        processor = Processors()
        processor.makeImages()


if __name__ == '__main__':
    p = Processors('tarotPnG', 'png', preloaded)

    p.makeImages()