from fastapi import APIRouter
from pydantic import BaseModel, Field 
import random

router = APIRouter()

#Pydantic model for the request body (the instant form data)
class DiceRollRequest(BaseModel):
    # Default to 1 roll and 0 modifier as defined in the helper function
    count: int = Field(1, description="The number of dice to roll (N). Must be 1 or greater.")
    modifier: int = Field(0, description="The integer modifier to add to the total roll (M).")

#helper function for parameter
def roll_dice(sides: int, count: int = 1, modifier: int = 0):
    # Ensure count is at least 1
    count = max(1, count)
    
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    
    return {
        "sides": sides,
        "count": count,
        "modifier": modifier,
        "rolls": rolls,
        "total": total
    }

@router.post("/roll/d{sides}")
def roll_custom_dice(sides: int, request: DiceRollRequest):
    #error handling
    if sides < 2:
        return {"error": "Dice must have at least 2 sides."}, 400

    result = roll_dice(sides, request.count, request.modifier)
    return result
