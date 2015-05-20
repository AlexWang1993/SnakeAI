'''
Created on Mar 7, 2014

@author: alexwang
'''
#include <wx/wx.h>

# simple.py

import wx
import random
import math
import SnakeAI
from sets import Set

BoardWidth = 13
BoardHeight = 13
Width = 300
Height = 300
Speed = 5
Ratio = 0.8
class Direction:
    Left=0
    Right=1
    Up=2
    Down=3
    
class SnakeGame(wx.Frame):
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(Width,Height))
        self.statusbar=self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.board.SetFocus()
        self.board.start()
        self.Centre()
        self.Show()
        

class Board(wx.Panel):
    

    ID_TIMER=1
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.timer = wx.Timer(self, Board.ID_TIMER)
        self.snake=Snake((BoardWidth-1)/2,(BoardHeight-1)/2)
        self.food=Food(max((BoardWidth-1)/2-5,0),(BoardHeight-1)/2)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.SetBackgroundColour('#ffffff')
        self.direction=Direction.Left
        self.snakeAI=SnakeAI.SnakeAI(BoardWidth,BoardHeight,self.food.position(),self.snake.loc)
        self.Bind(wx.EVT_KEY_DOWN,self.onKeyDown)
        self.Bind(wx.EVT_TIMER,self.makeMove,id=Board.ID_TIMER)
        print "reached"
        self.Refresh()
        self.isPaused=False
    
    def start(self):
        self.timer.Start(Speed)
        self.pause()
    
    def gameOver(self):
        self.pause()
        self.snake=Snake((BoardWidth-1)/2,(BoardHeight-1)/2)
        self.food=Food(max((BoardWidth-1)/2-5,0),(BoardHeight-1)/2)
        self.direction=Direction.Left
        self.snakeAI=SnakeAI.SnakeAI(BoardWidth,BoardHeight,self.food.position(),self.snake.loc)
        
    def pause(self):
        self.timer.Stop()
    
    def resume(self):
        self.timer.Start() 
           
    def onKeyDown(self,event):
        if event.GetKeyCode()==wx.WXK_SPACE:
            if self.isPaused:
                self.resume()
                self.isPaused=False
            else:
                self.pause()
                self.isPaused=True
        else:
            self.setDirection(event)
            
    def makeMove(self,event):
        self.direction=self.snakeAI.chooseDirection()
        if self.direction==Direction.Up:
            if not(self.snake.moveUp()):
                self.gameOver()
        if self.direction==Direction.Down:
            if not(self.snake.moveDown()):
                self.gameOver()
        if self.direction==Direction.Left:
            if not(self.snake.moveLeft()):
                self.gameOver()
        if self.direction==Direction.Right:
            if not(self.snake.moveRight()):
                self.gameOver()
        if self.touchedFood():
            self.snake.grow()
            if len(self.snake.loc)==BoardWidth*BoardHeight:
                self.pause()
            else:
                newFoodLoc=self.generateFoodLoc()[0]
                self.food=Food(newFoodLoc[0],newFoodLoc[1])
                self.snakeAI.updateFood(self.food.position())
        self.Refresh()
        ##print self.snake.loc
        
    def generateFoodLoc(self):
        goodPoints=Set()
        for i in range(0,BoardWidth):
            for j in range(0,BoardHeight):
                goodPoints.add((i,j))
        try:
            for i in self.snake.loc:
                goodPoints.remove(i)
        except KeyError:
            pass
        return random.sample(goodPoints,1)      
                            
    def setDirection(self,event):
        key=event.GetKeyCode()
        if key==wx.WXK_UP:
            self.direction=Direction.Up
        elif key==wx.WXK_DOWN:
            self.direction=Direction.Down
        elif key==wx.WXK_LEFT:
            self.direction=Direction.Left
        elif key==wx.WXK_RIGHT:
            self.direction=Direction.Right
            
    def touchedFood(self):
        return self.food.position()==self.snake.position()  
       
    def squareHeight(self):
        return math.trunc(  wx.GetTopLevelParent(self).GetClientSize().GetHeight() / BoardHeight )
    
    def squareWidth(self):
        return math.trunc(  wx.GetTopLevelParent(self).GetClientSize().GetWidth() / BoardWidth )
    
    def translateDirection(self,u,v):
        w=(v[0]-u[0],v[1]-u[1])
        if (w==(1,0)):
            return Direction.Right
        elif (w==(-1,0)):
            return Direction.Left
        elif (w==(0,1)):
            return Direction.Down
        elif (w==(0,-1)):
            return Direction.Up
    
    def drawSnake(self,dc):
        for i in range(0,len(self.snake.loc)-1):
            dirt=self.translateDirection(self.snake.loc[i], self.snake.loc[i+1])
            x=self.snake.loc[i][0]*self.squareWidth()
            y=self.snake.loc[i][1]*self.squareHeight()

            if dirt==Direction.Right:
                self.drawSquare(dc, x + (1-Ratio)/2*self.squareWidth(), y + (1-Ratio)/2*self.squareHeight(), self.squareWidth()*(1+Ratio), self.squareHeight()*Ratio, 0, 0)
            if dirt==Direction.Left:
                self.drawSquare(dc, x - (1-(1-Ratio)/2)*self.squareWidth(), y + (1-Ratio)/2*self.squareHeight(), self.squareWidth()*(1+Ratio), self.squareHeight()*Ratio, 0, 0)
            if dirt==Direction.Down:
                self.drawSquare(dc, x + (1-Ratio)/2*self.squareWidth(), y + (1-Ratio)/2*self.squareHeight(), self.squareWidth()*Ratio, self.squareHeight()*(1+Ratio), 0, 0)
            if dirt==Direction.Up:
                self.drawSquare(dc, x + (1-Ratio)/2*self.squareWidth(), y - (1-(1-Ratio)/2)*self.squareHeight(), self.squareWidth()*Ratio, self.squareHeight()*(1+Ratio), 0, 0)
                                
    def OnPaint(self,event):
        dc=wx.PaintDC(self)
        self.drawSnake(dc)
        self.drawHead(dc,(self.snake.loc[0][0])*self.squareWidth()+(1-Ratio)/2*self.squareWidth(),(self.snake.loc[0][1])*self.squareHeight()+(1-Ratio)/2*self.squareHeight(),self.squareWidth()*Ratio,self.squareHeight()*Ratio)
        #for i in range(1,len(self.snake.loc)):
        #    point = self.snake.loc[i]
        #    self.drawSquare(dc,(point[0])*self.squareWidth(),(point[1])*self.squareHeight(),self.squareWidth(),self.squareHeight(),0,shape2=2)
        self.drawSquare(dc,(self.food.x)*self.squareWidth()+(1-Ratio)/2*self.squareWidth(),(self.food.y)*self.squareHeight()+(1-Ratio)/2*self.squareHeight(),self.squareWidth()*Ratio,self.squareHeight()*Ratio,1)
            
    def drawSquare(self,dc,x,y,w,h,shape,shape2=0):
        color=['#000000','#F0E68C', '#0099FF']
        pen=wx.Pen(color[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush(color[shape]))
        dc.DrawRectangle(x,y,w,h)
    
    def drawHead(self,dc,x,y,w,h):
        pen=wx.Pen('#0099FF')
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush('#6666FF'))
        dc.DrawRectangle(x,y,w,h)
            
        
