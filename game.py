from tkinter import Tk, Canvas, Label, PhotoImage, Button, messagebox, Entry
from random import randint as rand
import time

# bullets = 1000
# money = 0
windowWidth = 0
windowHeight = 0
# Your Steps
steps = 0
# decision
decision = False
# this variable is holding the phase of the game
gamePhase = "interactL"
walk = 0
chase = 27
openspaceX = 0
openspaceX1 = 0
openspaceY = 0
openspaceY1 = 0
magicianCome = 0
pause = False
# This variable will hold the string value of the saved variables
textSave = ""
user = "defaultUser"
# This variable is used when the the game is saved
save = True

message = ["a", "b", "c", "d", "e", "f", "g", "e"]


class Unicorn:
    # def __init__(self, x = windowWidth/2, y = windowHeight/2, width = windowWidth/ 10.24, height = windowHeight/ 12.8):
    def __init__(
        self, x=0, y=0, width=0, height=0, speed=0, crosses=0, start=False, alive=True
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.crosses = crosses
        self.start = start
        self.alive = alive

    def create(self, x, y, width, height, speed, nameOfImg):
        self.setXY(x, y)
        self.setImg(nameOfImg)
        self.width = width
        self.height = height
        self.speed = speed
        self.crosses = 0

    def getStatus(self):
        # dead or alive
        return self.alive

    def die(self):
        self.alive = False

    def resurrect(self):
        self.alive = True

    def getX(self):
        # print(self.x)
        return self.x

    def getY(self):
        # print(self.y)
        return self.y

    def getImg(self):
        return self.img

    def getWidth(self):
        # print(self.width)
        return self.width

    def getHeight(self):
        # print(self.height)
        return self.height

    def getX1(self):
        # print(self.x + self.width)
        return self.x + self.width

    def getY1(self):
        # print(self.y + self.height)
        return self.y + self.height

    def setXY(self, newX, newY):
        self.setX(newX)
        self.y = newY

    def setX(self, newX):
        self.x = newX

    def setSpeed(self, speed):
        self.speed = speed

    def getState(self):
        # either running or waiting
        return self.start

    # the 2 functions down are important to define when the unicorn will cross
    def Start(self):
        self.start = True

    def stop(self):
        self.start = False

    # every time the unicorn crosses the road this variable will be incremented by 1
    # if its value is an even number then the animal is going to the right direction
    # else - left
    def cross(self):
        self.crosses += 1

    def getCrosses(self):
        return self.crosses

    def getSpeed(self):
        return self.speed

    def setImg(self, nameOfImg):
        address = "images/"
        extension = ".gif"
        self.img = PhotoImage(file=address + nameOfImg + extension)


def configure_window():
    global windowWidth, windowHeight, openspaceY, openspaceY1, openspaceX, openspaceX1
    window.geometry("1024x768")
    window.configure(background="black")
    window.title("Lost in the forest")
    windowWidth = 1024
    windowHeight = 768

    # The comments below represent the ration between the size of the window
    # and the size of the open space /.gif/
    # The open space is where the unicorn crosses the road
    # 1024px / 426 = 2.4037558685
    # 1024px / 567 = 1.8059964727
    # 768px  / 210 = 3.6571428571
    # 768px  / 307 = 2.5016286645
    openspaceX = windowWidth / 2.4037558685
    openspaceX1 = windowWidth / 1.8059964727
    openspaceY = windowHeight / 3.6571428571
    openspaceY1 = windowHeight / 2.5016286645


# This function moves your player with step ahead
def stepOn(event):
    global walk, steps
    walk += 1
    steps += 1
    canvas.itemconfig(stepsLabel, text="Steps: " + str(steps))
    if walk == 1:
        canvas.itemconfig(movement, image=leftUp)
    elif walk == 2:
        canvas.itemconfig(movement, image=rightUp)
        walk = 0
    canvas.update()


# At the end of the road in the woods between the trees there is open space
# which will be crossed by the unicorn.
# This function will check if the animal is on the road
def isHidden(headX, headX1, headY, headY1):
    if unicorn.getCrosses() % 2 == 0:
        if (
            headX1 >= openspaceX
            and headX <= openspaceX1
            and headY >= openspaceY
            and headY1 <= openspaceY1
        ):
            return False
    else:
        # print(str(headX1) + "  " + str(headX))
        # print(str(openspaceX1) + "  " + str(openspaceX))
        if (
            headX >= openspaceX
            and headX1 <= openspaceX1
            and headY >= openspaceY
            and headY1 <= openspaceY1
        ):
            return False
    return True


# Check whether you have shot the unicorn in the head
def isShot(mouseX, mouseY, headX, headX1, headY, headY1):
    # global money
    # print(str(mouseX) + " " + str(mouseY) + " " + str(headX) + " " + str(headX1) + " " + str(headY) + " " + str(headY1))
    if mouseX >= headX and mouseX <= headX1 and mouseY >= headY and mouseY <= headY1:
        unicorn.die()
        # money = 100
        # canvas.itemconfig(moneyLabel, text = "Money: " + str(money))


# This function compared to the previous one checks whether any part of the unicorn is hit
def isShot1(event):
    if (
        event.x >= unicorn.getX()
        and event.x <= unicorn.getX1()
        and event.y >= unicorn.getY()
        and event.y <= unicorn.getY1()
    ):
        # the shot wont kill the unicorn but we set dead to 1 to produce the impact
        unicorn.die()


# Takes the event of clicking on the screen and calls isShot()
def shoot(event):
    # global bullets
    # print("mouse clicked at: ", event.x, event.y)
    # bullets -= 1
    # canvas.itemconfig(bulletsLabel, text = "Bullets: " + str(bullets))
    if unicorn.getCrosses() % 2 == 0:
        headX = unicorn.getX() + unicorn.getWidth() * 75 / 100
        headY = unicorn.getY() + unicorn.getHeight() * 10 / 60
        headY1 = headY + unicorn.getHeight() * 16 / 60
        if not isHidden(headX, unicorn.getX1(), headY, headY1):
            isShot(event.x, event.y, headX, unicorn.getX1(), headY, headY1)
    else:
        headX1 = unicorn.getX() + unicorn.getWidth() * 25 / 100
        headY = unicorn.getY() + unicorn.getHeight() * 10 / 60
        headY1 = headY + unicorn.getHeight() * 16 / 60
        if not isHidden(unicorn.getX(), headX1, headY, headY1):
            isShot(event.x, event.y, unicorn.getX(), headX1, headY, headY1)


# This function moves the unicorn from left to right or the opposite respectively
def unicorn_move():
    if unicorn.getCrosses() % 2 == 0:
        canvas.move(canvasUnicorn, unicorn.getSpeed(), 0)
        unicorn.setX(unicorn.getX() + unicorn.getSpeed())
        # When the tail of the unicorn is behind the trees, it is turned around
        if unicorn.getX() >= openspaceX1:
            unicorn.cross()
            unicorn.setImg("unicornToLeft")
            canvas.itemconfig(canvasUnicorn, image=unicorn.getImg())
    else:
        canvas.move(canvasUnicorn, -unicorn.getSpeed(), 0)
        unicorn.setX(unicorn.getX() - unicorn.getSpeed())
        if unicorn.getX1() <= openspaceX:
            unicorn.cross()
            unicorn.setImg("unicornToRight")
            canvas.itemconfig(canvasUnicorn, image=unicorn.getImg())
    canvas.update()


# All the events are in sequence.
def story():
    global magicianCome, gamePhase, chase, steps, decision

    if gamePhase == "interactL":
        messagebox.showinfo("Information", message[0])
        canvas.focus_set()
        gamePhase = "magician"

    elif gamePhase == "magician":
        if steps == magicianCome + 1:
            if magicianCome < len(magician) - 1:
                magicianCome += 1

            canvas.itemconfig(canvasMagician, image=magician[magicianCome])
            canvas.itemconfig(canvasMagician, state="normal")
            canvas.move(canvasMagician, 0, windowHeight / 48)
            canvas.unbind("<Button-1>")

            if magicianCome == len(magician) - 1:
                gamePhase = "interactM"
                # I am going to reuse that variable for the welcome sign
                magicianCome = 0
        else:
            canvas.bind("<space>", stepOn)

    elif gamePhase == "interactM":
        messagebox.showinfo("Information", message[1])
        canvas.focus_set()
        # Walk after the magician
        gamePhase = "walkM"

    elif gamePhase == "walkM":
        canvas.itemconfig(canvasMagician, state="hidden")
        gamePhase = "welcome"

    elif gamePhase == "welcome":
        # Reusing the previous variable
        if steps == magicianCome + 10:
            if magicianCome < len(welcome) - 1:
                magicianCome += 1

            canvas.itemconfig(canvasSign, image=welcome[magicianCome])
            canvas.itemconfig(canvasSign, state="normal")
            canvas.move(canvasSign, 0, windowHeight / 48)
            canvas.unbind("<Button-1>")

            if magicianCome == len(welcome) - 1:
                gamePhase = "interactS"
        else:
            canvas.bind("<space>", stepOn)

    elif gamePhase == "interactS":
        messagebox.showinfo("Information", message[2])
        canvas.focus_set()
        # Walk after the sign
        gamePhase = "walkS"

    elif gamePhase == "walkS":
        canvas.itemconfig(canvasSign, state="hidden")
        # Interact with the unicorn
        gamePhase = "interactU"

    elif gamePhase == "interactU":
        if steps >= 17:
            messagebox.showinfo("Information", message[3])
            canvas.focus_set()
            # Walk after the sign
            gamePhase = "uniWalk"
        else:
            canvas.bind("<space>", stepOn)

    elif gamePhase == "uniWalk" and steps >= 20 and unicorn.getCrosses() % 2 == 0:
        unicorn.Start()
        # Player stops moving when unicorn shows up
        canvas.unbind("<space>")
        canvas.itemconfig(movement, image=stance)
        unicorn_move()
        # Shoot
        canvas.bind("<Button-1>", isShot1)
        # if shot => then start running and hiding
        if not unicorn.getStatus():
            canvas.unbind("<Button-1>")
            unicorn.resurrect()
            unicorn.setSpeed(unicorn.getSpeed() * 3)
            decision = True
        # print(openspaceX1, unicorn.getX())
        if openspaceX1 <= unicorn.getX():
            if decision:
                # Either kill
                gamePhase = "interactShot"
                time.sleep(1)
            else:
                # Or follow it
                gamePhase = "followUni0"

    elif gamePhase == "interactShot":
        messagebox.showinfo("Information", message[4])
        canvas.focus_set()
        # Walk after the sign
        gamePhase = "chase1"

    # Run from right to left
    elif gamePhase == "chase1":
        if steps <= chase:
            canvas.bind("<space>", stepOn)
        else:
            canvas.unbind("<space>")
            canvas.itemconfig(movement, image=stance)
            unicorn_move()
            # Shoot
            canvas.bind("<Button-1>", shoot)
            if openspaceX >= unicorn.getX1():
                gamePhase = "chase2"
                chase += rand(3, 7)
                unicorn.setSpeed(unicorn.getSpeed() * 0.8)

    # Run from left to right
    elif gamePhase == "chase2":
        if steps <= chase:
            canvas.bind("<space>", stepOn)
        else:
            canvas.unbind("<space>")
            canvas.itemconfig(movement, image=stance)
            unicorn_move()
            # Shoot
            canvas.bind("<Button-1>", shoot)
            if openspaceX1 <= unicorn.getX():
                gamePhase = "chase1"
                chase += rand(3, 7)
                unicorn.setSpeed(unicorn.getSpeed() * 0.98)

    elif gamePhase == "followUni0":
        messagebox.showinfo("Information", message[7])
        canvas.focus_set()
        # Walk after the sign
        gamePhase = "followUni1"

    elif gamePhase == "followUni1":
        if steps <= chase:
            canvas.bind("<space>", stepOn)
        else:
            unicorn.setSpeed(8)
            unicorn_move()
            canvas.unbind("<space>")
            canvas.unbind("<Button-1>")
            canvas.itemconfig(movement, image=stance)
            if openspaceX >= unicorn.getX1():
                chase += rand(3, 7)
                if steps >= 40:
                    gamePhase = "survive"
                else:
                    gamePhase = "followUni2"

    elif gamePhase == "followUni2":
        if steps <= chase:
            canvas.bind("<space>", stepOn)
        else:
            unicorn_move()
            canvas.unbind("<space>")
            canvas.unbind("<Button-1>")
            canvas.itemconfig(movement, image=stance)
            if openspaceX1 <= unicorn.getX():
                chase += rand(3, 7)
                if steps >= 40:
                    gamePhase = "survive"
                else:
                    gamePhase = "followUni1"

    elif gamePhase == "survive":
        # canvas.itemconfig(forestBack, state = "hidden")
        canvas.itemconfig(sky, image=sunny)
        canvas.unbind("<space>")
        canvas.itemconfig(movement, image=stance)
        time.sleep(1)
        gamePhase = "gameWon"
        messagebox.showinfo("Information", message[6])

    canvas.update()


# This function is to mark the ending of the game
def fallingStars():
    # default size
    points = [
        10,
        40,
        40,
        40,
        50,
        10,
        60,
        40,
        90,
        40,
        65,
        60,
        75,
        90,
        50,
        70,
        25,
        90,
        35,
        60,
    ]
    # customized size
    for i in range(len(points)):
        points[i] = points[i] / 2
    stars = [points for i in range(25)]
    canvasStar = [None] * 25
    for star in stars:
        for i in range(len(star)):
            star[i] += 2
        time.sleep(0.12)
        canvasStar[stars.index(star)] = canvas.create_polygon(star, fill="yellow")
        canvas.update()
    # Tried to hide the stars but it does not work as intended
    for i in range(25):
        # canvas.itemconfig(canvasStar[i], state = "hidden")
        canvas.update()


def Continue():
    global pause
    pauseCanvas.pack_forget()
    canvas.pack()
    canvas.focus_set()
    pause = False


def saveUpdate():
    global textSave, save
    file = open("textFiles/save.txt", "r")
    textSave = (
        str(magicianCome)
        + "\n"
        + str(gamePhase)
        + "\n"
        + str(chase)
        + "\n"
        + str(steps)
        + "\n"
        + str(decision)
    )
    textSave = textSave.strip()
    text1 = file.read()
    file.close()

    # print(textSave+'\n'+text1)
    if text1 != textSave:
        saveButton.configure(text="Save Game")
        save = True
    else:
        saveButton.configure(text="Saved")
        save = False
    pauseCanvas.update()


def Save():
    # write these variables: magicianCome, gamePhase, chase, steps, decision
    time.sleep(0.5)
    if save:
        file = open("textFiles/save.txt", "w")
        file.write(textSave)
        file.close()
    saveUpdate()
    pauseCanvas.update()


def Quit():
    time.sleep(0.5)
    window.destroy()


def Pause():
    global pause
    pause = True
    canvas.pack_forget()
    pauseCanvas.pack()
    pauseCanvas.focus_set()
    # Whenever Pause menu is brought up, check whether variables are updated
    saveUpdate()
    pauseCanvas.update()


def bossKey(event):
    Pause()
    window.iconify()


def Game():
    entryCanvas.pack_forget()
    canvas.pack()
    canvas.focus_set()
    while True:
        canvas.update()
        # Implementing BOSS KEY
        canvas.bind("<Tab>", bossKey)
        if not unicorn.getStatus():
            canvas.itemconfig(sky, image=red)
            time.sleep(2)
            canvas.itemconfig(canvasUnicorn, state="hidden")
            fallingStars()
            messagebox.showinfo("Information", message[5])
        if gamePhase == "gameLost" or gamePhase == "gameWon":
            Quit()
        else:
            story()


def New():
    global user
    menuCanvas.pack_forget()
    entryCanvas.pack()
    entry = Entry(window)
    entryCanvas.create_window(windowWidth / 2, windowHeight / 2, window=entry)
    user = entry.get()
    print(user)
    buttonEntry = Button(window, text="Type your username:", command=Game())
    entryCanvas.create_window(
        windowWidth / 2, windowHeight / 2 + 35, window=buttonEntry
    )


file = open("textFiles/textFile1.txt", "r")
message[0] = file.read()
file.close()
file = open("textFiles/textFile2.txt", "r")
message[1] = file.read()
file.close()
file = open("textFiles/textFile3.txt", "r")
message[2] = file.read()
file.close()
file = open("textFiles/textFile4.txt", "r")
message[3] = file.read()
file.close()
file = open("textFiles/textFile5.txt", "r")
message[4] = file.read()
file.close()
file = open("textFiles/textFile6.txt", "r")
message[5] = file.read()
file.close()
file = open("textFiles/textFile7.txt", "r")
message[6] = file.read()
file.close()
file = open("textFiles/textFile8.txt", "r")
message[7] = file.read()
file.close()

unicorn = Unicorn()

# create the main window
window = Tk()
configure_window()

# MENU MAIN
menuCanvas = Canvas(window, width=windowWidth, height=windowHeight, background="black")


entryCanvas = Canvas(window, width=windowWidth, height=windowHeight, background="black")
canvas = Canvas(window, width=windowWidth, height=windowHeight, background="green")
canvas.pack()
pauseCanvas = Canvas(window, width=windowWidth, height=windowHeight, background="black")


# BUTTONS
newGameButton = Button(window, text="New Game", command=New)
newGameButton.configure(borderwidth=2, bg="white", width=int(windowWidth / 100))
newGameButton_window = menuCanvas.create_window(
    windowWidth / 2, windowHeight / 2, window=newGameButton
)


# All the used images are loaded here
leftUp = PhotoImage(file="images/leftFront.gif")
rightUp = PhotoImage(file="images/rightFront.gif")
stance = PhotoImage(file="images/stance.gif")
forest = PhotoImage(file="images/forest.gif")
forestBack = PhotoImage(file="images/forestBack.gif")
way = PhotoImage(file="images/way.gif")
sunny = PhotoImage(file="images/sunny.gif")
dark = PhotoImage(file="images/dark.gif")
red = PhotoImage(file="images/red.gif")
magician = [
    PhotoImage(file="images/magician0.gif"),
    PhotoImage(file="images/magician1.gif"),
    PhotoImage(file="images/magician2.gif"),
    PhotoImage(file="images/magician3.gif"),
]
# PhotoImage(file = "images/magician.gif")]
welcome = [
    PhotoImage(file="images/welcome0.gif"),
    PhotoImage(file="images/welcome1.gif"),
    PhotoImage(file="images/welcome2.gif"),
    PhotoImage(file="images/welcome3.gif"),
]

####################################

# The images are positioned on the canvas here
canvas.create_image(windowWidth / 2, windowHeight / 2, image=way)
sky = canvas.create_image(windowWidth / 2, windowHeight / 2, image=dark)
canvas.create_image(windowWidth / 2, windowHeight / 2, image=forestBack)
# Unicorn
unicorn.create(
    windowWidth / 3 - windowWidth / 10, windowHeight / 3, 100, 60, 5, "unicornToRight"
)
canvasUnicorn = canvas.create_image(
    unicorn.getX() + unicorn.getWidth() / 2,
    unicorn.getY() + unicorn.getHeight() / 2,
    image=unicorn.getImg(),
)
canvas.create_image(windowWidth / 2, windowHeight / 2, image=forest)
movement = canvas.create_image(windowWidth / 2, windowHeight / 2, image=stance)
# Create and hide the magician until the player reaches him
canvasMagician = canvas.create_image(
    windowWidth / 2,
    windowHeight / 2 - windowHeight * (magicianCome + 1) / 6,
    image=magician[0],
)
canvas.itemconfig(canvasMagician, state="hidden")
canvasSign = canvas.create_image(
    windowWidth / 2,
    windowHeight / 2 - windowHeight * (magicianCome + 1) / 6,
    image=welcome[0],
)
canvas.itemconfig(canvasSign, state="hidden")

# BUTTONS OF PAUSE
# They will not be packed until pause button is pressed
# If it is pressed, game canvas is forgot and the other adre packed
pauseButton = Button(window, text="Pause", command=Pause)
pauseButton.configure(borderwidth=2, bg="brown")
pauseButton_window = canvas.create_window(
    windowWidth * 9 / 10, windowHeight / 10, window=pauseButton
)
# pauseButton.pack()

saveButton = Button(window, text="Save Game", command=Save)
saveButton.configure(borderwidth=2, bg="white", width=int(windowWidth / 100))
saveButton_window = pauseCanvas.create_window(
    windowWidth / 2, windowHeight / 2, window=saveButton
)
# saveButton.pack_forget()

continueButton = Button(window, text="Continue", command=Continue)
continueButton.configure(borderwidth=2, bg="white", width=int(windowWidth / 100))
continueButton_window = pauseCanvas.create_window(
    windowWidth / 2, windowHeight / 2 + 25, window=continueButton
)
# continueButton.pack_forget()

quitButton = Button(window, text="Quit Game", command=Quit)
quitButton.configure(borderwidth=2, bg="white", width=int(windowWidth / 100))
quitButton_window = pauseCanvas.create_window(
    windowWidth / 2, windowHeight / 2 + 25 + 25, window=quitButton
)
# quitButton.pack_forget()
####################################

# Place the Score label next to each other on top of window
# moneyLabel = canvas.create_text(windowWidth/2 - windowWidth/8, 10, fill = "white", text="Money: " + str(money), font=("Arial Bold",15))
# bulletsLabel = canvas.create_text(windowWidth/2 , 10, fill = "white", text="Bullets: " + str(bullets), font=("Arial Bold",15))
stepsLabel = canvas.create_text(
    windowWidth / 2,
    10,
    fill="white",
    text="Steps: " + str(steps),
    font=("Arial Bold", 15),
)
Game()

window.mainloop()
