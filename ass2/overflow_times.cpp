//Copyright 2018 Vaibhav Bansal vbansal@bu.edu
#include<iostream>
#include<ctime>
#include<math.h>

using namespace std;

int main()
{
	clock_t start_time, end_time;
	int i=1;
	//cout << i << endl;
	start_time=clock();
	while (i<65536)
	{
		i++;
	}
	end_time=clock();
	
	//cout<<CLOCKS_PER_SEC<<endl;

	double seconds = (double)(end_time-start_time)/CLOCKS_PER_SEC;
	

	double loop_16 = (double)(seconds*1000000.0);

	double loop_time = seconds/65536.0;

	double loop_8 = loop_time*pow(2,8)*pow(10,9);
	double loop_32 = loop_time*pow(2,32);
	double loop_64 = loop_time*pow(2,64)/(60*60*24*365.0);

	std::cout << "estimated int8 time (nanoseconds): " << loop_8 << std::endl;
    std::cout << "measured int16 time (microseconds): "<< loop_16 << std::endl;
    std::cout << "estimated int32 time (seconds): "    << loop_32 << std::endl;
   	std::cout << "estimated int64 time (years): "      << loop_64 << std::endl;

   	//cout<< loop_8 <<"\n";
	//cout<< loop_16 <<"\n";
	//cout<< loop_32 <<"\n";
	//cout<< loop_64 <<"\n";

	return 0;
}