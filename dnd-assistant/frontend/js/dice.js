function rollCustom(){
    //getting user input
    const notation = $('#dice-input').val();  //extracted from dice.py

    fetch(`http://localhost:8000/api/dice/roll/${notation}`)
        .then(res => res.json())
        .then(data => {
            displayRoll(data);
        });
}

function displayRoll(data) {
    $('#result').html(`
        <p>Rolled: ${data.notation}</p>
        <p>Individual rolls: [${data.rolls.join(', ')}]</p>
        <p>Modifier: ${data.modifier}</p>
        <p><strong>Total: ${data.total}</strong></p>
    `);
}