// ml_dashboard — main.js

// ── Modal helpers ──
function openModal(id) {
  document.getElementById(id).classList.add('open');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}
// Close on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', function(e) {
    if (e.target === this) this.classList.remove('open');
  });
});

// ── Alert auto-dismiss ──
document.querySelectorAll('.alert[data-dismiss]').forEach(el => {
  setTimeout(() => el.remove(), parseInt(el.dataset.dismiss) || 4000);
});

// ── Confirm delete ──
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', function(e) {
    if (!confirm(this.dataset.confirm || 'Are you sure?')) e.preventDefault();
  });
});

// ── Live table search ──
const searchInput = document.getElementById('tableSearch');
if (searchInput) {
  searchInput.addEventListener('input', function() {
    const q = this.value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

// ── Sidebar active link ──
const currentPath = window.location.pathname;
document.querySelectorAll('.sidebar a').forEach(a => {
  if (a.getAttribute('href') && currentPath.includes(a.getAttribute('href').split('/')[1])) {
    a.classList.add('active');
  }
});

// ── Toast notification ──
function showToast(msg, type = 'info') {
  const colors = { info: '#00e5ff', success: '#00ffa3', error: '#ff4d6d' };
  const t = document.createElement('div');
  t.style.cssText = `
    position:fixed; bottom:1.5rem; right:1.5rem; z-index:999;
    background:#131929; border:1px solid ${colors[type]};
    color:${colors[type]}; padding:.8rem 1.2rem;
    border-radius:10px; font-size:.88rem;
    box-shadow:0 8px 32px rgba(0,0,0,.5);
    animation: slideUp .3s ease;
  `;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ── Inject keyframe for toast ──
if (!document.getElementById('toastStyle')) {
  const s = document.createElement('style');
  s.id = 'toastStyle';
  s.textContent = `
    @keyframes slideUp {
      from { transform: translateY(20px); opacity: 0; }
      to   { transform: translateY(0);    opacity: 1; }
    }`;
  document.head.appendChild(s);
}
