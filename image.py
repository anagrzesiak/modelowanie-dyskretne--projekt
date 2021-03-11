from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from numpy import *
import time
import random
import os.path
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

root = Tk()
root.title("CIII MODELOWANIE DYSKRETNE")
root.configure(bg="black")
e = Entry(root, width=100, exportselection=0, fg="white", bg="black")
e.grid(row=4, column=0)
e1 = Entry(root, width=100, exportselection=0, fg="white", bg="black")
e1.grid(row=5, column=0)
e2 = Entry(root, width=100, exportselection=0, fg="white", bg="black")
e2.grid(row=6, column=0)
e1.insert(0, "ENTER WIDTH")
e2.insert(0, "ENTER HEIGHT")
e.insert(0, "ENTER THRESHOLD/RULE")


nbhd = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
empty, tree, fire = 0, 1, 2
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'red']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)


image = Image.open("audi2.jpg")
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)
label.image = photo
label.grid(row=0, column=0)

occupiedBytrees = 0.3
newtree, lightningStrike = 0.009, 0.0009
forestX, forestY = 100, 100
X  = np.zeros((forestY, forestX))
X[1:forestY-1, 1:forestX-1] = np.random.randint(0, 2, size=(forestY-2, forestX-2))
X[1:forestY-1, 1:forestX-1] = np.random.random(size=(forestY-2, forestX-2)) < occupiedBytrees

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)

def iterate(X):
    X1 = np.zeros((forestY, forestX))
    for ix in range(1,forestX-1):
        for iy in range(1,forestY-1):
            if X[iy,ix] == empty and np.random.random() <= newtree:
                X1[iy,ix] = tree
            if X[iy,ix] == tree:
                X1[iy,ix] = tree
                for dx,dy in nbhd:
                    if X[iy+dy,ix+dx] == fire:
                        X1[iy,ix] = fire
                        break
                else:
                    if np.random.random() <= lightningStrike:
                        X1[iy,ix] = fire
    return X1


def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)
animate.X = X


interval = 10
anim = animation.FuncAnimation(fig, animate, interval=interval)


def openNewWindow():
    newWindow = Toplevel(root);
    newWindow.title("GAME OF LIFE")
    newWindow.geometry("533x420")
    return newWindow


