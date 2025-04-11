// === Menu mobile ===
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById("menu-btn");
    const menu = document.getElementById("mobile-menu");
    if (btn && menu) {
        btn.addEventListener("click", () => {
            menu.classList.toggle("hidden");
        });
    }

    initSearchInput();
    setupAjaxPagination();
    setupAjaxDelete();
    handleToasts();
});


// === Recherche AJAX ===
function initSearchInput() {
    const input = document.getElementById('search-input');
    if (!input) return;

    let timeout = null;

    input.addEventListener('input', function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const query = this.value;
            const url = `?query=${encodeURIComponent(query)}`;
            fetchPage(url);
        }, 300);
    });
}


// === Pagination AJAX ===
function setupAjaxPagination() {
    document.querySelectorAll('.pagination-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            fetchPage(this.href);
        });
    });
}

function fetchPage(url) {
    fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('table-body-container').innerHTML = data.html;
        document.getElementById('pagination').innerHTML = data.pagination;
        window.history.pushState({}, '', url);
        setupAjaxPagination();
        setupAjaxDelete();
    });
}


// === Toasts dynamiques ===
function handleToasts() {
    const url = new URL(window.location.href);

    // Toast succès ajout
    const toast = document.getElementById('toast-success');
    if (url.searchParams.get('success') === '1' && toast) {
        showToast(toast);
        url.searchParams.delete('success');
        window.history.replaceState({}, '', url);
    }

    // Toast succès édition
    const toastEdit = document.getElementById('toast-edit');
    if (url.searchParams.get('success_edit') === '1' && toastEdit) {
        showToast(toastEdit);
        url.searchParams.delete('success_edit');
        window.history.replaceState({}, '', url);
    }

    // Toast succès inscription
    if (url.searchParams.get('registered') === '1') {
        createInlineToast("Votre compte a été créé avec succès !");
        url.searchParams.delete('registered');
        window.history.replaceState({}, '', url);
    }

    // Toast succès login
    if (url.searchParams.get('login') === '1') {
        createInlineToast("Vous êtes connecté !");
        url.searchParams.delete('registered');
        window.history.replaceState({}, '', url);
    }
}

function showToast(toastElement) {
    toastElement.classList.remove('hidden');
    toastElement.classList.add('opacity-100');

    setTimeout(() => {
        toastElement.classList.remove('opacity-100');
        setTimeout(() => toastElement.classList.add('hidden'), 500);
    }, 3000);
}


// === Suppression AJAX ===
function setupAjaxDelete() {
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const subscriberId = this.dataset.id;
            if (!confirm("Supprimer cet adhérent ?")) return;

            fetch('/ajax/supprimer-adherent', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `subscriber_id=${subscriberId}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const row = document.getElementById(`row-${subscriberId}`);
                    if (row) row.remove();
                    createInlineToast("Adhérent supprimé avec succès !");
                } else {
                    createInlineToast("Erreur lors de la suppression", 'red');
                }
            });
        });
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}

function createInlineToast(message, color = 'green') {
    const toast = document.createElement('div');
    toast.className = `fixed top-5 right-5 bg-${color}-600 text-white px-4 py-2 rounded shadow z-50 transition-opacity duration-300`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('opacity-0');
        setTimeout(() => toast.remove(), 500);
    }, 2500);
}
