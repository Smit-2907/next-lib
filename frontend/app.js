/**
 * NexLib Core Logic - 120% Consistent & Premium
 */

const API_URL = 'http://127.0.0.1:8000';

// --- SHARED UTILITIES ---

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const icons = { success: 'fa-circle-check', danger: 'fa-circle-xmark', warning: 'fa-triangle-exclamation', info: 'fa-circle-info' };
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fas ${icons[type]}" style="color: var(--${type})"></i><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 400); }, 4000);
}

function checkAuth(roleRequired = null) {
    const token = sessionStorage.getItem('token');
    const role = sessionStorage.getItem('role');
    const path = window.location.pathname.toLowerCase();
    
    if (!token) {
        // If no token, only allow landing, login and register
        const permitted = ['login.html', 'register.html', 'index.html'];
        const isPermitted = permitted.some(p => path.endsWith(p)) || path === '/' || path.endsWith('/');
        
        if (!isPermitted) {
            window.location.href = 'login.html';
        }
        return null;
    }
    
    // If a specific role is required and user doesn't have it, redirect to OWN dashboard
    if (roleRequired && role !== roleRequired) {
        window.location.href = role === 'admin' ? 'admin_dashboard.html' : 'student_dashboard.html';
    }
    return role;
}

function logout() {
    sessionStorage.clear();
    showToast('Session terminated safely');
    setTimeout(() => window.location.href = 'login.html', 1000);
}

async function fetchApi(endpoint, method = 'GET', body = null) {
    const token = sessionStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    try {
        const response = await fetch(`${API_URL}${endpoint}`, { method, headers, body: body ? JSON.stringify(body) : null });
        if (response.status === 401) { sessionStorage.clear(); window.location.href = 'login.html'; return null; }
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'API Error');
        return data;
    } catch (err) {
        showToast(err.message, 'danger');
        return null;
    }
}

// --- UI INJECTION ---

function injectLayout(activePage) {
    const sidebar = document.getElementById('sidebar-container');
    const header = document.getElementById('header-profile');
    const role = sessionStorage.getItem('role');
    const isAdmin = role === 'admin';
    
    // Inject Sidebar
    if (sidebar) {
        const menu = isAdmin ? [
            { href: 'admin_dashboard.html', icon: 'fa-chart-pie', label: 'Monitor' },
            { href: 'books.html', icon: 'fa-book-stack', label: 'Management' },
            { href: 'issue.html', icon: 'fa-plus-circle', label: 'Issue Asset' },
            { href: 'return.html', icon: 'fa-rotate-left', label: 'Returns' }
        ] : [
            { href: 'student_dashboard.html', icon: 'fa-house-user', label: 'My Hub' },
            { href: 'books.html', icon: 'fa-magnifying-glass', label: 'Explore' },
            { href: 'issue.html', icon: 'fa-book-medical', label: 'Issue Book' },
            { href: 'return.html', icon: 'fa-clock-rotate-left', label: 'Archive' }
        ];
        
        sidebar.innerHTML = `
            <div class="sidebar-brand"><i class="fas fa-book-bookmark"></i><span>NexLib</span></div>
            <ul class="nav-menu">
                ${menu.map(i => `<li><a href="${i.href}" class="nav-link ${activePage.includes(i.href) ? 'active' : ''}"><i class="fas ${i.icon}"></i><span>${i.label}</span></a></li>`).join('')}
            </ul>
            <button onclick="logout()" class="btn btn-glass" style="width:100%; color:var(--danger); border-color:rgba(244,63,94,0.1)">
                <i class="fas fa-power-off"></i><span>Sign Out</span>
            </button>
        `;
    }

    // Inject Header Profile
    if (header) {
        header.innerHTML = `
            <div style="text-align: right;">
                <p style="font-weight: 700;">${isAdmin ? 'Systems Admin' : 'Nexus Student'}</p>
                <p style="font-size: 0.8rem; color: ${isAdmin ? 'var(--primary)' : 'var(--secondary)'};">● ${role.toUpperCase()}</p>
            </div>
            <img src="https://images.unsplash.com/photo-${isAdmin ? '1472099645785-5658abf4ff4e' : '1543269865-cbf427effbad'}?q=80&w=40&h=40&fit=crop" style="border-radius: 50%; border: 2px solid var(--${isAdmin ? 'primary' : 'secondary'});">
        `;
    }
}