class GameOfLife(Frame):
    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.sizeX = 22
        self.sizeY = 14
        self.cellButtons = []
        self.generateNext = True

        self.initialUI()

    def initialUI(self):
        self.parent.title("Game of Life")
        self.buildGrid(1)
        self.startButton = Button(self.parent, text="Start", command=self.simulateGame, width=5, fg="light blue",
                                  bg="black")
        self.startButton.grid(row=1, column=0, sticky='nesw')
        self.stopButton = Button(self.parent, text="Stop", command=self.resetGame, width=5, fg="light blue",
                                  bg="black")
        self.stopButton.grid(row=1, column=1, sticky='nesw')
        self.randomButton = Button(self.parent, text="Random", command=lambda: self.buildGrid(5), width=5,
                                   fg="light blue", bg="black")
        self.randomButton.grid(row=1, column=2, sticky='nesw')
        self.oscilatorButton = Button(self.parent, text="Oscilator", command=lambda: self.buildGrid(2), width=5,
                                      fg="light blue", bg="black")
        self.oscilatorButton.grid(row=1, column=3, sticky='nesw')
        self.gliderButton = Button(self.parent, text="Glider", command=lambda: self.buildGrid(4), width=5,
                                   fg="light blue", bg="black")
        self.gliderButton.grid(row=16, column=0, sticky='nesw')
        self.constantButton = Button(self.parent, text="Constant", command=lambda: self.buildGrid(3), width=5,
                                     fg="light blue", bg="black")
        self.constantButton.grid(row=16, column=1, sticky='nesw')
        self.heartButton = Button(self.parent, text="Heart", command=lambda: self.buildGrid(6), width=5,
                                  fg="light blue", bg="black")
        self.heartButton.grid(row=16, column=2, sticky='nesw')
        self.kewlButton = Button(self.parent, text="C00L", command=lambda: self.buildGrid(7), width=5,
                                 fg="light blue", bg="black")
        self.kewlButton.grid(row=16, column=3, sticky='nesw')

    def buildGrid(self, a):
        self.gameFrame = Frame(
            self.parent, width=self.sizeX + 2, height=self.sizeY + 2, borderwidth=1, relief=SUNKEN)
        self.gameFrame.grid(row=2, column=0, columnspan=4)

        self.cellButtons = [
            [Button(self.gameFrame, bg="white", width=2, height=1) for i in range(self.sizeX + 2)]
            for j in range(self.sizeY + 2)]

        if a == 2:
            m = random.randint(0, 1)
            if m == 1:
                n = random.randint(0, 12)
                self.cellButtons[n][n]['bg'] = "magenta"
                self.cellButtons[n + 1][n]['bg'] = "magenta"
                self.cellButtons[n + 2][n]['bg'] = "magenta"
            elif m == 0:
                n = random.randint(0, 20)
                self.cellButtons[n][n]['bg'] = "magenta"
                self.cellButtons[n][n + 1]['bg'] = "magenta"
                self.cellButtons[n][n + 2]['bg'] = "magenta"


        elif a == 3:
            n = random.randint(1, 14)
            self.cellButtons[n][n]['bg'] = "magenta"
            self.cellButtons[n - 1][n + 1]['bg'] = "magenta"
            self.cellButtons[n - 1][n + 2]['bg'] = "magenta"
            self.cellButtons[n + 1][n + 1]['bg'] = "magenta"
            self.cellButtons[n + 1][n + 2]['bg'] = "magenta"
            self.cellButtons[n][n + 3]['bg'] = "magenta"

        elif a == 4:
            n = random.randint(1, 12)
            self.cellButtons[n][n]['bg'] = "magenta"
            self.cellButtons[n + 1][n]['bg'] = "magenta"
            self.cellButtons[n + 1][n - 1]['bg'] = "magenta"
            self.cellButtons[n + 2][n - 1]['bg'] = "magenta"
            self.cellButtons[n + 2][n + 1]['bg'] = "magenta"

        elif a == 5:
            m = random.randint(3, 69)
            for i in range(m):
                n = random.randint(0, 14)
                o = random.randint(0, 22)
                self.cellButtons[n][o]['bg'] = "magenta"

        elif a == 6:
            self.cellButtons[3][6]['bg'] = "magenta"
            self.cellButtons[3][7]['bg'] = "magenta"
            self.cellButtons[3][8]['bg'] = "magenta"
            self.cellButtons[4][9]['bg'] = "magenta"
            self.cellButtons[5][10]['bg'] = "magenta"
            self.cellButtons[5][11]['bg'] = "magenta"
            self.cellButtons[4][12]['bg'] = "magenta"
            self.cellButtons[3][13]['bg'] = "magenta"
            self.cellButtons[3][14]['bg'] = "magenta"
            self.cellButtons[3][15]['bg'] = "magenta"
            self.cellButtons[4][16]['bg'] = "magenta"
            self.cellButtons[5][17]['bg'] = "magenta"
            self.cellButtons[6][17]['bg'] = "magenta"
            self.cellButtons[7][16]['bg'] = "magenta"
            self.cellButtons[8][15]['bg'] = "magenta"
            self.cellButtons[9][14]['bg'] = "magenta"
            self.cellButtons[10][13]['bg'] = "magenta"
            self.cellButtons[11][12]['bg'] = "magenta"
            self.cellButtons[12][11]['bg'] = "magenta"
            self.cellButtons[12][10]['bg'] = "magenta"
            self.cellButtons[11][9]['bg'] = "magenta"
            self.cellButtons[10][8]['bg'] = "magenta"
            self.cellButtons[9][7]['bg'] = "magenta"
            self.cellButtons[8][6]['bg'] = "magenta"
            self.cellButtons[7][5]['bg'] = "magenta"
            self.cellButtons[6][4]['bg'] = "magenta"
            self.cellButtons[5][4]['bg'] = "magenta"
            self.cellButtons[4][5]['bg'] = "magenta"

        elif a == 7:
            self.cellButtons[7][8]['bg'] = "magenta"
            self.cellButtons[7][9]['bg'] = "magenta"
            self.cellButtons[7][11]['bg'] = "magenta"
            self.cellButtons[7][12]['bg'] = "magenta"
            self.cellButtons[8][9]['bg'] = "magenta"
            self.cellButtons[8][10]['bg'] = "magenta"
            self.cellButtons[8][11]['bg'] = "magenta"
            self.cellButtons[9][10]['bg'] = "magenta"
            self.cellButtons[6][9]['bg'] = "magenta"
            self.cellButtons[6][10]['bg'] = "magenta"
            self.cellButtons[6][11]['bg'] = "magenta"
            self.cellButtons[5][10]['bg'] = "magenta"


        else:
            print("git")

        for i in range(1, self.sizeY + 1):
            for j in range(1, self.sizeX + 1):
                self.cellButtons[i][j].grid(row=i, column=j, sticky=W + E)
                self.cellButtons[i][j]['command'] = lambda i=i, j=j: self.cellToggle(self.cellButtons[i][j])

    def simulateGame(self):
        self.disableButtons()
        buttonsToToggle = []
        for i in range(1, self.sizeY + 1):
            for j in range(1, self.sizeX + 1):
                coord = (i, j)
                if self.cellButtons[i][j]['bg'] == "white" and self.neighboursCount(i, j) == 3:
                    buttonsToToggle.append(coord)
                elif self.cellButtons[i][j]['bg'] == "magenta" and self.neighboursCount(i,
                                                                                        j) != 3 and self.neighboursCount(
                    i,
                    j) != 2:
                    buttonsToToggle.append(coord)

        for coord in buttonsToToggle:
            self.cellToggle(self.cellButtons[coord[0]][coord[1]])

        if self.generateNext:
            self.after(100, self.simulateGame)
        else:
            self.enableButtons()

    def disableButtons(self):
        if self.cellButtons[1][1] != DISABLED:
            for i in range(0, self.sizeY + 2):
                for j in range(0, self.sizeX + 2):
                    self.cellButtons[i][j].configure(state=DISABLED)

            self.stopButton.configure(state=NORMAL)
            self.startButton.configure(state=DISABLED)

    def enableButtons(self):
        for i in range(0, self.sizeY + 2):
            for j in range(0, self.sizeX + 2):
                self.cellButtons[i][j]['bg'] = "white"
                self.cellButtons[i][j].configure(state=NORMAL)

        self.stopButton.configure(state=DISABLED)
        self.startButton.configure(state=NORMAL)
        self.generateNext = True

    def neighboursCount(self, xCoord, yCoord):
        count = 0
        for i in range(xCoord - 1, xCoord + 2):
            for j in range(yCoord - 1, yCoord + 2):
                if (i != xCoord or j != yCoord) and self.cellButtons[i][j]['bg'] == "magenta":
                    count += 1

        return count

    def cellToggle(self, cell):
        if cell['bg'] == "white":
            cell['bg'] = "magenta"
        else:
            cell['bg'] = "white"

    def resetGame(self):
        self.generateNext = False


