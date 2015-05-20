'''
Created on Mar 8, 2014

@author: alexwang
'''
import snake
from sets import Set
import copy
import math
import random
class SnakeAI:
    def __init__(self,width,height,foodLoc,snakeLocArray):
        self.width=width
        self.height=height
        self.foodLoc=foodLoc
        self.snakeLoc=snakeLocArray
        self.inBadPosition=0
    
    def updateFood(self,foodLoc):
        self.foodLoc=foodLoc
    
    def safePathToFood(self):
        f=[[-1 for i in range(0,self.width)] for i in range(0,self.height)]
        prev=[[-1 for i in range(0,self.width)] for i in range(0,self.height)]
        for i in range(0,len(self.snakeLoc)):
            j=self.snakeLoc[i]
            f[j[0]][j[1]]=0
        q=[-1 for i in range(0,self.width*self.height)]
        q[0]=self.snakeLoc[0]
        l=0
        r=0
        while l<=r:
            v=q[l]
            if (v[0]+1<self.width)and(f[v[0]+1][v[1]]==-1):
                r+=1
                u=(v[0]+1,v[1])
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1
                prev[u[0]][u[1]]=v
            if (v[0]-1>=0)and(f[v[0]-1][v[1]]==-1):
                r+=1
                u=(v[0]-1,v[1])
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1
                prev[u[0]][u[1]]=v
                
            if (v[1]+1<self.height)and(f[v[0]][v[1]+1]==-1):
                r+=1
                u=(v[0],v[1]+1)
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1
                prev[u[0]][u[1]]=v                
            if (v[1]-1>=0)and(f[v[0]][v[1]-1]==-1):
                r+=1
                u=(v[0],v[1]-1)
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1
                prev[u[0]][u[1]]=v     
            l+=1
        
        if f[self.foodLoc[0]][self.foodLoc[1]]==-1:
            return False
        
        g=[[-1 for i in range(0,self.width)] for i in range(0,self.height)]
        leftSize=len(self.snakeLoc)+1
        v=self.foodLoc
        nextStep=0
        while not (v==self.snakeLoc[0]) and (leftSize>0):
            nextStep=v
            if leftSize>1:
                g[v[0]][v[1]]=0
            snakeEnd=v
            v=prev[v[0]][v[1]] 
            leftSize-=1
        while not (v==self.snakeLoc[0]):
            nextStep=v
            v=prev[v[0]][v[1]] 
    
        for i in range(0,len(self.snakeLoc)):
            j=self.snakeLoc[i]
            if leftSize>1:x
                g[j[0]][j[1]]=0   
            snakeEnd=j
            leftSize-=1
            if leftSize==0:
                break 
        print snakeEnd    
        l=0
        r=0
        q[0]=self.foodLoc
        while l<=r:
            v=q[l]
            if (v[0]+1<self.width)and(g[v[0]+1][v[1]]==-1):
                r+=1
                u=(v[0]+1,v[1])
                q[r]=u
                g[u[0]][u[1]]=g[v[0]][v[1]]+1

            if (v[0]-1>=0)and(g[v[0]-1][v[1]]==-1):
                r+=1
                u=(v[0]-1,v[1])
                q[r]=u
                g[u[0]][u[1]]=g[v[0]][v[1]]+1

                
            if (v[1]+1<self.height)and(g[v[0]][v[1]+1]==-1):
                r+=1
                u=(v[0],v[1]+1)
                q[r]=u
                g[u[0]][u[1]]=g[v[0]][v[1]]+1
              
            if (v[1]-1>=0)and(g[v[0]][v[1]-1]==-1):
                r+=1
                u=(v[0],v[1]-1)
                q[r]=u
                g[u[0]][u[1]]=g[v[0]][v[1]]+1
            l+=1

        if g[snakeEnd[0]][snakeEnd[1]]==-1:
            return False
        return nextStep
         
        
    def lengthCatchEnd(self,snakeLoc):       
        f=[[-1 for i in range(0,self.width)] for i in range(0,self.height)]
        for i in range(1,len(self.snakeLoc)):
            j=snakeLoc[i]
            f[j[0]][j[1]]=0
        q=[-1 for i in range(0,self.width*self.height)]
        q[0]=snakeLoc[len(snakeLoc)-1]
        l=0
        r=0
        while l<=r:
            v=q[l]
            if (v[0]+1<self.width)and(f[v[0]+1][v[1]]==-1):
                r+=1
                u=(v[0]+1,v[1])
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1

            if (v[0]-1>=0)and(f[v[0]-1][v[1]]==-1):
                r+=1
                u=(v[0]-1,v[1])
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1
                
            if (v[1]+1<self.height)and(f[v[0]][v[1]+1]==-1):
                r+=1
                u=(v[0],v[1]+1)
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1
             
            if (v[1]-1>=0)and(f[v[0]][v[1]-1]==-1):
                r+=1
                u=(v[0],v[1]-1)
                q[r]=u
                f[u[0]][u[1]]=f[v[0]][v[1]]+1

            l+=1
            
        snakeHead=snakeLoc[0]
        '''if f[snakeHead[0]][snakeHead[1]]==-1:
            return False'''
        return f[snakeHead[0]][snakeHead[1]]
 
    def pathToEnd(self): 

        snakeHead=self.snakeLoc[0]
        ans=0
        maxi=False
        v=(snakeHead[0]+1,snakeHead[1])  
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            length=self.lengthCatchEnd(snakeLoc)
            ans=max(length,ans)
            if ans==length:
                maxi=v
        v=(snakeHead[0]-1,snakeHead[1])  
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            length=self.lengthCatchEnd(snakeLoc)
            ans=max(length,ans)
            if ans==length:
                maxi=v
        v=(snakeHead[0],snakeHead[1]+1)  
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            length=self.lengthCatchEnd(snakeLoc)
            ans=max(length,ans)
            if ans==length:
                maxi=v
        v=(snakeHead[0],snakeHead[1]-1) 
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            length=self.lengthCatchEnd(snakeLoc)
            ans=max(length,ans)
            if ans==length:
                maxi=v  
        if maxi==False:
            pass     
        nextStep=maxi
        return nextStep
    
    def checkValidity(self,pos):
        for j in range(0,len(self.snakeLoc)-1):
            i=self.snakeLoc[j]
            if i==pos:
                return False
        if (pos[0]>=self.width)or(pos[0]<0)or(pos[1]>=self.height)or(pos[1]<0):
            return False
        return True
    def checkBorder(self,pos):
        if (pos[0]>=self.width)or(pos[0]<0)or(pos[1]>=self.height)or(pos[1]<0):
            return False
        return True
            
    def arbitraryStep(self):
        snakeHead=self.snakeLoc[0]
        v=(snakeHead[0]+1,snakeHead[1])  
        maxi=v
        ans=0
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            size=self.calculateComponent(snakeLoc)
            ans=max(ans,size)
            if ans==size:
                maxi=v
                
        v=(snakeHead[0]-1,snakeHead[1])  
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            size=self.calculateComponent(snakeLoc)
            ans=max(ans,size)
            if ans==size:
                maxi=v
                
        v=(snakeHead[0],snakeHead[1]+1)  
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            size=self.calculateComponent(snakeLoc)
            ans=max(ans,size)
            if ans==size:
                maxi=v
                
        v=(snakeHead[0],snakeHead[1]-1) 
        if self.checkValidity(v):
            snakeLoc=copy.deepcopy(self.snakeLoc)
            snakeLoc.pop(len(snakeLoc)-1)
            snakeLoc.insert(0,v)
            size=self.calculateComponent(snakeLoc)
            ans=max(ans,size)
            if ans==size:
                maxi=v
        
        return maxi
    
    def dfs(self,v,vis):
        print vis
        u=(v[0]+1,v[1])
        if (u not in vis)and(self.checkBorder(u)):
            vis.add(u)
            self.dfs(u,vis)
        u=(v[0]-1,v[1])
        if (u not in vis)and(self.checkBorder(u)):
            vis.add(u)
            self.dfs(u,vis)
        u=(v[0],v[1]+1)
        if (u not in vis)and(self.checkBorder(u)):
            vis.add(u)
            self.dfs(u,vis)
        u=(v[0],v[1]-1)
        if (u not in vis)and(self.checkBorder(u)):
            vis.add(u)
            self.dfs(u,vis)
        
            
    def calculateComponent(self,snakeLoc):
        vis=Set(snakeLoc) 
        self.dfs(snakeLoc[0],vis)
        return len(vis)
             
    def chooseDirection(self):
        nextStep=0
        rand=0
        ##if len(self.snakeLoc)>=0.8*self.width*self.height:
        ##    rand=random.random()
        if (self.inBadPosition==0)and(rand<=0.5):
            nextStep=self.safePathToFood()
        if not (nextStep==False) and not (nextStep==0):
            return self.translateDirection(self.snakeLoc[0], nextStep)
        #if (nextStep==False)and(self.inBadPosition==0):
        #    self.inBadPosition=math.trunc((self.width+self.height)/4)
        nextStep=self.pathToEnd()
        if not (nextStep==False):
            return self.translateDirection(self.snakeLoc[0], nextStep)
        nextStep=self.arbitraryStep()
        return self.translateDirection(self.snakeLoc[0], nextStep)      
        
        
    def translateDirection(self,u,v):
        w=(v[0]-u[0],v[1]-u[1])
        if (w==(1,0)):
            return snake.Direction.Right
        elif (w==(-1,0)):
            return snake.Direction.Left
        elif (w==(0,1)):
            return snake.Direction.Down
        elif (w==(0,-1)):
            return snake.Direction.Up
        
