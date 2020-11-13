import numpy as np
import encoder_decoder


#this is success probability matrix and it's valid only for 3-types of weapons and 3 targets
probability_matrix = [[0.3, 0.6, 0.5],
                      [0.4,0.5, 0.4],
                      [0.1, 0.2, 0.2]]

weapons_type = ['tank','aircraft','grenade']

enc = encoder_decoder.encode(weapons_type,[2,1,2])

#the chrom size is equal to sum of weapons inctances
def initialize(List, List_size, chrom_size):
    for i in range(List_size):
        arr = np.random.randint(0, 2, chrom_size)
        #this if statment in case the generated array is full of zeros which is wrong cuz this solution will not reduce the total threat
        if not arr.__contains__(1):
            i -= 1
            continue
        List.append(arr)


#this function is to assigne each inctance of the weapons to a specific target via roulette wheel
#it returns a dictionary with keys are the weapon type and number and the value is the assigned target
def assigne(List, threat_list):
    dictionary = {}
    Sum = sum(threat_list)
    wheel_range = [x/Sum for x in threat_list]
    for i in range(len(List)):
        if List[i] == 0:
            #dictionary.update({'weapon #'+str((i+1)):'not assigned'})
            #the 0 here means that that inctance of a specific weapon type will not be used
            dictionary[i+1] = 0
        else:
            num = np.random.randint(0, Sum+1)/Sum
            for j in range(len(wheel_range)):
                if num >= 0 and num < wheel_range[0]:
                    #dictionary.update({'weapon #'+str((i+1)):'assigned to target #1'})
                    dictionary[i+1] = 1
                    #print(num)
                    break
                elif num >= sum(wheel_range[:j]) and num < sum(wheel_range[:j+1]):
                    #dictionary.update({'weapon #'+str((i+1)):'assigned to target #'+str((j+1))})
                    dictionary[i+1] = j+1
                    #print(num)
                    break
    dictionary = set_WeaponTpye(dictionary, enc)
    return dictionary


def get_key(d,val):
    for key, value in d.items(): 
         if val == value:
             return key
            
    return "key doesn't exist"

#this function is to get all of the inctances assigned to a specific single target
def get_weapons(d,val):
    l = []
    for key, value in d.items(): 
         if val == value:
             l.append(key)
    return l

#this function is to map the indeces of the chrom which are the keys in d1 to the names of the inctances(ex. 'tank #2') which are the keys in d2 via the values in d2
#and it returns a dictionary with keys are the names and values are the targets
def set_WeaponTpye(d1, d2):
    keys = [x-1 for x in d1.keys()]  
    dictionary = {}
    for i in keys:
        dictionary[get_key(d2,i)] = d1[i+1]
    return dictionary

#this function computes the threat of a single target using the formula: (1-p)^n*target's threat
def multiply(weapons_instance, target):
    #NOTE: if the list of weapons assigned to a pecific target is empty that means this target will effect with 100% of its threat  value
    if len(weapons_instance)==0: return threat_list[target-1]
    result = 1.0
    for item in weapons_instance:
        for item2 in weapons_type:
            if item.__contains__(item2):
                type_index = weapons_type.index(item2)
                target_index = target-1
                result *= 1-probability_matrix[type_index][target_index]

    return result*threat_list[target-1]

#this function computes the fitness which is the expected total threat of survival of a specific chrom
def compute_fitness(chrom, threat_list):
    fitness = 0.0
    assigned_targets = assigne(chrom, threat_list)
    print(assigned_targets)
    for i in range(len(threat_list)):
        weapon_list = get_weapons(assigned_targets, i+1)
        fitness += multiply(weapon_list, i+1)
    return fitness

#here we select to random parents from the list of initialized chroms via roulette wheel
#it returns a list with the indecees if the selected chroms
def select(chrom_list):
    fitness_list= []
    selection_list = []
    for i in chrom_list:
        fitness = compute_fitness(i, threat_list)
        fitness_list.append(fitness)
    Sum = sum([(1.0/x) for x in fitness_list])
    #print(fitness_list)
    #print(Sum)
    wheel_range = [(1.0/x)/Sum for x in fitness_list]
    #print(wheel_range)
    i = 0
    #NOTE: if the selected chrom is already in the list we will iterate again until we get different chrom
    while(i < 2):
        num = np.random.uniform(0, Sum+0.0001)/Sum
        #print(num)
        for j in range(len(wheel_range)):
            if num >= 0 and num < wheel_range[0]:
                if  not selection_list.__contains__(0):
                    selection_list.append(0)
                    i+=1
                break
            elif num >= sum(wheel_range[:j]) and num < sum(wheel_range[:j+1]):
                if not selection_list.__contains__(j):
                    selection_list.append(j)
                    i+=1
                break
    return selection_list
            
"""threat_list = [16,5,10]
chrom_list = []
initialize(chrom_list, 3, 5)
print(chrom_list)
select(chrom_list)"""
