#Copyright 2018 JuliePark ysp599@bu.edu
#Copyright 2018 Vaibhav Bansal vbansal@bu.edu
#Copyright 2018 Ayush Shirsat ayush34@bu.edu

earth_mass = 5.972*(10**24)
p_mass = 0.49*earth_mass
proton_mass = 1.6726219*(10**-27)
protons = p_mass/proton_mass

electrons = protons
byte = electrons//8
TB = byte*(10**-12)
tb_up = TB+0.1*TB
tb_low= TB-0.1*TB

print (str(TB)+"\n"+str(tb_low)+"\n"+str(tb_up)) 


