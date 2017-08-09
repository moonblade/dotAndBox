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

    def clean(self,move):
        p1=(int(move[1]),int(move[3]))
        p2=(int(move[7]),int(move[9]))
        if(p1[0]>p2[0] or p1[1]>p2[1]):
            p1,p2=p2,p1
        return p1,p2

    def opponent_move(self,move):
        p1, p2 = self.clean(move)
        self.board.move(self.opp,p1,p2)

    def myMove(self):
        x=randint(0,18)
        y=randint(0,9)
        while(not self.board.isFree((x,y))):
            x=randint(0,18)
            y=randint(0,9)
        self.board.moveBP(self.me, (x, y));
        return self.toString(self.board.boardToPoint((x,y)))

    def view(self):
        self.board.view()

    def toString(self, point):
        return (str(point[0])+","+str(point[1])).replace(" ","")


class Board:
    def __init__(self):
        self.boardSize = 10
        self.board = [[-1 if (x==self.boardSize-1 and y%2==0) else 0 for x in range(self.boardSize)] for y in range(self.boardSize*2-1)]
    
    def view(self):
        for x in range(len(self.board)):
            debug(self.board[x])
        debug("")

    def move(self, player, p1, p2):
        point = self.pointToBoard(p1, p2)
        self.moveBP(player,point)

    def moveBP(self, player, bp):
        self.board[bp[0]][bp[1]]=player

    def isFree(self, p):
        return self.board[p[0]][p[1]]==0


    def pointToBoard(self, p1, p2):
        if(p1[0]<p2[0]):
            return(2*p1[0]+1,p1[1])
        elif(p1[1]<p2[1]):
            return(2*p1[0],p1[1])

    def boardToPoint(self, bp):
        if(bp[0]%2==1):
            # vertical
            return ((bp[0]//2,bp[1]),(bp[0]//2+1,bp[1]))
        else:
            # horizontal
            return ((bp[0]//2,bp[1]),(bp[0]//2,bp[1]+1))


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