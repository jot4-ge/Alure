// app/static/js/admin.js

document.addEventListener('DOMContentLoaded', () => {
    const addProductForm = document.getElementById('addProductForm');
    const productListDiv = document.getElementById('productList');

    // Altere esta URL base para onde suas rotas Bottle de produto estarão
    // Por exemplo, se seu Bottle roda em localhost:8080 e a rota é /api/products
    const API_BASE_URL = 'http://localhost:8080/api/products'; 

    loadProducts();

    addProductForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const productName = document.getElementById('productName').value;
        const productCategory = document.getElementById('productCategory').value;
        const productPrice = parseFloat(document.getElementById('productPrice').value);
        const productImage = document.getElementById('productImage').value;
        const productDescription = document.getElementById('productDescription').value;

        const productData = {
            name: productName,
            category: productCategory,
            price: productPrice,
            image: productImage,
            description: productDescription
        };

        const submitButton = addProductForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Enviando...';
        submitButton.disabled = true;

        try {
            const productIdToEdit = addProductForm.dataset.editingId;
            if (productIdToEdit) {
                await updateProduct(productIdToEdit, productData);
                delete addProductForm.dataset.editingId;
                submitButton.textContent = 'Adicionar Produto'; // Volta para o texto original
            } else {
                await addProduct(productData);
            }
            addProductForm.reset();
            loadProducts(); // Recarrega a lista
        } catch (error) {
            console.error('Erro ao salvar produto:', error);
            alert('Ocorreu um erro ao salvar o produto. Verifique o console para mais detalhes.');
        } finally {
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });

    async function addProduct(product) {
        try {
            const response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(product),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erro ao adicionar produto');
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição POST:', error);
            throw error;
        }
    }

    async function updateProduct(id, product) {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(product),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erro ao atualizar produto');
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição PUT:', error);
            throw error;
        }
    }

    async function deleteProduct(id) {
        if (!confirm('Tem certeza que deseja excluir este produto?')) {
            return;
        }
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erro ao excluir produto');
            }
            loadProducts();
        } catch (error) {
            console.error('Erro na requisição DELETE:', error);
            alert('Ocorreu um erro ao excluir o produto. Verifique o console para mais detalhes.');
        }
    }

    async function loadProducts() {
        try {
            const response = await fetch(API_BASE_URL);
            if (!response.ok) {
                throw new Error('Erro ao carregar produtos');
            }
            const products = await response.json();
            productListDiv.innerHTML = '';
            products.forEach(product => renderProduct(product));
        } catch (error) {
            console.error('Erro ao carregar produtos:', error);
            productListDiv.innerHTML = '<p>Erro ao carregar produtos. Tente novamente mais tarde.</p>';
        }
    }

    function renderProduct(product) {
        const productCard = document.createElement('div');
        productCard.classList.add('product-card-admin');
        productCard.dataset.id = product.id;

        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Categoria: ${product.category}</p>
            <p class="price">R$ ${product.price.toFixed(2).replace('.', ',')}</p>
            <p>${product.description}</p>
            <div class="actions">
                <button class="edit-btn">Editar</button>
                <button class="delete-btn">Excluir</button>
            </div>
        `;

        productListDiv.appendChild(productCard);

        productCard.querySelector('.edit-btn').addEventListener('click', () => editProduct(product.id));
        productCard.querySelector('.delete-btn').addEventListener('click', () => deleteProduct(product.id));
    }

    async function editProduct(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`);
            if (!response.ok) {
                throw new Error('Erro ao buscar produto para edição');
            }
            const productToEdit = await response.json();

            document.getElementById('productName').value = productToEdit.name;
            document.getElementById('productCategory').value = productToEdit.category;
            document.getElementById('productPrice').value = productToEdit.price;
            document.getElementById('productImage').value = productToEdit.image;
            document.getElementById('productDescription').value = productToEdit.description;

            addProductForm.dataset.editingId = productToEdit.id;
            addProductForm.querySelector('button[type="submit"]').textContent = 'Atualizar Produto';
        } catch (error) {
            console.error('Erro ao carregar produto para edição:', error);
            alert('Ocorreu um erro ao carregar o produto para edição.');
        }
    }
});