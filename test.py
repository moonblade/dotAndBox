#!/usr/bin/env python2.7
from random import randint
import sys
from turtle import *
import time

def debug(string):
    print(string)

ticker=1000
class Logic:
    def __init__(self, board, me):
        self.board = board
        self.me = me
        self.opp = 1 if me==2 else 2
        self.moveSpace = {}
        for x in range(10):
            for y in range(10):
                for orientation in range(2):
                    if(self.board.possible((x,y), orientation)):
                        self.moveSpace[x*100 + y*10 + orientation]=((x,y),orientation)
    def clean(self,move):
        p1=(int(move[1]),int(move[3]))
        p2=(int(move[7]),int(move[9]))
        # if(p1[0]>p2[0] or p1[1]>p2[1]):
        #     p1,p2=p2,p1
        if(p1[0]<p2[0]):
            # vertical
            return p1,1
        else:
            # horizontal
            return p1,0

    def opponent_move(self,move):
        p, orientation = self.clean(move)
        del self.moveSpace[p[0]*100 + p[1]*10 + orientation]
        self.board.move(p,orientation)
        self.board.updateChain(p, orientation)

    def score(self, move):
        sidesLine=self.board.sidesLine(move[0],move[1])
        if(sidesLine[0][0]==3 and sidesLine[1][0]==3):
            return 6

        if(sidesLine[0][0]==3 or sidesLine[1][0]==3):
            chainLength=self.board.chainLength(move[0],move[1])
            return -100 if chainLength==2 else chainLength

        if(sidesLine[0][0]<2 and sidesLine[1][0]<2):
            saveBoard=self.board        
            self.board.move(move[0],move[1])
            chainLength=self.board.chainLength(move[0],move[1])
            self.board=saveBoard
            return chainLength

        if(sidesLine[0][0]==2 or sidesLine[1][0]==2):
            return -self.board.chainLength(move[0],move[1])
        return 0

    def myMove(self):
        ticker=1000
        selected=-1
        best=-1000
        bestMove=[]
        for key in self.moveSpace:
            move=self.moveSpace[key]
            score=self.score(move)
            if(score>best):
                bestMove=move
                selected=key
            if(ticker<0):
                break;
                        
        del self.moveSpace[selected]
        self.board.move(bestMove[0],bestMove[1]);
        self.board.updateChain(bestMove[0],bestMove[1])
        return self.board.toString(bestMove[0],bestMove[1])

    def view(self):
        self.board.view()