def startGame():
    window = openNewWindow()
    game = GameOfLife(window)
    window.mainloop()


def changePhoto(img):
    photo1 = ImageTk.PhotoImage(img)
    label = Label(root, image=photo1)
    label.image = photo1
    label.grid(row=0, column=0)


def truncate(val):
    if val < 0:
        val = 0
    elif val > 255:
        val = 255
    return val


def changeBrightness(val):
    img = image
    im = img.convert('RGB')
    imageSizeW, imageSizeH = im.size
    for i in range(1, imageSizeW):
        for j in range(1, imageSizeH):
            r, g, b = im.getpixel((i, j))
            r = truncate(r + val)
            g = truncate(g + val)
            b = truncate(b + val)
            im.putpixel((i, j), (r, g, b))
    changePhoto(im)


def getNumber(a):
    if a.get() is None:
        return 0
    else:
        string_answer = a.get()
        int_answer = int(string_answer)
        print(int_answer)
        return int_answer


dMatrix = np.array([
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9]])

upMatrix = np.array([
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1]])

gMatrix = np.array([
    [1, 4, 1],
    [4, 32, 4],
    [1, 4, 1]])

possibleNeighbours = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]])  # czy ma być odwrotnie?


def automata1D(rule, width, height):
    binary = np.binary_repr(rule, width=8)
    finalArr = np.zeros([height, width + 2])
    finalArr[0, int(width / 2) + 1] = 1;
    temp = np.zeros(3)
    for y in np.arange(0, height - 1):
        for x in np.arange(0, width - 1):
            temp[0] = finalArr[y][x]
            temp[1] = finalArr[y][x + 1]
            temp[2] = finalArr[y][x + 2]
            for i in range(8):
                if np.array_equal(possibleNeighbours[i], temp):
                    finalArr[y + 1, x + 1] = binary[i]
    for y in np.arange(0, height - 1):
        finalArr[y][0] = 1
        finalArr[y][width - 1] = 1
    for x in np.arange(0, width - 1):
        finalArr[0][x] = 1
        finalArr[height - 1][x] = 1
    return finalArr