// --- VIEW LOGIC ---

async function loadDashboard() {
    const role = sessionStorage.getItem('role');
    if (role === 'admin') {
        const stats = await fetchApi('/reports/summary');
        if (stats) {
            renderAdminDash(stats);
            if (typeof initAdminChart === 'function') initAdminChart(stats);
        }
        const issues = await fetchApi('/issued');
        if (issues) renderActivityTable(issues.slice(0, 5));
        
        // --- NEW OPERATION: CATEGORY SYNC ---
        const catStats = await fetchApi('/reports/categories');
        if (catStats) renderCategoryAnalytics(catStats);
    } else {

        const history = await fetchApi('/my-issues');
        if (history) renderStudentPortal(history);
    }
}

function renderAdminDash(stats) {
    const grid = document.getElementById('stats-grid');
    if (!grid) return;
    const items = [
        { label: 'Books', val: stats.total_books, icon: 'fa-book', col: 'var(--primary)' },
        { label: 'Total Stock', val: stats.available_books, icon: 'fa-layer-group', col: 'var(--secondary)' },
        { label: 'Issued', val: stats.issued_books, icon: 'fa-hand-holding', col: 'var(--warning)' },
        { label: 'Students', val: stats.total_students, icon: 'fa-users', col: 'var(--accent)' }
    ];
    grid.innerHTML = items.map(i => `
        <div class="stat-card glass">
            <div class="stat-icon" style="background:rgba(255,255,255,0.03); color:${i.col}"><i class="fas ${i.icon}"></i></div>
            <div class="stat-info"><span class="label">${i.label}</span><span class="value">${i.val}</span></div>
        </div>
    `).join('');
}

function renderActivityTable(issues) {
    const list = document.getElementById('activity-list');
    if (!list) return;
    const tableHeader = list.closest('table').querySelector('thead tr');
    if (tableHeader && !tableHeader.innerHTML.includes('Actions')) {
        tableHeader.innerHTML += '<th>Actions</th>';
    }

    list.innerHTML = issues.map(i => {
        const isPending = i.status === 'pending';
        const isOverdue = i.status === 'issued' && new Date(i.due_date) < new Date();
        const statusClass = isPending ? 'badge-info' : (isOverdue ? 'badge-danger' : (i.status === 'issued' ? 'badge-warning' : 'badge-success'));
        
        return `
            <tr>
                <td style="font-weight:600">${i.student_name}</td>
                <td><strong>${i.book_title}</strong></td>
                <td>${i.issue_date}</td>
                <td><span style="color:${isOverdue ? 'var(--danger)' : 'inherit'}">${i.due_date}</span></td>
                <td><span class="badge ${statusClass}">${i.status.toUpperCase()}</span></td>
                <td>
                    ${isPending ? `
                        <div style="display:flex; gap:8px;">
                            <button onclick="handleIssueAction(${i.id}, 'approve')" class="btn btn-primary" style="padding: 5px 10px; font-size: 0.7rem;"><i class="fas fa-check"></i></button>
                            <button onclick="handleIssueAction(${i.id}, 'reject')" class="btn btn-glass" style="padding: 5px 10px; font-size: 0.7rem; color:var(--danger); border-color:var(--danger);"><i class="fas fa-times"></i></button>
                        </div>
                    ` : '<span style="color:var(--text-muted); font-size:0.8rem;">---</span>'}
                </td>
            </tr>
        `;
    }).join('') || '<tr><td colspan="6" class="text-center">No recent activity</td></tr>';
}

