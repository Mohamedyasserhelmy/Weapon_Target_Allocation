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
#it returns a list with size equal tochrom size. its indeces represents weaponse inctance and its values represents the target number in binary rep
def assigne(List, threat_list):
    assigne_list = []
    Sum = sum(threat_list)
    wheel_range = [x/Sum for x in threat_list]
    #print(wheel_range)
    for i in range(len(List)):
        if List[i] == 0:
            #the 0 here means that that inctance of a specific weapon type will not be used
            assigne_list.append(0)
        else:
            num = np.random.randint(0, Sum)/Sum
            #print(num)
            for j in range(len(wheel_range)):
                if num >= 0 and num < wheel_range[0]:
                    assigne_list.append(np.int(np.binary_repr(1)))
                    break
                elif num >= sum(wheel_range[:j]) and num < sum(wheel_range[:j+1]):
                    assigne_list.append(np.int(np.binary_repr(j+1)))
                    break
    return assigne_list


def assigne_all(pop):
    l = []
    for i in pop:
        l.append(assigne(i, threat_list))
    return l


def get_key(d,val):
    for key, value in d.items(): 
         if val == value:
             return key
            
    return "key doesn't exist"

#this function is to get all of the inctances assigned to a specific single target
def get_weapons(assigne_list, val):
    l = []
    for i in range(len(assigne_list)):
        if np.int(np.binary_repr(val)) == assigne_list[i]:
            l.append(get_key(enc, i))
    return l


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
    #print(chrom)
    for i in range(len(threat_list)):
        weapon_list = get_weapons(chrom, i+1)
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
        num = np.random.uniform(0, Sum)/Sum
        #print(num)
        for j in range(len(wheel_range)):
            if num >= 0 and num < wheel_range[0]:
                if  not selection_list.__contains__(chrom_list[0]):
                    selection_list.append(chrom_list[0])
                    i+=1
                break
            elif num >= sum(wheel_range[:j]) and num < sum(wheel_range[:j+1]):
                if not selection_list.__contains__(chrom_list[j]):
                    selection_list.append(chrom_list[j])
                    i+=1
                break
    return selection_list


def replace(NewGen, OldGen, assigned_list):
    for i in range(len(NewGen)):
        new_fitness = compute_fitness(NewGen[i], threat_list)
        old_fitness = compute_fitness(OldGen[i], threat_list)
        #print(str(new_fitness) + "   " + str(old_fitness))
        if new_fitness < old_fitness:
            index = assigned_list.index(OldGen[i])
            assigned_list[index] = NewGen[i]

            

"""threat_list = [16,5,10]
chrom_list = []
initialize(chrom_list, 3, 5)
print(chrom_list)
assigne_all = assigne_all(chrom_list)
print(assigne_all)
selected_chroms = select(assigne_all)
print(selected_chroms)
replace([[1,11,1,10,10],[1,1,1,0,11]], selected_chroms, assigne_all)
print(assigne_all)"""