def suma(arr, i, j, k):
    sum = (arr[i - 1][j - 1] * k[0][0]) + (arr[i][j - 1] * k[1][0]) + (arr[i + 1][j - 1] * k[2][0]) + \
          (arr[i - 1][j] * k[0][1]) + (arr[i][j] * k[1][1]) + (arr[i + 1][j] * k[2][1]) + \
          (arr[i - 1][j + 1] * k[0][2]) + (arr[i][j + 1] * k[1][2]) + (arr[i + 1][j + 1] * k[2][2])
    return truncate(sum)


def convolution(arr, matrix):
    x = np.shape(arr)[0]
    y = np.shape(arr)[1]
    finalArr = np.copy(arr)
    for i in range(1, x-1):
        for j in range(1, y-1):
            finalArr[i][j] = suma(arr, i, j, matrix)
    return finalArr


def _convert(path):
    image = Image.open(path)
    image = image.convert('1')
    A = array(image)
    new_A = empty((A.shape[0], A.shape[1]), None)
    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] == True:
                new_A[i][j] = 1
            else:
                new_A[i][j] = 0
    return new_A


def _convert2(img):
    image = img;
    image = image.convert('1')
    A = array(image)
    new_A = empty((A.shape[0], A.shape[1]), None)
    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] == True:
                new_A[i][j] = 1
            else:
                new_A[i][j] = 0
    return new_A


def neighbourhood(arr, i, j, blackWhite):
    if arr[i - 1][j - 1] == blackWhite or arr[i][j - 1] == blackWhite or arr[i + 1][j - 1] == blackWhite or \
            arr[i - 1][j] == blackWhite or arr[i][j] == blackWhite or arr[i + 1][j] == blackWhite or \
            arr[i - 1][j + 1] == blackWhite or arr[i][j + 1] == blackWhite or arr[i + 1][j + 1] == blackWhite:
        return True
    else:
        return False


def dilation(arr):
    x = np.shape(arr)[0]
    y = np.shape(arr)[1]
    finalArr = np.copy(arr)
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            if arr[i][j] == 0:
                if neighbourhood(arr, i, j, 1):
                    finalArr[i][j] = 127
    return finalArr


def erosion(arr):
    x = np.shape(arr)[0]
    y = np.shape(arr)[1]
    finalArr = np.copy(arr)
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            if arr[i][j] == 1:
                if neighbourhood(arr, i, j, 0):
                    finalArr[i][j] = 127
    return finalArr


def binarization(threshold):
    pixelMap = image.load()
    mode = image.mode
    pixelMap2 = image.load()
    width, height = image.size
    newImage = Image.new(mode, (width, height))
    newPixelMap = newImage.load()
    for x in range(width):
        for y in range(height):
            newPixelMap[x, y] = pixelMap2[x, y]
    im2 = image
    # threshold = 100
    for x in range(width):
        for y in range(height):
            orPixel = pixelMap[x, y]
            orR = orPixel[0]
            orG = orPixel[1]
            orB = orPixel[2]
            if (orR) <= threshold:
                newR = int(0)
            else:
                newR = int(255)
            if (orG) <= threshold:
                newG = int(0)
            else:
                newG = int(255)
            if int(orB) <= threshold:
                newB = int(0)
            else:
                newB = int(255)
            newPixel = (newR, newG, newB)
            newPixelMap[x, y] = newPixel
    changePhoto(newImage)
    newImage.save("ana.jpg")
    return newImage


