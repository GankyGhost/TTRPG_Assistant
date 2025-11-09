# Importing random
import random

# dictionary containg all possible dice rolls
dice = {'d4':4, 'd6':6, 'd8':8, 'd10':10, 'd12':12, 'd20':20, 'd100':100}

# dice rolling function
def roll_dice(sides, count = 1, modifier=0):
    rolls = [random.randint(1, sides) for _ in range(count)]
    return sum(rolls) + modifier


# processes a hit roll
def hit_processor(hit:str):
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return None


# processes an attack roll
def attack_processor(attack:str):
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return None