async function handleIssueAction(id, action) {
    const res = await fetchApi(`/issue/${action}/${id}`, 'POST');
    if (res) {
        showToast(`Request ${action}ed successfully`, 'success');
        loadDashboard();
    }
}

function renderStudentPortal(history) {
    const pending = history.filter(h => h.status === 'pending').length;
    const active = history.filter(h => h.status === 'issued').length;
    const overdue = history.filter(h => h.status === 'issued' && new Date(h.due_date) < new Date()).length;
    
    const summary = document.getElementById('student-summary');
    if (summary) {
        summary.innerHTML = `
            <div class="stat-card glass"><div class="stat-icon" style="color:var(--warning)"><i class="fas fa-clock"></i></div><div class="stat-info"><span class="label">Pending Requests</span><span class="value">${pending}</span></div></div>
            <div class="stat-card glass"><div class="stat-icon" style="color:var(--secondary)"><i class="fas fa-book-reader"></i></div><div class="stat-info"><span class="label">Currently Reading</span><span class="value">${active}</span></div></div>
            <div class="stat-card glass" style="border-color:${overdue? 'var(--danger)':'var(--accent)'}"><div class="stat-icon" style="color:var(--danger)"><i class="fas fa-exclamation-circle"></i></div><div class="stat-info"><span class="label">Overdue Items</span><span class="value">${overdue}</span></div></div>
        `;
    }
    const list = document.getElementById('history-list');
    if (list) {
        list.innerHTML = history.map(i => {
            const isPending = i.status === 'pending';
            const isOverdue = i.status === 'issued' && new Date(i.due_date) < new Date();
            const statusClass = isPending ? 'badge-info' : (isOverdue ? 'badge-danger' : (i.status === 'issued' ? 'badge-warning' : 'badge-success'));
            
            return `
                <tr>
                    <td style="font-weight:700">${i.book_title}</td>
                    <td>${i.issue_date}</td>
                    <td><span style="color:${isOverdue ? 'var(--danger)' : 'inherit'}">${i.due_date}</span></td>
                    <td><span class="badge ${statusClass}">${i.status.toUpperCase()}</span></td>
                    <td>${isPending ? 'Waiting for Admin...' : `₹${i.fine}`}</td>
                </tr>
            `;
        }).join('') || '<tr><td colspan="5" class="text-center">Your library account is fresh.</td></tr>';
    }
}

