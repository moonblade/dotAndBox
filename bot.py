#!/usr/bin/env python3

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
        self.move(p1,p2)

    def move(self,p1,p2):
        self.board.move(self.me, p1, p2)

    def print(self):
        self.board.print()


class Board:
    def __init__(self):
        self.boardSize = 10
        self.board = [[-1 if (x==self.boardSize-1 and y%2==0) else 0 for x in range(self.boardSize)] for y in range(self.boardSize)]
    
    def print(self):
        for x in range(self.boardSize):
            print(self.board[x])
        print()

    def move(self, player, p1, p2):
        if(p1[0]<p2[0]):
            self.board[p1[0]+1][p1[1]]=player
        elif(p1[1]<p2[1]):
            self.board[p1[0]][p1[1]]=player


if __name__=="__main__":
    b=Board()
    l=Logic(b,1);
    l.print();
    l.opponent_move("(1,0),(0,0)")
    l.print();

    # while(True):
        # Game loop
        