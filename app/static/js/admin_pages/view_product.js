

document.addEventListener('DOMContentLoaded', () => {
    const productListBody = document.getElementById('product-list-body');

    function formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }

    /**
     * Busca os produtos na API e popula a tabela.
     */
    async function loadProducts() {
        productListBody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Carregando produtos...</td></tr>';

        try {
            const response = await fetch('/api/products');
            if (!response.ok) {
                throw new Error(`Erro na rede: ${response.statusText}`);
            }
            const products = await response.json();

            // Limpa a tabela antes de adicionar os novos dados
            productListBody.innerHTML = '';

            if (products.length === 0) {
                productListBody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Nenhum produto encontrado.</td></tr>';
                return;
            }

            products.forEach(product => {
                const row = document.createElement('tr');

                // Constrói as células da tabela dinamicamente, SEM o botão de deletar
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td><img src="/static/img/clothes/${product.image_filename}" alt="${product.nome}"></td>
                    <td>${product.nome}</td>
                    <td>${formatCurrency(product.preco)}</td>
                    <td>${product.estoque}</td>
                    <td>${product.tamanho}</td>
                    <td>${product.categoria}</td>
                `;

                productListBody.appendChild(row);
            });

        } catch (error) {
            console.error('Falha ao carregar produtos:', error);
            productListBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--vermelho-perigo);">Falha ao carregar produtos. Tente novamente mais tarde.</td></tr>`;
        }
    }

    // Carrega os produtos assim que a página é aberta
    loadProducts();
});