#!/usr/bin/env python2.7
from random import randint
import sys

f=open(sys.argv[1],'w')
def debug(string):
    f.write(str(string))
    f.write("\n")
    f.flush()


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
        # self.movesLeft = 220
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
        # self.movesLeft-=1
        del self.moveSpace[p[0]*100 + p[1]*10 + orientation]
        self.board.move(p,orientation)

    def score(self, move):
        sidesLine=self.board.sidesLine(move[0],move[1])
        if(sidesLine[0][0]==3 or sidesLine[1][0]==3):
            return 3
        if(sidesLine[0][0]<2 and sidesLine[1][0]<2):
            return 0
        if(sidesLine[0][0]==2 or sidesLine[1][0]==2):
            return -1
        return 0

    def myMove(self):
        selected=-1
        best=-1000
        bestMove=[]
        for key in self.moveSpace:
            move=self.moveSpace[key]
            score=self.score(move)
            if(score>best):
                bestMove=move
                selected=key
                if(score==3):
                    break;
                        
        del self.moveSpace[selected]
        self.board.move(bestMove[0],bestMove[1]);
        return self.board.toString(bestMove[0],bestMove[1])

    def view(self):
        self.board.view()

class Board:
    def __init__(self):
        # RIGHT 0 and DOWN 1
        self.board = [[[0,0] for x in range(10)] for y in range(10)]
    
    def view(self):
        for x in range(len(self.board)):
            debug(self.board[x])
        debug("")

    def possible(self, point, orientation):
        return not ((point[0]==9 and point[1]==9) or (point[0]==9 and orientation==1) or (point[1]==9 and orientation==0) or not self.isFree((point[0],point[1]),orientation))

    def sidesLine(self, point, orientation):
        if(orientation==0):
            # horiz
            if(point[0]==0):
                return [self.sides(point),[0]]
            if(point[0]==9):
                return [self.sides((point[0]-1,point[1])),[0]]
            return [self.sides(point), self.sides((point[0]-1,point[1]))]
        if(orientation==1):
            # vert
            if(point[1]==0):
                return [self.sides(point),[0]]
            if(point[1]==9):
                return [self.sides((point[0],point[1]-1)),[0]]
            return [self.sides(point), self.sides((point[0],point[1]-1))]

    def sides(self, boxTL):
        # top left bottom right
        return [self.board[boxTL[0]][boxTL[1]][0]+self.board[boxTL[0]][boxTL[1]][1]+self.board[boxTL[0]+1][boxTL[1]][0]+self.board[boxTL[0]][boxTL[1]+1][1],self.board[boxTL[0]][boxTL[1]][0],self.board[boxTL[0]][boxTL[1]][1],self.board[boxTL[0]+1][boxTL[1]][0],self.board[boxTL[0]][boxTL[1]+1][1]]

    def move(self, point, orientation):
        self.board[point[0]][point[1]][orientation]=1


    def isFree(self, point, orientation):
        return self.board[point[0]][point[1]][orientation]==0

    def toString(self, point, orientation):
        if orientation==0:
            return (str(point)+","+str((point[0],point[1]+1))).replace(" ","")
        if orientation==1:
            return (str(point)+","+str((point[0]+1,point[1]))).replace(" ","")


if __name__=="__main__":
    b=Board()
    debug("starting")
    string=raw_input().split()
    if(string[0]=="START"):
        l=Logic(b,int(string[1]));
    else:
        l=Logic(b,1);

    while True:
        string=raw_input().split()
        debug(string)
        if(string[0]=="YOUR_MOVE"):
            move=l.myMove()
            debug("my " + move)
            sys.stdout.write(move+"\n")
            sys.stdout.flush()
        elif(string[0]=="OPPONENT_MOVE"):
            debug("his " + string[1])
            l.opponent_move(string[1])
        elif(string[0]=="STOP"):
            break;
        l.view()
    f.close()