class Board:
    def __init__(self, b = None):
        # RIGHT 0 and DOWN 1
        if b is None:
            self.board = 0
        else:
            self.board = b
        self.saved = {}
        self.noc = 0

    def view(self):
        debug(hex(self.board))
        debug("")

    def possible(self, point, orientation):
        return not ((point[0]==9 and point[1]==9) or (point[0]==9 and orientation==1) or (point[1]==9 and orientation==0) or not self.isFree((point[0],point[1]),orientation))

    def sidesLine(self, point, orientation):
        boxTL=self.getBoxTL(point, orientation)
        return [self.sides(boxTL[0]), [0] if len(boxTL)==1 else self.sides(boxTL[0])]


    def getBoxTL(self, point, orientation):
        if(orientation==0):
            # horiz
            if(point[0]==0):
                return [point]
            if(point[0]==9):
                return [(point[0]-1,point[1])]
            return [(point[0]-1,point[1]), point]
        if(orientation==1):
            # vert
            if(point[1]==0):
                return [point]
            if(point[1]==9):
                return [(point[0],point[1]-1)]
            return [(point[0],point[1]-1),point]

    def nextBox(self, boxTL, point, orientation):
        # give box and one line, will give next box and its opening line
        if point is None:
            return

        sides=self.sides(boxTL)

        if(sides[0]==2):
            if(boxTL[0]==point[0] and boxTL[1]==point[1]):
                if orientation==0:
                    # top
                    sides[1]=1
                else:
                    # left
                    sides[2]=1
            if(boxTL[1]==point[1]):
                # bottom
                sides[3]=1
            if(boxTL[0]==point[0]):
                # right
                sides[4]=1
            toMove=sides.index(0)
            if(toMove==1):
                # top
                return [ (boxTL[0]-1,boxTL[1]), boxTL, 0]  if boxTL[0]>0 else None
            elif(toMove==2):
                # left
                return [ (boxTL[0],boxTL[1]-1), boxTL, 1]  if boxTL[1]>0 else None
            elif(toMove==3):
                # bottom
                return [ (boxTL[0]+1,boxTL[1]), (boxTL[0]+1,boxTL[1]), 0]  if boxTL[0]<9 else None
            elif(toMove==4):
                # right
                return [ (boxTL[0],boxTL[1]+1), (boxTL[0],boxTL[1]+1), 1]  if boxTL[1]<9 else None

        elif(sides[0]==3):
            return [boxTL, None, orientation]
        else:
            return None

        
    def updateChain(self, point, orientation):
        self.saved={}
        self.noc=0
    #     boxTL=self.getBoxTL(point, orientation)
    #     if(boxTL[0] in self.saved):
    #         updateList=self.saved[boxTL[0]]
    #         for x in updateList[1]:
    #             if x in self.saved:
    #                 del self.saved[x]
    #         self.noc-=1
    #     if(len(boxTL)>1):
    #         if(boxTL[1] in self.saved):
    #             updateList=self.saved[boxTL[1]]
    #             for x in updateList[1]:
    #                 if x in self.saved:
    #                     del self.saved[x]
    #         self.noc-=1
    #     self.chainLength(point, orientation)


    def chainLength(self, point, orientation):
        # saveBoard=self.board        
        chainLength = 0
        self.move(point, orientation)
        sidesLine=self.sidesLine(point, orientation)
        boxTL = self.getBoxTL(point, orientation)
        if(boxTL[0] in self.saved):
            return self.saved[boxTL[0]][0]
        nextBox=[boxTL[0], point, orientation]
        updateList=[]
        while(nextBox is not None):
            chainLength+=1
            updateList.append(nextBox[0])
            nextBox=self.nextBox(nextBox[0], nextBox[1], nextBox[2])
        if(len(boxTL)>1):
            nextBox=[boxTL[1], point, orientation]
            while(nextBox is not None):
                chainLength+=1
                updateList.append(nextBox[0])
                nextBox=self.nextBox(nextBox[0], nextBox[1], nextBox[2])
        for x in updateList:
            self.saved[x]=[chainLength,updateList]
        self.noc+=1
        debug("chainLength")
        debug(self.saved)
        debug("noc")
        debug(self.noc)
        # self.board=saveBoard
        return chainLength

    def sides(self, boxTL):
        # top left bottom right
        # return [self.get((boxTL[0],boxTL[1]),0)+self.get((boxTL[0],boxTL[1]),1)+self.get((boxTL[0]+1,boxTL[1]),0)+self.get((boxTL[0],boxTL[1]+1),1)]
        return [self.get((boxTL[0],boxTL[1]),0)+self.get((boxTL[0],boxTL[1]),1)+self.get((boxTL[0]+1,boxTL[1]),0)+self.get((boxTL[0],boxTL[1]+1),1),self.get((boxTL[0],boxTL[1]),0),self.get((boxTL[0],boxTL[1]),1),self.get((boxTL[0]+1,boxTL[1]),0),self.get((boxTL[0],boxTL[1]+1),1)]

    def get(self, point, orientation):
        ticker-=1
        return self.board&(1<<(point[0]*20+point[1]*2+orientation))

    def move(self, point, orientation):
        self.board|=1<<(point[0]*20+point[1]*2+orientation)

    def isFree(self, point, orientation):
        return self.get(point,orientation)==0

    def toString(self, point, orientation):
        if orientation==0:
            return (str(point)+","+str((point[0],point[1]+1))).replace(" ","")
        if orientation==1:
            return (str(point)+","+str((point[0]+1,point[1]))).replace(" ","")


if __name__=="__main__":
    with open("controller") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    pen({"pendown":False})
    for x in content:
        x=x.split()
        if x[2]=="Moved":
            if(x[1]=="1"):
                pencolor("red")
            else:
                pencolor("black")
            setpos(int(x[3][2])*30,int(x[3][4])*30)
            pen({"pendown":True})
            begin_fill()
            setpos(int(x[3][8])*30,int(x[3][10])*30)
            pen({"pendown":False})
            end_fill()
    done()
