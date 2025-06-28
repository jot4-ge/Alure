document.addEventListener('DOMContentLoaded', () => {
    // --- Seleção de Elementos do DOM ---
    const loadProductIdInput = document.getElementById('loadProductId');
    const loadProductBtn = document.getElementById('loadProductBtn');
    //Seleção dos novos elementos para busca por nome
    const loadProductNameInput = document.getElementById('loadProductName');
    const loadProductByNameBtn = document.getElementById('loadProductByNameBtn');

    const editProductForm = document.getElementById('editProductForm');

    // Campos do formulário de edição
    const productIdInput = document.getElementById('productId');
    const productNameInput = document.getElementById('productName');
    const productDescriptionInput = document.getElementById('productDescription');
    const productPriceInput = document.getElementById('productPrice');
    const productStockInput = document.getElementById('productStock');
    const productImageInput = document.getElementById('productImage');
    const currentProductImage = document.getElementById('currentProductImage');
    const productSizeSelect = document.getElementById('productSize');
    const productCategorySelect = document.getElementById('productCategory');
    const messageArea = document.getElementById('messageArea');

    let currentProductId = null;

    // --- Funções Auxiliares ---

    function showMessage(msg, type) {
        messageArea.textContent = msg;
        messageArea.className = `message-area ${type}`;
        messageArea.style.display = 'block';
    }

    function clearMessage() {
        messageArea.style.display = 'none';
        messageArea.textContent = '';
        messageArea.className = 'message-area';
    }

    function resetForm() {
        editProductForm.style.display = 'none';
        editProductForm.reset();
        currentProductId = null;
        currentProductImage.src = '';
        currentProductImage.alt = '';
        currentProductImage.style.display = 'none';
    }

    //Função dedicada para preencher o formulário, evitando duplicação de código.
    function populateFormWithProductData(productData) {
        productIdInput.value = productData.id;
        productNameInput.value = productData.nome;
        productDescriptionInput.value = productData.descricao;
        productPriceInput.value = productData.preco.toFixed(2).replace('.', ',');
        productStockInput.value = productData.estoque;
        productSizeSelect.value = productData.tamanho;
        productCategorySelect.value = productData.categoria;

        if (productData.image_filename) {
            currentProductImage.src = `/static/img/clothes/${productData.image_filename}`;
            currentProductImage.alt = `Imagem atual de ${productData.nome}`;
            currentProductImage.style.display = 'block';
        } else {
            currentProductImage.style.display = 'none';
        }

        currentProductId = productData.id;
        editProductForm.style.display = 'block';
        showMessage('Dados do produto carregados com sucesso! Agora você pode editá-los.', 'success');
    }

    // --- Event Listeners ---

    // Listener para o botão "Carregar por ID"
    loadProductBtn.addEventListener('click', async () => {
        clearMessage();
        resetForm();
        const idToLoad = loadProductIdInput.value.trim();
        if (!idToLoad) {
            showMessage('Por favor, digite o ID do produto.', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/products/${idToLoad}`);
            const productData = await response.json();

            if (response.ok) {
                populateFormWithProductData(productData); // Usa a função auxiliar
            } else {
                showMessage(productData.error || 'Produto não encontrado. Verifique o ID.', 'error');
            }
        } catch (error) {
            console.error('Erro ao carregar por ID:', error);
            showMessage('Erro de conexão ao carregar dados do produto.', 'error');
        }
    });

    // Listener para o botão "Carregar por Nome"
    loadProductByNameBtn.addEventListener('click', async () => {
        clearMessage();
        resetForm();
        const nameToLoad = loadProductNameInput.value.trim();
        if (!nameToLoad) {
            showMessage('Por favor, digite o nome do produto.', 'error');
            return;
        }

        try {
            // Chama o endpoint de busca por nome
            const response = await fetch(`/api/products/get-name/${encodeURIComponent(nameToLoad)}`);
            const productData = await response.json();

            if (response.ok) {
                populateFormWithProductData(productData); // Reutiliza a mesma função
            } else {
                showMessage(productData.error || 'Produto não encontrado. Verifique o nome.', 'error');
            }
        } catch (error) {
            console.error('Erro ao carregar por Nome:', error);
            showMessage('Erro de conexão ao carregar dados do produto.', 'error');
        }
    });

    // Listener para submeter o formulário de edição (sem alterações na lógica interna)
    editProductForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearMessage();

        if (!currentProductId) {
            showMessage('Nenhum produto carregado para atualizar.', 'error');
            return;
        }

        const formData = new FormData(editProductForm); // Forma mais simples de pegar todos os dados
        // O FormData já pega os valores dos inputs, selects, etc.
        // Apenas precisamos ajustar o preço e adicionar a imagem se houver.
        formData.set('productPrice', productPriceInput.value.replace(',', '.'));

        // O campo de imagem só é adicionado se um novo arquivo for selecionado.
        // O FormData lida com isso automaticamente se o input 'productImage' tiver um arquivo.

        try {
            const response = await fetch(`/api/products/${currentProductId}`, {
                method: 'PUT', // O método correto para atualização completa é PUT
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                showMessage('Produto atualizado com sucesso!', 'success');
                // Atualiza a imagem na página se uma nova foi enviada
                if (data.image_filename) {
                    currentProductImage.src = `/static/img/clothes/${data.image_filename}?t=${new Date().getTime()}`;
                }
                setTimeout(() => {
                    window.location.href = '/view_products_page';
                }, 1500);
            } else {
                showMessage(data.error || 'Erro ao atualizar produto.', 'error');
            }
        } catch (error) {
            console.error('Erro ao atualizar produto:', error);
            showMessage('Erro de conexão ao atualizar produto.', 'error');
        }
    });

    // Código para carregar ID da URL (sem alterações)
    const initialProductIdFromUrl = new URLSearchParams(window.location.search).get('id');
    if (initialProductIdFromUrl) {
        loadProductIdInput.value = initialProductIdFromUrl;
        loadProductBtn.click();
    }
});