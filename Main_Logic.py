import numpy as np
import initialize_select_v2 as m
import encoder_decoder as ed
import crossoverMutation as cm

weapon_names = []                                   # Weapons list to be encoded 
weapon_instances = []                               # Instances of each weapon also used in encoding
threat_list = []                                    # List of Threat Coefficients for each target
chrom_list = []                                     # population list
# Just for input 
w_name = ""                     
w_inst = ""


# Getting the number of weapons with their names 
while (True):
    w_name, w_inst = input("Enter weapons and number of instances: \n").split(" ")
    if (w_name == "x" or w_inst == "x"):            # Stop Delimeter
        break
    weapon_names.append(w_name)
    weapon_instances.append(int(w_inst))

noftargets= int(input("Enter the number of targets : \n"))      # N of targets [1-> N]

print ("Enter Threat coefficient for each target : ")
# Get Threat coeff. from input
for k in range(noftargets):
    threat_list.append(int(input()))

#print(threat_coeff)
# Initializing probability matrix 
prob_matrix = []
print ("Enter Success probability matrix : ")
for i in range(0, len(weapon_names)):
    a=[]
    for j in range(0, noftargets):
        a.append(float(input()))
    prob_matrix.append(a)

# Encoding Dictionary 
enc = ed.encode(weapon_names, weapon_instances)

best_chrom = []
best_sol = sum(threat_list)

# Main Loop

for f in range(50):
    m.initialize(chrom_list, 5, sum(weapon_instances))
    #print("hromList: "+str(chrom_list))
    assign_all = m.assigne_all(chrom_list, threat_list)
    
    #print ("Assign All : " + str(assign_all))
    selected_chroms = m.select(assign_all, threat_list, enc, weapon_names, prob_matrix)
    
    #print("Selected : " + str(selected_chroms))
    out = cm.crossover(selected_chroms[0], selected_chroms[1])
    #print("CrossOvered " + str(out))
    out2 = cm.mutation(out, threat_list, enc, weapon_names, prob_matrix)
    #print("Mutated : " + str(out2))
    m.replace(out2, selected_chroms, assign_all, threat_list, enc, weapon_names, prob_matrix)
    for k in out2:
        fit_out = m.compute_fitness(k, threat_list, enc, weapon_names, prob_matrix)
        if (fit_out < best_sol) :
            best_chrom = k
            best_sol = fit_out
    
print("Total Expected Threat : " + str(best_sol))
print(best_chrom)
for h in range(1, noftargets+1):
    print("The waepon assigned to target " + str(h) + " is ")
    print(m.get_weapons(best_chrom, h, enc))
