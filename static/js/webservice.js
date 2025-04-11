function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('siret-input');
    const button = document.getElementById('check-btn');
    const output = document.getElementById('xml-output');
    const codeBlock = output.querySelector('code');

    button.addEventListener('click', () => {
        const siret = input.value.trim();
        if (!siret) {
            output.textContent = "Veuillez entrer un SIRET";
            output.classList.remove('hidden');
            return;
        }

        fetch('/check-siret/ajax/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `siret=${encodeURIComponent(siret)}`
        })
            .then(res => res.json())
            .then(data => {
                codeBlock.textContent = data.xml;
                output.classList.remove('hidden');
                Prism.highlightElement(codeBlock);
            });
    });
});