class Snake():
    def __init__(self,x,y):
        self.loc=[(x,y),(x+1,y),(x+2,y),(x+3,y),(x+4,y)]

    def shape(self):
        return self.loc
    
    def position(self):
        return self.loc[0]
      
    def checkConflict(self):
        if (self.loc[0][0]<0) or (self.loc[0][1]<0) or (self.loc[0][0]>=BoardWidth) or (self.loc[0][1]>=BoardHeight):
            return False
        for i in range(1,len(self.loc)):
            if self.loc[i]==self.loc[0]:
                return False
        return True
            
    def moveDown(self):
        self.lastOne=self.loc.pop(len(self.loc)-1)
        firstOne=(self.loc[0][0],self.loc[0][1]+1)
        self.loc.insert(0, firstOne)
        return self.checkConflict()
    
    def moveUp(self):
        self.lastOne=self.loc.pop(len(self.loc)-1)
        firstOne=(self.loc[0][0],self.loc[0][1]-1)
        self.loc.insert(0, firstOne)
        return self.checkConflict()

    def moveRight(self):
        self.lastOne=self.loc.pop(len(self.loc)-1)
        firstOne=(self.loc[0][0]+1,self.loc[0][1])
        self.loc.insert(0, firstOne)
        return self.checkConflict()
    
    def moveLeft(self):
        self.lastOne=self.loc.pop(len(self.loc)-1)
        firstOne=(self.loc[0][0]-1,self.loc[0][1])
        self.loc.insert(0, firstOne)
        return self.checkConflict()  
    
    def grow(self):
        self.loc.append(self.lastOne)         
        
class Food():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def position(self):
        return (self.x,self.y)


if __name__=="__main__":
    app=wx.App()
    SnakeGame(None,-1,"SNAKE")
    app.MainLoop()