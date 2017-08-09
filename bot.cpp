#include<iostream>
#include<fstream>
#include<string>

using namespace std;
int temp;
void swap(int &a, int &b)
{
	temp=a;
	a=b;
	b=a;
}

class Board{
public:
	// in and out is going to be point notations any changes are to be done here itself
	int b[19][10];
	Board(){
		for(int i=0;i<19; ++i)
		{
			for(int j=0;j<10;++j)
			{
				b[i][j]=0;
			}
			if(i%2==1)
				b[i][9]=-1;
		}
	}

	void play(int ix, int iy, int jx, int jy)
	{
		if(ix>jx || iy>jy)
		{
			swap(ix,jx);
			swap(iy,jy);
		}
		if(ix<jx)
		{
		}else if(iy<jy){

		}
	}

	// void view()
	// {
	// 	for(int i=0;i<19; ++i)
	// 	{
	// 		for(int j=0;j<10;++j)
	// 		{
	// 			log>>b[i][j]<<" ";
	// 		}
	// 		log<<endl;
	// 	}
	// 	log<<endl;
	// }
};
class Logic{
public:
	int player;
	Board b;
	void setPlayer(int p){
		player=p;
	}

	void opponentMove(int ix, int iy, int jx, int jy){

	}

	void view()
	{
		// b.view();
	}
};


int main(int argc, char* argv[])
{
	ofstream log;
	log.open(argv[1]);

	bool gameRunning = true;
	int ix,iy,jx,jy;
	Logic l;
	string temp;
	do{
		cin>>temp;
		log<<temp<<endl;
		if(temp.compare("START")==0)
		{
			int p;
			cin>>p;
			l.setPlayer(p);
		}
		else if(temp.compare("YOUR_MOVE")==0)
		{
			cout<<"(0,1),(1,1)"<<std::flush();
		}
		else if(temp.compare("OPPONENT_MOVE")==0)
		{
			cin>>temp;
			log<<temp<<endl;
			ix=temp[1]-'0';
			iy=temp[3]-'0';
			jx=temp[7]-'0';
			jy=temp[9]-'0';
			l.opponentMove(ix,iy,jx,jy);
		}else if(temp.compare("STOP")==0)
		{
			log<<temp<<endl;
			gameRunning = false;
		}
	}while(gameRunning);
	log<<"end";
	return 0;
}