const API_URL = 'http://localhost:8000/api';

// Open menu modal
function openStatblockMenu() {
    document.getElementById('statblock-menu-modal').style.display = 'block';
}

// Close menu modal
function closeStatblockMenu() {
    document.getElementById('statblock-menu-modal').style.display = 'none';
}

// Close list modal
function closeStatblockList() {
    document.getElementById('statblock-list-modal').style.display = 'none';
}

// Close detail modal
function closeStatblockDetail() {
    document.getElementById('statblock-detail-modal').style.display = 'none';
}

// Close form modal
function closeStatblockForm() {
    document.getElementById('statblock-form-modal').style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Show list of saved stat blocks
async function showStatblockList() {
    closeStatblockMenu();
    
    try {
        // Fetch all stat blocks from backend
        const response = await fetch(`${API_URL}/statblock`);
        const statblocks = await response.json();
        
        // Display them in the list modal
        const container = document.getElementById('statblock-list-container');
        container.innerHTML = '';
        
        if (statblocks.length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 20px;">No stat blocks saved yet. Create one!</p>';
        } else {
            statblocks.forEach(sb => {
                const item = document.createElement('div');
                item.className = 'statblock-list-item';
                item.onclick = () => viewStatblockDetail(sb._id);
                item.innerHTML = `
                    <h3>${sb.name}</h3>
                    <p>${sb.size} ${sb.creature_type} | AC: ${sb.ac} | HP: ${sb.hp}</p>
                `;
                container.appendChild(item);
            });
        }
        
        document.getElementById('statblock-list-modal').style.display = 'block';
    } catch (error) {
        console.error('Error fetching stat blocks:', error);
        alert('Error loading stat blocks. Make sure the backend is running.');
    }
}


// View full stat block detail
async function viewStatblockDetail(statblockId) {
    closeStatblockList();
    
    try {
        // Fetch full stat block data
        const response = await fetch(`${API_URL}/statblock/${statblockId}`);
        const sb = await response.json();
        
        if (sb.error) {
            alert('Stat block not found');
            return;
        }
        
        // Build the stat block HTML using your template
        const detailHTML = `
            <div class="statblock">
                <div class="statblock-card rounded overflow-hidden shadow-lg">
                    <div class="char_img">
                        ${sb.image_b64 ? `<img src="data:image/png;base64,${sb.image_b64}" style="max-width: 300px;"/>` : '<p style="color: #888;">No image uploaded</p>'}
                    </div>
                    <div class="char_detz">
                        <div class="Name font-bold text-xl mb-2">${sb.name}</div>
                        <h5 class="species">${sb.size} ${sb.creature_type}</h5><hr size="5">
                        <div class="rating">
                            <p><strong>Armor Class:</strong> ${sb.ac}</p>
                            <p><strong>Hit Points:</strong> ${sb.hp}</p>
                            <p><strong>Speed:</strong> ${sb.speed}</p>
                        </div><hr size="5">
                        <div class="container">
                            <div><strong>STR</strong><br>${sb.abilities.STR}</div>
                            <div><strong>DEX</strong><br>${sb.abilities.DEX}</div>
                            <div><strong>CON</strong><br>${sb.abilities.CON}</div>
                            <div><strong>INT</strong><br>${sb.abilities.INT}</div>
                            <div><strong>WIS</strong><br>${sb.abilities.WIS}</div>
                            <div><strong>CHA</strong><br>${sb.abilities.CHA}</div>
                        </div><hr size="5">
                        <div class="metrics">
                            <p><strong>Skills:</strong> ${sb.skills.length > 0 ? sb.skills.join(', ') : 'None'}</p>
                            <p><strong>Senses:</strong> ${sb.senses.length > 0 ? sb.senses.join(', ') : 'None'}</p>
                            <p><strong>Languages:</strong> ${sb.languages.length > 0 ? sb.languages.join(', ') : 'None'}</p>
                            <p><strong>Challenge:</strong> ${sb.cr}</p>
                            <p><strong>Proficiency Bonus:</strong> +${sb.pb}</p>
                        </div><hr size="5">
                        <div class="Traits">
                            <h5>Traits</h5>
                            ${sb.traits.length > 0 ? sb.traits.map(t => `<p>${t}</p>`).join('') : '<p>None</p>'}
                        </div><hr size="5">
                        <div class="Actions">
                            <h5>Actions</h5>
                            ${sb.actions.length > 0 ? sb.actions.map(a => `<p>${a}</p>`).join('') : '<p>None</p>'}
                        </div><hr size="5">
                        <button class="modal-btn" onclick="closeStatblockDetail(); showStatblockList();">Back to List</button>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('statblock-detail-content').innerHTML = detailHTML;
        document.getElementById('statblock-detail-modal').style.display = 'block';
    } catch (error) {
        console.error('Error fetching stat block detail:', error);
        alert('Error loading stat block details.');
    }
}


// Show create form modal
async function showStatblockForm() {
    closeStatblockMenu();
    
    try {
        // Load the form HTML
        const response = await fetch('/form.html');
        const html = await response.text();
        
        // Extract just the form content (not the full HTML page)
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const form = doc.querySelector('#statblock-form');
        
        if (!form) {
            alert('Error loading form');
            return;
        }
        
        // Insert form into modal
        document.getElementById('form-container').innerHTML = form.outerHTML;
        
        // Add submit button at the bottom
        const submitBtn = document.createElement('button');
        submitBtn.className = 'modal-btn';
        submitBtn.textContent = 'Save Stat Block';
        submitBtn.type = 'button';
        submitBtn.onclick = submitStatblockForm;
        document.getElementById('form-container').appendChild(submitBtn);
        
        document.getElementById('statblock-form-modal').style.display = 'block';
    } catch (error) {
        console.error('Error loading form:', error);
        alert('Error loading form. Make sure form.html exists.');
    }
}

// Submit the form
async function submitStatblockForm() {
    // Gather all form data
    const formData = {
        name: document.getElementById('char-name').value,
        size: document.getElementById('char-size').value,
        creature_type: document.getElementById('char-race').value,
        ac: parseInt(document.getElementById('armor-class').value),
        hp: parseInt(document.getElementById('hit-points').value),
        speed: document.getElementById('speed').value + " ft.",
        abilities: {
            STR: parseInt(document.getElementById('str').value),
            DEX: parseInt(document.getElementById('dex').value),
            CON: parseInt(document.getElementById('con').value),
            INT: parseInt(document.getElementById('int').value),
            WIS: parseInt(document.getElementById('wis').value),
            CHA: parseInt(document.getElementById('cha').value)
        },
        skills: Array.from(document.getElementById('skills').selectedOptions).map(opt => opt.text),
        senses: [], // Add if you have senses input
        languages: Array.from(document.getElementById('languages').selectedOptions).map(opt => opt.text),
        challenge_rating: parseInt(document.getElementById('challenges').value),
        traits: document.getElementById('traits').value.split('\n').filter(t => t.trim()),
        actions: document.getElementById('actions').value.split('\n').filter(a => a.trim())
    };
    
    // Validation
    if (!formData.name) {
        alert('Please enter a character name');
        return;
    }
    if (!formData.size) {
        alert('Please select a size');
        return;
    }
    if (!formData.creature_type) {
        alert('Please select a race/type');
        return;
    }
    
    try {
        // Send to backend
        const response = await fetch(`${API_URL}/statblock`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.inserted_id) {
            alert('Stat block created successfully!');
            closeStatblockForm();
            // Show the list with the new stat block
            showStatblockList();
        } else {
            alert('Error creating stat block: ' + JSON.stringify(result));
        }
    } catch (error) {
        console.error('Error submitting stat block:', error);
        alert('Error saving stat block. Check console for details.');
    }
}