let currentSides = 0;
let currentResultId = '';

/**
 * Shows the modal, sets the context for the roll, and updates the modal title.
 * @param {number} sides - The number of sides on the die (e.g., 4, 6, 20).
 * @param {string} resultElementId - The ID of the span below the die (e.g., 'd4-result').
 */
function openModal(sides, resultElementId) {
    currentSides = sides;
    currentResultId = resultElementId;

    const modal = document.getElementById('dice-roll-modal');
    const title = document.getElementById('modal-title');
    
    document.getElementById('roll-count').value = 1;
    document.getElementById('roll-modifier').value = 0;
    
    if (title) {
        title.textContent = `Configure D${sides} Roll`;
    }
    if (modal) {
        modal.classList.add('visible');
    }
}

function closeModal() {
    const modal = document.getElementById('dice-roll-modal');
    if (modal) {
        modal.classList.remove('visible');
    }
}

function handleRollSubmit(event) {
    event.preventDefault(); 

    const rollCount = parseInt(document.getElementById('roll-count').value) || 1;
    const rollModifier = parseInt(document.getElementById('roll-modifier').value) || 0;

    if (currentSides === 0 || rollCount < 1) {
        console.error("Invalid roll configuration or missing dice context.");
        return;
    }

    closeModal();
    
    sendRollRequest(currentSides, currentResultId, rollCount, rollModifier);
}

/**
 * Sends a request to the FastAPI backend to roll a die and updates the UI.
 * @param {number} sides - The number of sides on the die.
 * @param {string} resultElementId - The ID of the span below the die.
 * @param {number} count - The number of dice to roll (N).
 * @param {number} modifier - The integer modifier to add (M).
 */
async function sendRollRequest(sides, resultElementId, count, modifier) {
    const apiUrl = `/api/dice/roll/d${sides}`;
    const individualResult = document.getElementById(resultElementId);
    const mainDisplay = document.getElementById('main-roll-display');

    if (individualResult) {
        individualResult.textContent = '...'; 
    }
    if (mainDisplay) {
        const modifierText = modifier !== 0 ? (modifier > 0 ? ` + ${modifier}` : ` ${modifier}`) : '';
        mainDisplay.innerHTML = `Rolling ${count}D${sides}${modifierText}...`;
    }

    try {
        const payload = {
            count: count,
            modifier: modifier
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result && result.total !== undefined && result.rolls) {
            const { total, rolls, modifier } = result;

            if (individualResult) {
                individualResult.textContent = total;
            }

            if (mainDisplay) {
                const rollsDetail = rolls.join(' + ');
                const modifierText = modifier !== 0 ? (modifier > 0 ? ` + ${modifier}` : ` ${modifier}`) : '';
                
                mainDisplay.innerHTML = `
                    Rolled ${count}D${sides}${modifierText}. Total: 
                    <span style="color: yellow; font-weight: 900;">${total}</span> 
                    (Rolls: ${rollsDetail}${modifierText})
                `;
            }
        } else {
            throw new Error("Invalid response structure from backend.");
        }

    } catch (error) {
        console.error("Dice roll failed:", error);
        if (individualResult) {
            individualResult.textContent = 'Err';
        }
        if (mainDisplay) {
            mainDisplay.innerHTML = 'Error rolling dice. Check console for details.';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('roll-form');
    if (form) {
        form.addEventListener('submit', handleRollSubmit);
    }
});