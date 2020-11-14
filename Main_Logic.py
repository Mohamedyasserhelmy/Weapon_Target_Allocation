import numpy
import encoder_decoder as ed

weapon_names = []                                   # Weapons list to be encoded 
weapon_instances = []                               # Instances of each weapon also used in encoding
threat_coeff = []                                   # List of Threat Coefficients for each target
# Just for input 
w_name = ""                     
w_inst = ""

# Getting the number of weapons with their names 
while (True):
    w_name, w_inst = input("Enter weapons and number of instances: \n").split(" ")
    if (w_name == "x" or w_inst == "x"):            # Stop Delimeter
        break
    weapon_names.append(w_name)
    weapon_instances.append(w_inst)

noftargets= int(input("Enter the number of targets : \n"))      # N of targets [1-> N]

print ("Enter Threat coefficient for each target : ")
# Get Threat coeff. from input
for k in range(noftargets):
    threat_coeff.append(int(input()))

print(threat_coeff)
# Initializing probability matrix 
prob_matrix = []
print ("Enter Success probability matrix : ")
for i in range(0, len(weapon_names)):
    a=[]
    for j in range(0, noftargets):
        a.append(float(input()))
    prob_matrix.append(a)    
    

