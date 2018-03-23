from  tkinter import *
import time
import random

root = Tk()

class Ball:
    def __init__(self,mycanvas):
        self.cv = mycanvas
        self.velocityx = 1
        self.velocityy = 1
        self.ballsize = 50
        self.canvas_height = int(self.cv.cget("height"))
        self.canvas_width = int(self.cv.cget("width"))
        self.create_ball()


    def move_ball(self):

        fpsinterval = int(1000/60)  # 60fps

        topx,topy,bottomx,bottomy = self.cv.coords(self.ball)
        if (int(bottomy) >= self.canvas_height ):
            self.velocityy = -self.velocityy
        elif (int(topy) <= 0):
            self.velocityy = -(self.velocityy)


        topx, topy, bottomx, bottomy = self.cv.coords(self.ball)
        # if ball intersecting paddle , bounce

        if len(self.cv.find_overlapping(topx, topy, bottomx, bottomy)) > 1 :
            self.velocityx = -self.velocityx

        self.cv.move(self.ball, self.velocityx, self.velocityy)

        # if ball outside frame , center ball
        if bottomx < 0 or topx > self.canvas_width:
            self.center_ball()

        self.cv.after(fpsinterval, self.move_ball)

    def center_ball(self):
        topx, topy, bottomx, bottomy = self.cv.coords(self.ball)
        velocityx = int(self.canvas_width/2 - topx)
        velocityy = int(self.canvas_height/2 - topy)
        self.cv.move(self.ball, velocityx, velocityy)


    def create_ball(self):
        cv_cntrh = self.canvas_height /2
        cv_cntrw = self.canvas_width /2
        halfball = self.ballsize /2
        self.ball = self.cv.create_oval(cv_cntrh - halfball, cv_cntrw - halfball,
                                        cv_cntrh + halfball, cv_cntrw + halfball,
                                        fill="black")

class Paddle:
    def __init__(self, mycanvas, align):
        self.cv = mycanvas
        self.canvas_height = int(self.cv.cget("height"))
        self.canvas_width = int(self.cv.cget("width"))
        cv_cntrh = self.canvas_height /2
        width = 20
        height = 60

        if align == "right":
            offset = self.canvas_width
            self.paddle = self.cv.create_rectangle(offset - width, cv_cntrh - height / 2,
                                                   offset, cv_cntrh + height / 2,
                                                   fill="black")

        if align == "left":
            offset = 0
            self.paddle = self.cv.create_rectangle( offset, cv_cntrh - height/2,
                                                offset + width, cv_cntrh + height / 2,
                                                fill="black")


class ComputerPaddle(Paddle):

    def __init__(self,mycanvas ,trackball):
        Paddle.__init__(self,mycanvas,align="right")
        self.trackedball = trackball.ball
        self.pvelocity = 1



    def move_paddle(self):
        fpsinterval = int(1000 / 60)
        _, btopy, _, bbottomy = self.cv.coords(self.trackedball)
        _,ptopy,_, pbottomy = self.cv.coords(self.paddle)

        delta = int(btopy - ptopy)
        self.cv.move(self.paddle, 0, delta)

        self.cv.after(fpsinterval, self.move_paddle)


class UserPaddle(Paddle):
    def __init__(self,mycanvas):
        Paddle.__init__(self,mycanvas,align="left")
        self.cv.bind("<Up>", self.up)
        self.cv.bind("<Down>", self.down)
        self.cv.focus_set()

    def up(self,event):
        self.cv.move(self.paddle, 0, -10)

    def down(self,event):
        self.cv.move(self.paddle, 0, 10)


class Game:
    def __init__(self,rootframe):
        self.cv = Canvas(rootframe, width=600, height=600)
        self.cv.pack()
        self.userpaddle = UserPaddle(self.cv)
        self.ball = Ball(self.cv)
        self.computerpaddle = ComputerPaddle(self.cv,self.ball)

    def start(self):
        self.ball.move_ball()
        self.computerpaddle.move_paddle()


game = Game(root)
game.start()
root.mainloop()
