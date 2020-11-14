import random as r
import numpy as np

# Depending on the value of pc which indicates to make crossover or not
# and the value of xc which indicates where the crossover occurs

pc = r.uniform(0.4, 0.7)    #probability of crossover
pm = r.uniform(0.001, 0.1)  #Probability of mutation

def crossover(x1, x2):
    # x1: Chromosome1 (Parent 1)
    # x2: Chromosome2 (parent 2)

    # Crossover point
    xc = int(r.uniform(1, len(x1)-1))

    # Crossover indicator
    rc = r.uniform(0, 1)

    # Mutation Indicator
    rm = r.uniform(0, 1)
    
    # For debug Reasons
    """print ("rc : " + str(rc))
    print ("xc: " + str(xc))
    print ("pc : " + str(pc))"""
    
    # Keeping Children out of parents to apply replacement with Elitis strategy
    y1 = []
    y2 = []
    if (rc <= pc):
        #Perform Crossover
        temp = x1[xc:len(x1)]
        y1[0:xc] = x1[0:xc]
        y1[xc:len(x1)] = x2[xc: len(x2)]
        y2[0:xc] = x2[0:xc]
        y2[xc:len(x2)] = temp
        """
        print ("xc: " + str(xc))
        print(x1)
        print(x2)
        print(y1)
        print(y2)"""
        return list([y1, y2])
    else:
        #No crossover will be performed 
        return list([x1, x2])

    

# Mutation function flips each bit in chromosomes
def mutation(targets):
    # targets: targets List [1, 2, 3,...N]

    n_targets = len(targets)

    # Converting Array to string
    c_array = np.array([str(i) for i in targets])

    # changed in integration 
    rm = 0.01
    
    # If Rm within range then replace this index with the next index number
    for j in range(0, n_targets):
        if (rm <= pm):
            if (j == n_targets-1):
                targets[j] = int(c_array[0])
            else:
                targets[j] = int(c_array[j+1])
                
        else:
            return None

    return targets



print(mutation([1,10,11]))
print(crossover([1,10,11,1,10],[10,11,1,1,1]))
