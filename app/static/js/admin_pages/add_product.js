// /home/tiago/Projects/LojaVirtual/app/static/js/admin_pages/add_product.js

document.addEventListener('DOMContentLoaded', () => {
    const priceInput = document.getElementById('productPrice');

    if (priceInput) {
        priceInput.addEventListener('input', (event) => {
            let value = event.target.value;
            value = value.replace(/[^0-9,.]/g, '');
            const parts = value.split(/[,.]/);
            if (parts.length > 2) {
                value = parts[0] + ',' + parts.slice(1).join('');
            }
            value = value.replace('.', ',');
            event.target.value = value;
        });

        priceInput.addEventListener('blur', (event) => {
            let value = event.target.value;
            if (value) {
                let numericValue = parseFloat(value.replace(',', '.'));
                if (!isNaN(numericValue)) {
                    event.target.value = numericValue.toFixed(2).replace('.', ',');
                } else {
                    event.target.value = '';
                }
            }
        });
    }
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) { // Adicione uma verificação para garantir que o formulário foi encontrado
        addProductForm.addEventListener('submit', async function(event) {
            console.log("Evento de submit do formulário disparado!");
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const messageArea = document.getElementById('messageArea');

            const productImageFile = formData.get('productImage');
            if (!productImageFile || productImageFile.name === '') {
                messageArea.textContent = 'Por favor, selecione uma imagem para o produto.';
                messageArea.className = 'message-area error';
                return;
            }

            messageArea.textContent = 'Adicionando produto...';
            messageArea.className = 'message-area';

            try {
                const response = await fetch('/api/products', { // Endpoint da API
                    method: 'POST',
                    body: formData
                });
                console.log("Requisição fetch enviada.");

                const result = await response.json();

                if (response.ok) {
                    messageArea.textContent = 'Produto adicionado com sucesso! ID: ' + result.id;
                    messageArea.className = 'message-area success';
                    form.reset(); // Limpa o formulário
                } else {
                    messageArea.textContent = 'Erro ao adicionar produto: ' + (result.error || 'Erro desconhecido.');
                    messageArea.className = 'message-area error';
                    console.error('Erro da API:', result);
                }
            } catch (error) {
                messageArea.textContent = 'Erro de conexão: Não foi possível conectar ao servidor.';
                messageArea.className = 'message-area error';
                console.error('Erro na requisição:', error);
            }
        });
    } else {
        console.error("Erro: Formulário com ID 'addProductForm' não encontrado.");
    }
});