'''
Created on Mar 7, 2014

@author: alexwang
'''
#include <wx/wx.h>

# simple.py

import wx
import random
import math
BoardWidth = 40
BoardHeight = 40
Width = 400
Height = 400
Speed = 100
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
        self.snake=Snake(19,19)
        self.food=Food(14,19)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.SetBackgroundColour('#ffffff')
        self.direction=Direction.Left
        self.Bind(wx.EVT_KEY_DOWN,self.onKeyDown)
        self.Bind(wx.EVT_TIMER,self.makeMove,id=Board.ID_TIMER)
        print "reached"
        self.Refresh()
        self.isPaused=False
    
    def start(self):
        self.timer.Start(Speed)
    
    def gameOver(self):
        self.snake=Snake(19,19)
        self.food=Food(14,19)
        self.direction=Direction.Left
        
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
            self.food=Food(math.trunc(random.random()*BoardWidth),math.trunc(random.random()*BoardHeight))
        self.Refresh()
        print self.snake.loc
                                        
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
        return wx.GetTopLevelParent(self).GetClientSize().GetHeight() / BoardHeight 
    
    def squareWidth(self):
        return wx.GetTopLevelParent(self).GetClientSize().GetWidth() / BoardWidth 
    
    def OnPaint(self,event):
        dc=wx.PaintDC(self)
        for point in self.snake.loc:
            self.drawSquare(dc,(point[0])*self.squareWidth(),(point[1])*self.squareHeight(),self.squareWidth(),self.squareHeight(),0)
        self.drawSquare(dc,(self.food.x)*self.squareWidth(),(self.food.y)*self.squareHeight(),self.squareWidth(),self.squareHeight(),1)
            
    def drawSquare(self,dc,x,y,w,h,shape):
        color=['#000000','#F0E68C']
        pen=wx.Pen(color[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush(color[shape]))
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