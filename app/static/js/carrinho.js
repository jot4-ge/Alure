document.addEventListener('DOMContentLoaded', () => {
  // Elementos do DOM
  const cartItemsContainer = document.getElementById('cartItemsContainer');
  const subtotalValueEl = document.getElementById('subtotalValue');
  const totalValueEl = document.getElementById('totalValue');
  const emptyCartEl = document.getElementById('emptyCart');
  const cartContentEl = document.getElementById('cartContent');
  const cartCountEl = document.getElementById('cartCount');
  const clearCartBtn = document.getElementById('clearCartBtn');
  const checkoutBtn = document.getElementById('checkoutBtn');

  // Estado local para guardar os itens do carrinho com detalhes
  let detailedCartItems = [];

  // Função para formatar valores em BRL
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  };

  // 1. Função principal para carregar o carrinho
  const loadCart = async () => {
    try {
      // Pega o carrinho básico da API de usuários (só IDs e quantidades)
      const cartResponse = await fetch('/api/cart');
      if (!cartResponse.ok) throw new Error('Falha ao buscar o carrinho.');
      const basicCart = await cartResponse.json();

      if (!basicCart || basicCart.length === 0) {
        showEmptyCart();
        return;
      }

      // Busca os detalhes de cada produto em paralelo
      const productPromises = basicCart.map(item =>
        fetch(`/api/products/${item.product_id}`).then(res => res.json())
      );

      const productsDetails = await Promise.all(productPromises);

      // Combina os detalhes dos produtos com as quantidades do carrinho
      detailedCartItems = basicCart.map((item, index) => ({
        ...productsDetails[index], // Detalhes do produto (id, nome, preco, etc.)
        quantity: item.quantity    // Quantidade do carrinho
      }));

      renderCart();
      showCartContent();

    } catch (error) {
      console.error('Erro ao carregar o carrinho:', error);
      showEmptyCart(); // Mostra carrinho vazio em caso de erro
    }
  };

  // 2. Função para renderizar os itens na tela
  const renderCart = () => {
    cartItemsContainer.innerHTML = ''; // Limpa o container

    if (!detailedCartItems || detailedCartItems.length === 0) {
        showEmptyCart();
        return;
    }

    detailedCartItems.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = 'cart-item';
      itemEl.setAttribute('data-product-id', item.id);

      itemEl.innerHTML = `
        <div class="cart-item-image">
          <img src="/static/img/clothes/${item.image_filename}" alt="${item.nome}">
        </div>
        <div class="cart-item-details">
          <h3>${item.nome}</h3>
          <p>Preço: ${formatCurrency(item.preco)}</p>
        </div>
        <div class="cart-item-actions">
          <div class="quantity-control">
            <label for="quantity-${item.id}">Qtd:</label>
            <input type="number" id="quantity-${item.id}" value="${item.quantity}" min="1" max="${item.estoque}" disabled>
          </div>
          <p class="item-total-price">Total: ${formatCurrency(item.preco * item.quantity)}</p>
          <button class="btn-remove-item">Remover</button>
        </div>
      `;
      cartItemsContainer.appendChild(itemEl);
    });

    updateSummary();
    addEventListenersToItems();
  };

  // 3. Função para atualizar o resumo (subtotal, total)
  const updateSummary = () => {
    const subtotal = detailedCartItems.reduce((sum, item) => sum + (item.preco * item.quantity), 0);

    subtotalValueEl.textContent = formatCurrency(subtotal);
    totalValueEl.textContent = formatCurrency(subtotal); // Assumindo frete zero por enquanto

    const totalItems = detailedCartItems.reduce((sum, item) => sum + item.quantity, 0);
    cartCountEl.textContent = totalItems;
    cartCountEl.style.display = totalItems > 0 ? 'flex' : 'none';
  };

  // 4. Adiciona eventos aos botões de remover
  const addEventListenersToItems = () => {
    document.querySelectorAll('.cart-item').forEach(itemEl => {
      const productId = itemEl.dataset.productId;

      // Evento para remover item
      itemEl.querySelector('.btn-remove-item').addEventListener('click', () => {
        removeItemFromCart(productId);
      });
    });
  };

  // 5. Função para remover um item específico
  const removeItemFromCart = async (productId) => {
    try {
      const response = await fetch(`/api/cart/remove/${productId}`, {
        method: 'DELETE'
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || 'Não foi possível remover o item.');
      }

      detailedCartItems = detailedCartItems.filter(item => item.id !== productId);
      renderCart();

    } catch (error) {
      console.error('Erro ao remover item:', error);
      alert(`Erro: ${error.message}`);
    }
  };

  // 6. Função para limpar o carrinho inteiro
  const clearCart = async () => {
    if (!confirm('Tem certeza que deseja remover todos os itens do carrinho?')) {
      return;
    }

    try {
      const response = await fetch('/api/cart/clear', {
        method: 'DELETE'
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || 'Não foi possível limpar o carrinho.');
      }

      detailedCartItems = [];
      showEmptyCart();

    } catch (error) {
      console.error('Erro ao limpar o carrinho:', error);
      alert(`Erro: ${error.message}`);
    }
  };

  // 7.Função para confirmar a compra
  const confirmPurchase = async () => {
    // Prepara os dados para enviar à API
    const purchaseData = {
      cart: detailedCartItems.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      }))
    };

    try {
      const response = await fetch('/api/products/purchase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(purchaseData)
      });

      const result = await response.json();

      if (!response.ok && response.status !== 207) { // 207 é um sucesso parcial
        throw new Error(result.error || 'Ocorreu um erro ao processar sua compra.');
      }

      // Exibe a mensagem de sucesso (ou sucesso parcial)
      let successMessage = result.message;
      if (result.erros && result.erros.length > 0) {
        successMessage += "\nAlguns itens não puderam ser comprados por falta de estoque.";
      }
      alert(successMessage);

      // Limpa o carrinho no backend
      await fetch('/api/cart/clear', { method: 'DELETE' });

      // Redireciona o usuário para a página inicial após a compra
      window.location.href = '/initial_page';

    } catch (error) {
      console.error('Erro ao confirmar a compra:', error);
      alert(`Erro: ${error.message}`);
    }
  };

  // Funções para controlar a visibilidade
  const showEmptyCart = () => {
    emptyCartEl.style.display = 'block';
    cartContentEl.style.display = 'none';
    cartCountEl.textContent = 0;
    cartCountEl.style.display = 'none';
  };

  const showCartContent = () => {
    emptyCartEl.style.display = 'none';
    cartContentEl.style.display = 'flex';
  };

  // Evento para limpar o carrinho
  clearCartBtn.addEventListener('click', clearCart);

  // Evento para finalizar a compra (agora chama a nova função)
  checkoutBtn.addEventListener('click', confirmPurchase); // <-- ALTERAÇÃO AQUI

  // Inicia o processo ao carregar a página
  loadCart();
});