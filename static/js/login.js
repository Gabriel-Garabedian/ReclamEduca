document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.querySelector('input[name="username"]');
    if (userInput) userInput.focus();

    const senhaInput = document.querySelector('input[name="senha"]');
    if (senhaInput) {
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.textContent = 'Mostrar';
        toggleBtn.classList.add('toggle-btn');

        const wrapper = document.createElement('div');
        wrapper.classList.add('toggle-wrapper');
        wrapper.appendChild(toggleBtn);

        senhaInput.parentNode.insertBefore(wrapper, senhaInput.nextSibling);

        toggleBtn.addEventListener('click', () => {
            const isPassword = senhaInput.type === 'password';
            senhaInput.type = isPassword ? 'text' : 'password';
            toggleBtn.textContent = isPassword ? 'Ocultar' : 'Mostrar';
        });
    }

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            if (senhaInput && senhaInput.value.length < 8) {
                alert('A senha deve ter pelo menos 8 caracteres!');
                e.preventDefault();
            }
        });
    }
});
