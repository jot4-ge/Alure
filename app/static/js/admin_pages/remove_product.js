document.addEventListener('DOMContentLoaded', () => {
    // 1. Seleção de Elementos do DOM
    const removeForm = document.getElementById('removeProductForm');
    const productIdInput = document.getElementById('productId');
    const productNameInput = document.getElementById('productName');
    const messageArea = document.getElementById('messageArea');

    // Flag para evitar chamadas recursivas entre os listeners
    let isUpdating = false;

    async function findProductById() {
        if (isUpdating) return;
        const productId = productIdInput.value.trim();

        if (!productId) {
            productNameInput.value = '';
            return;
        }

        isUpdating = true;
        try {
            const response = await fetch(`/api/products/${productId}`);
            if (response.ok) {
                const product = await response.json();
                productNameInput.value = product.nome;
            } else {
                productNameInput.value = 'Produto não encontrado';
            }
        } catch (error) {
            console.error('Erro ao buscar produto por ID:', error);
            productNameInput.value = 'Erro na busca';
        } finally {
            isUpdating = false;
        }
    }

    async function findProductByName() {
        if (isUpdating) return;
        const productName = productNameInput.value.trim();

        if (!productName) {
            productIdInput.value = '';
            return;
        }

        isUpdating = true;
        try {
            // Chama o novo endpoint de busca, codificando o nome para a URL
            const response = await fetch(`/api/products/get-name/${encodeURIComponent(productName)}`);
            if (response.ok) {
                const product = await response.json();
                productIdInput.value = product.id;
            } else {
                productIdInput.value = 'ID não encontrado';
            }
        } catch (error) {
            console.error('Erro ao buscar produto por Nome:', error);
            productIdInput.value = 'Erro na busca';
        } finally {
            isUpdating = false;
        }
    }

    // 2. Adição dos Event Listeners
    // Listeners para o campo de ID
    productIdInput.addEventListener('blur', findProductById);
    productIdInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            findProductById();
        }
    });

    // Listeners para o campo de Nome
    productNameInput.addEventListener('blur', findProductByName);
    productNameInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            findProductByName();
        }
    });

    // 3. Lógica de Submissão do Formulário
    if (removeForm) {
        removeForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const productId = productIdInput.value.trim();
            if (!productId || productIdInput.value.includes('não encontrado')) {
                messageArea.textContent = 'Por favor, insira um ID de produto válido.';
                messageArea.className = 'message-area error';
                return;
            }

            const isConfirmed = confirm(`Você tem certeza que deseja remover o produto "${productNameInput.value}" (ID: ${productId})? Esta ação não pode ser desfeita.`);
            if (!isConfirmed) return;

            messageArea.textContent = `Removendo produto com ID ${productId}...`;
            messageArea.className = 'message-area';
            messageArea.style.display = 'block';

            try {
                const response = await fetch(`/api/products/${productId}`, {
                    method: 'DELETE',
                });

                if (response.ok || response.status === 204) {
                    messageArea.textContent = `Produto com ID "${productId}" removido com sucesso!`;
                    messageArea.className = 'message-area success';
                    removeForm.reset();
                } else {
                    const result = await response.json();
                    messageArea.textContent = `Erro ao remover produto: ${result.error || 'Resposta inesperada.'}`;
                    messageArea.className = 'message-area error';
                }
            } catch (error) {
                messageArea.textContent = 'Erro de conexão. Não foi possível conectar ao servidor.';
                messageArea.className = 'message-area error';
                console.error('Erro na requisição de remoção:', error);
            }
        });
    }
});