def dil():
    if(os.path.exists("new1.jpg")):
        image = Image.open("new1.jpg")
        photo = ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo
        label.grid(row=0, column=0)
    array = dilation(_convert2(binarization(100)))
    img = Image.fromarray(np.uint8(array * 255), 'L')
    # img.show()
    changePhoto(img)
    img.save("new1.jpg")



def aut():
    array = automata1D(getNumber(e), getNumber(e1), getNumber(e2))
    img = Image.fromarray(np.uint8(array * 255), 'L')
    img.show()
    changePhoto(img)
    img.save("new.jpg")


def er():
    if (os.path.exists("new1.jpg")):
        print("ok")
        image = Image.open("new1.jpg")
        photo = ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo
        label.grid(row=0, column=0)
    array = erosion(_convert2(binarization(100)))
    print("git")
    img = Image.fromarray(np.uint8(array * 255), 'L')
    changePhoto(img)
    # img.show()
    img.save("new1.jpg")


def up():
    array = convolution(_convert("audi2.jpg"), upMatrix)
    img = Image.fromarray(np.uint8(array * 255), 'L')
    changePhoto(img)


def down():
    array = convolution(_convert("audi2.jpg"), dMatrix)
    img = Image.fromarray(np.uint8(array * 255), 'L')
    changePhoto(img)


def gs():
    array = convolution(_convert("audi2.jpg"), gMatrix / 52)
    img = Image.fromarray(np.uint8(array * 255), 'L')
    changePhoto(img)


# myLabel1=Label(root, text="OBRAZEK", fg="white", bg="black").grid(row=3, column=0)
lightenButton = Button(root, text="LIGHTEN", command=lambda: changeBrightness(getNumber(e)), padx=50, pady=5,
                       fg="light blue", bg="black").grid(row=1, column=1, sticky='nesw')
darkenButton = Button(root, text="DARKEN", command=lambda: changeBrightness(-(getNumber(e))), padx=50, pady=5,
                      fg="light blue", bg="black").grid(row=2, column=1, sticky='nesw')
binarizationButton = Button(root, text="BINARY", command=lambda: binarization(getNumber(e)), padx=50, pady=5,
                            fg="light blue", bg="black").grid(row=3, column=1, sticky='nesw')
dilationButton = Button(root, text="DILATION", command=lambda: dil(), padx=50, pady=5, fg="light blue",
                        bg="black").grid(row=4, column=1, sticky='nesw')
erosionButton = Button(root, text="EROSION", command=lambda: er(), padx=50, pady=5, fg="light blue", bg="black").grid(
    row=5, column=1, sticky='nesw')
gaussButton = Button(root, text="GAUSS", command=lambda: gs(), padx=50, pady=5, fg="light blue", bg="black").grid(
    row=6, column=1, sticky='nesw')
upButton = Button(root, text="UP FILTER", command=lambda: up(), padx=50, pady=5, fg="light blue", bg="black").grid(
    row=7, column=1, sticky='nesw')
downButton = Button(root, text="DOWN FILTER", command=lambda: down(), padx=50, pady=5, fg="light blue",
                    bg="black").grid(row=8, column=1, sticky='nesw')
originalButton = Button(root, text="SHOW ORIGINAL", command=lambda: changePhoto(image), padx=50, pady=5,
                        fg="light blue", bg="black").grid(row=9, column=1, sticky='nesw')
automataButton = Button(root, text="CELLULAR AUTOMATA 1D", command=lambda: aut(), padx=50, pady=5,
                        fg="light blue", bg="black").grid(row=10, column=1, sticky='nesw')
conveyButton = Button(root, text="GAME OF LIFE", command=lambda: startGame(), padx=50, pady=5,
                      fg="light blue", bg="black").grid(row=11, column=1, sticky='nesw')

# label.pack()
root.mainloop()
