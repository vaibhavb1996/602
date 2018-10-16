//Copyright 2018 Vaibhav Bansal vbansal@bu.edu

#include<iostream>

int main(int argc, char *argv[])
{	
	//extern ostream cout;
	//extern ostream cerr;

	int i=1;
	for (i=1;i<argc;i++)
		{if (i<=4)
			std::cout<<argv[i]<<std::endl;
		else
			std::cerr<<argv[i]<<std::endl;
		}
return 0;
}