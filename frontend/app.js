const API_URL = 'http://127.0.0.1:5001';

// State
let token = localStorage.getItem('token');
let userRole = localStorage.getItem('role');

// DOM Elements
const authView = document.getElementById('auth-view');
const dashView = document.getElementById('dashboard-view');
const authForm = document.getElementById('auth-form');
const loginBtn = document.getElementById('login-btn');
const regBtn = document.getElementById('register-btn');
const errText = document.getElementById('auth-error');
const userBadge = document.getElementById('user-badge');
const logoutBtn = document.getElementById('logout-btn');
const notesContainer = document.getElementById('notes-container');
const createNoteForm = document.getElementById('create-note-form');
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-note-form');
const closeModalBtn = document.getElementById('close-modal-btn');

// Initialization
function init() {
    if (token) {
        showDashboard();
    } else {
        showAuth();
    }
}

// UI Management
function showAuth() {
    dashView.classList.remove('active');
    authView.classList.add('active');
}

function showDashboard() {
    authView.classList.remove('active');
    dashView.classList.add('active');
    userBadge.textContent = userRole || 'User';
    fetchNotes();
}

function showError(msg) {
    errText.textContent = msg;
    setTimeout(() => errText.textContent = '', 4000);
}

// Authentication
authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleAuth('/login');
});

regBtn.addEventListener('click', async () => {
    if (!authForm.checkValidity()) {
        authForm.reportValidity();
        return;
    }
    await handleAuth('/register');
});

async function handleAuth(endpoint) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.querySelector('input[name="role"]:checked').value;

    try {
        const res = await fetch(API_URL + endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, role })
        });
        
        const data = await res.json();
        
        if (!res.ok) {
            throw new Error(data.message || 'Authentication failed');
        }

        if (endpoint === '/register') {
            showError('Registered successfully. Logging you in...');
            // Auto login after register
            setTimeout(() => {
                loginBtn.click();
            }, 500);
            return;
        }

        token = data.access_token;
        userRole = data.role;
        localStorage.setItem('token', token);
        localStorage.setItem('role', userRole);
        
        authForm.reset();
        showDashboard();
        
    } catch (err) {
        showError(err.message);
    }
}

logoutBtn.addEventListener('click', () => {
    token = null;
    userRole = null;
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    showAuth();
});

// Notes CRUD
async function fetchNotes() {
    try {
        const res = await fetch(API_URL + '/allNotes', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        if (res.status === 401) {
            logoutBtn.click();
            return;
        }
        
        const notes = await res.json();
        renderNotes(notes);
    } catch (err) {
        console.error('Failed to fetch notes', err);
    }
}

function renderNotes(notes) {
    notesContainer.innerHTML = '';
    
    if (notes.length === 0) {
        notesContainer.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No notes yet. Create one!</p>';
        return;
    }

    notes.forEach(note => {
        const card = document.createElement('div');
        card.className = 'note-card';
        card.innerHTML = `
            <div class="note-header">
                <div class="note-title">
                    ${escapeHTML(note.title)} 
                    <span style="font-size: 0.8rem; color: var(--text-secondary); font-weight: normal; margin-left: 0.5rem;">by ${escapeHTML(note.username || 'Unknown')}</span>
                </div>
                <div class="note-actions">
                    <button class="icon-btn" onclick="openEditModal(${note.id}, '${escapeHTML(note.title).replace(/'/g, "\\'")}', '${escapeHTML(note.content).replace(/'/g, "\\'")}')">Edit</button>
                    <button class="icon-btn delete" onclick="deleteNote(${note.id})">Delete</button>
                </div>
            </div>
            <div class="note-content">${escapeHTML(note.content)}</div>
        `;
        notesContainer.appendChild(card);
    });
}

createNoteForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;

    try {
        await fetch(API_URL + '/notes', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token 
            },
            body: JSON.stringify({ title, content })
        });
        
        createNoteForm.reset();
        fetchNotes();
    } catch (err) {
        console.error(err);
    }
});

async function deleteNote(id) {
    if (!confirm('Are you sure you want to delete this note?')) return;
    
    try {
        await fetch(`${API_URL}/notes/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + token }
        });
        fetchNotes();
    } catch (err) {
        alert('Unauthorized or failed to delete');
    }
}

// Edit Modal Logic
window.openEditModal = function(id, title, content) {
    document.getElementById('edit-note-id').value = id;
    document.getElementById('edit-note-title').value = title;
    document.getElementById('edit-note-content').value = content;
    editModal.classList.add('active');
}

closeModalBtn.addEventListener('click', () => {
    editModal.classList.remove('active');
});

editForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('edit-note-id').value;
    const title = document.getElementById('edit-note-title').value;
    const content = document.getElementById('edit-note-content').value;

    try {
        await fetch(`${API_URL}/notes/${id}`, {
            method: 'PUT',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token 
            },
            body: JSON.stringify({ title, content })
        });
        
        editModal.classList.remove('active');
        fetchNotes();
    } catch (err) {
        alert('Failed to update note');
    }
});

// Utility
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Boot
init();
