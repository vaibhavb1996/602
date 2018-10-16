//Copyright 2018 JuliePark ysp599@bu.edu
//Copyright 2018 Vaibhav Bansal vbansal@bu.edu
//Copyright 2018 Ayush Shirsat ayush34@bu.edu

#include<iostream>
#include<math.h>

int main()
{
	double earth_mass = 5.972*(pow(10,24));
	double p_mass = 0.49*earth_mass;
	double proton_mass = 1.6726219*(pow(10,-27));
	double protons = p_mass/proton_mass;

	double electrons = protons;
	double byte = electrons/8;
	double TB = byte*(pow(10,-12));
	double tb_up = TB+0.1*TB;
	double tb_low= TB-0.1*TB;

	std::cout << TB << "\n" << tb_low << "\n" << tb_up << "\n";
	return 0;
}