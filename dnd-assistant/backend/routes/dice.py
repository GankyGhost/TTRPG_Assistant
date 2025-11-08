"""Barbie: I'm adding routes to Emilia's code so I can access and connect it to the frontend, 
I'll do my best to keep most of the functionalities as she intended"""
from fastapi import APIRouter
# import the random library 
import random

router = APIRouter

#simplified dice function
def roll_dice(sides, count = 1, modifier=0):
    rolls = [random.randint(1, sides) for _ in range(count)]
    return sum(rolls) + modifier

# create dice functions to use for rolling dice;
# d4, d6, d8, d10, d12, d20, and percentile dice --- d100, in this case.
@router.get("/roll/d4")
def d4(): 
    return {"result" + roll_dice(4)}

@router.get("/roll/d6")
def d6():
    return {"result" + roll_dice(6)}

@router.get("/roll/d8")
def d8():
    return {"result" + roll_dice(8)}

@router.get("/roll/d10")
def d10():
    return {"result" + roll_dice(10)}

@router.get("/roll/d12")
def d12():
    return {"result" + roll_dice(12)}

@router.get("/roll/d20")
def d20():
    return {"result" + roll_dice(20)}

@router.get("/roll/d100")
def d100():
    return {"result" + roll_dice(100)}