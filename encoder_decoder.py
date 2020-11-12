import numpy as np

# In this module I'm going to construct
# an encoding() function that encodes weapons and corresponding indices
# Then The decoding() function which do inverse

def encode(x1, x2):
    # x1 : List of weapons [tank, aircraft, grenade, sea vessel, ...]
    # x2 : List of instances count of each weapon [2, 1, 2, ...]
    #                              where count >= 1
    if (len(x1) != len(x2)):
        return "Error Arrays should Be at the same Size"
    enc = {}
    Sum = np.sum(np.array(x2))
    i=0
    k = 0
    while (i < len(x2)):
        for j in range(x2[i]):
            enc[x1[i] + "# " +str(j+1)] = k
            k+=1
        i+=1

    return enc


def decode(y, index):
    # input rhe index and return the corresponding key
    for weapon, number in y.items():
        if (number == index):
            return weapon

# If the Index not found the function returns None Type
# It could be used for exception as follows if (decode(r,t) == None):
#                                                print("Invalid Index")


# Tested && Debugged 