function renderCategoryAnalytics(cats) {
    const container = document.getElementById('category-stats');
    if (!container) return;
    const total = cats.reduce((acc, c) => acc + c.count, 0);
    container.innerHTML = `
        <div class="glass" style="padding: 30px; border-radius: 20px;">
            <h3 style="margin-bottom:20px;">Genre Distribution</h3>
            ${cats.map(c => `
                <div style="margin-bottom:15px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span>${c.category}</span>
                        <span style="font-weight:700">${Math.round((c.count/total)*100)}%</span>
                    </div>
                    <div style="height:8px; background:rgba(255,255,255,0.05); border-radius:4px; overflow:hidden;">
                        <div style="width:${(c.count/total)*100}%; height:100%; background:var(--primary); box-shadow:0 0 10px var(--primary)"></div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

// --- CATALOG ---


async function loadCatalog(search = '') {
    const books = await fetchApi(`/books${search ? `?search=${encodeURIComponent(search)}` : ''}`);
    if (!books) return;
    const role = sessionStorage.getItem('role');
    const container = document.getElementById('books-container');
    if (!container) return;
    
    // Check global view mode (defined in books.html for admin)
    const viewMode = (role === 'admin' && typeof currentView !== 'undefined') ? currentView : (role === 'admin' ? 'table' : 'grid');
    
    if (viewMode === 'table' && role === 'admin') {
        container.innerHTML = `
            <div class="glass table-card">
                <table>
                    <thead><tr><th>Asset</th><th>Volume Status</th><th>Genre</th><th>Management</th></tr></thead>
                    <tbody>${books.map(b => `<tr>
                        <td style="display:flex; align-items:center; gap:20px;">
                            <img src="${b.cover_url || 'https://images.unsplash.com/photo-1544947950-fa07a98d237f'}" class="book-cover">
                            <div><p style="font-weight:700; font-size:1.1rem">${b.title}</p><p style="color:var(--text-muted); font-size:0.85rem">${b.author}</p></div>
                        </td>
                        <td><span class="badge ${b.quantity>0?'badge-success':'badge-danger'}" style="padding: 8px 15px;">${b.quantity} In Stock</span></td>
                        <td><span class="badge badge-info">${b.category||'General'}</span></td>
                        <td>
                            <div style="display:flex; gap:10px;">
                                <button onclick='openBookModal(${JSON.stringify(b).replace(/'/g, "&#39;")})' class="btn btn-glass" style="padding: 10px 14px;"><i class="fas fa-pen"></i></button>
                                <button onclick="deleteBook(${b.id})" class="btn btn-glass" style="padding: 10px 14px; color: var(--danger);"><i class="fas fa-trash-alt"></i></button>
                            </div>
                        </td>
                    </tr>`).join('')}</tbody>
                </table>
            </div>
        `;
    } else {
        // Grid View (Standard for Students, Optional for Admin)
        const isAdmin = role === 'admin';
        container.innerHTML = `
            <div class="books-grid">${books.map(b => `
                <div class="book-card glass" style="position:relative;">
                    ${isAdmin ? `<div style="position:absolute; top:15px; right:15px; display:flex; gap:8px; z-index:10;">
                        <button onclick='openBookModal(${JSON.stringify(b).replace(/'/g, "&#39;")})' class="btn btn-primary" style="padding: 8px 12px; border-radius: 10px;"><i class="fas fa-pen"></i></button>
                    </div>` : ''}
                    <img src="${b.cover_url || 'https://images.unsplash.com/photo-1544947950-fa07a98d237f'}" class="book-card-cover">
                    <div class="book-info">
                        <span class="badge badge-info" style="margin-bottom:10px;">${b.category||'Genre'}</span>
                        <h3 style="font-size:1.3rem; margin-bottom:5px;">${b.title}</h3>
                        <p style="color:var(--text-muted); margin-bottom:15px;">${b.author}</p>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:600; color:${b.quantity>0?'var(--accent)':'var(--danger)'}">
                                ${b.quantity > 0 ? `${b.quantity} Available` : 'Sync Pending'}
                            </span>
                            ${!isAdmin ? `<button onclick="reqIssue(${b.id})" class="btn btn-primary" ${b.quantity<=0?'disabled':''}>${b.quantity>0?'Issue Asset':'Reserve'}</button>` : ''}
                        </div>
                    </div>
                </div>
            `).join('')}</div>
        `;
    }
}

let timer;
function debounce(val) { clearTimeout(timer); timer = setTimeout(() => loadCatalog(val), 400); }

async function reqIssue(id) {
    const res = await fetchApi('/issue', 'POST', { book_id: id });
    if (res) { showToast('Issue request successful!', 'success'); setTimeout(() => window.location.href='student_dashboard.html', 1500); }
}

// --- BOOTSTRAP ---
document.addEventListener('DOMContentLoaded', () => {
    let page = window.location.pathname.split('/').pop().toLowerCase() || 'index.html';
    const role = checkAuth();
    
    // Core pages that shared between roles
    const sharedPages = ['books.html', 'issue.html', 'return.html'];
    const isShared = sharedPages.some(p => page === p);
    
    if (role && !['index.html', 'login.html', 'register.html'].some(p => page.includes(p))) {
        injectLayout(page);
    }
    
    if (page.includes('dashboard')) loadDashboard();
    
    // Ensure catalog and issue functionality works
    if (page === 'books.html') loadCatalog();
    if (page === 'issue.html' && role !== 'admin') {
        // Extra check for student issue page specific logic if needed
    }
});

window.logout = logout;
window.debounce = debounce;
window.reqIssue = reqIssue;
window.handleIssueAction = handleIssueAction;
