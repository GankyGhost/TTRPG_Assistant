// Open menu modal
function openAudioMenu() {
    document.getElementById('audio-menu-modal').style.display = 'block';
}

// Open list modal
function openAudiolist() {
    document.getElementById('audio-list-modal').style.display = 'block';
}

// Close menu modal
function closeAudioMenu() {
    document.getElementById('audio-menu-modal').style.display = 'none';
}

// Close list modal
function closeAudioList() {
    document.getElementById('audio-list-modal').style.display = 'none';
}


// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Show list of saved movies
async function showAudioList() {
    closeAudioMenu();
    
    try {
        // Fetch all audio files from backend
        const response = await fetch(`${API_URL}/audio`);
        const audio_files = await response.json();
        
        // Display them in the list modal
        const container = document.getElementById('audio-list-container');
        container.innerHTML = '';
        
        if (audio_files.length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 20px;">No audio files saved yet. Create one!</p>';
        } else {
            audio_files.forEach(sb => {
                const item = document.createElement('div');
                item.className = 'audio-list-item';
                item.innerHTML = `
                    <h3>${sb.name}</h3>
                `;
                container.appendChild(item);
            });
        }
        
        document.getElementById('audio-list-modal').style.display = 'block';
    } catch (error) {
        console.error('Error fetching audio files:', error);
        alert('Error loading audio files. Make sure the backend is running.');
    }
}

