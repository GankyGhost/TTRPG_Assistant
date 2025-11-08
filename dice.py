# import the random library 
import random

# create dice functions to use for rolling dice;
# d4, d6, d8, d10, d12, d20, and percentile dice --- d100, in this case.
def d4(): 
    die = random.randint(1, 4)
    return die

def d6():
    die = random.randint(1, 6)
    return die

def d8(): 
    die = random.randint(1, 8)
    return die

def d10():
    die = random.randint(1,8)
    return die

def d12(): 
    die = random.randint(1, 12)
    return die

def d20(): 
    die = random.randint(1, 20)
    return die

def d100():
    die = random.randint(1, 100)
    return die