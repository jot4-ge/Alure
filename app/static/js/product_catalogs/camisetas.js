document.addEventListener('DOMContentLoaded', () => {
  const productContainer = document.getElementById('product-container');
  const cartCountElement = document.getElementById('cartCount');
  const categoria = "camisetas";

  // --- LÓGICA WEBSOCKET ---
  function connectWebSocket() {
    const socket = new WebSocket(`ws://${window.location.hostname}:8765`);

    socket.onopen = () => console.log('Conectado ao serviço de atualização
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'stock_update') {
        const { product_id, estoque } = data.payload;
        console.log(`Atualização recebida: Produto ${product_id} agora tem estoque ${estoque}.`);
        const productCard = document.querySelector(`.product-card[data-product-id="${product_id}"]`);
        if (productCard) {
          const stockElement = productCard.querySelector('.product-stock-value');
          if (stockElement) {
            stockElement.textContent = estoque;
          }
        }
      }
    };
    socket.onclose = () => {
      console.log('Conexão de tempo real perdida. Tentando reconectar em 5s...');
      setTimeout(connectWebSocket, 5000);
    };
  }

  function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  }

  async function addToCart(productId, productName) {
    try {
      // 1. Faz a requisição POST para a API do carrinho.
      const response = await fetch('/api/cart/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // 2. Envia o ID do produto e a quantidade desejada.
        body: JSON.stringify({
          product_id: productId,
          quantity: 1
        }),
      });

      const result = await response.json();

      // 3. Trata a resposta da API.
      if (!response.ok) {
        if (response.status === 401) {
          alert('Você precisa fazer o login para adicionar itens ao carrinho.');
          window.location.href = '/login';
        } else {
          alert(`Erro: ${result.error || 'Não foi possível adicionar o item.'}`);
        }
        return;
      }

      // 4. Se a operação foi um sucesso, atualiza o contador do carrinho na tela.
      if (cartCountElement && result.new_cart_count !== undefined) {
        cartCountElement.textContent = result.new_cart_count;
        cartCountElement.style.display = result.new_cart_count > 0 ? 'flex' : 'none';
      }

      // Exibe uma mensagem de sucesso para o usuário.
      alert(`${productName} foi adicionado ao carrinho!`);

    } catch (error) {
      console.error('Falha na requisição para adicionar ao carrinho:', error);
      alert('Ocorreu um erro de conexão. Tente novamente.');
    }
  }

  /**
   * Busca o carrinho na API e atualiza o contador de itens no header da página.
   */
  async function updateCartCount() {
    try {
      // A API /api/cart retorna a lista de itens: [{product_id, quantity}, ...]
      const response = await fetch('/api/cart');
      if (!response.ok) return;

      const cartItems = await response.json();

      // Soma a quantidade de todos os itens para obter o total.
      const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);

      if (cartCountElement) {
        cartCountElement.textContent = totalItems;
        cartCountElement.style.display = totalItems > 0 ? 'flex' : 'none';
      }
    } catch (error) {
      console.error("Falha ao buscar contagem do carrinho:", error);
    }
  }

  /**
   * Carrega os produtos da categoria específica e os renderiza na página.
   */
  async function loadProducts() {
    if (!productContainer) {
        console.error("Elemento com id 'product-container' não encontrado.");
        return;
    }
    try {
      // A rota da API de produtos foi corrigida para usar /category/
      const response = await fetch(`/api/products/category/${categoria}`);
      if (!response.ok) throw new Error(`Erro na rede: ${response.statusText}`);

      const products = await response.json();
      productContainer.innerHTML = '';

      if (!products || products.length === 0) {
        productContainer.innerHTML = '<p>Nenhuma camiseta encontrada no momento.</p>';
        return;
      }

      products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.setAttribute('data-product-id', product.id);

        card.innerHTML = `
          <img src="/static/img/clothes/${product.image_filename}" alt="${product.nome}">
          <div>
            <h3 class="product-name">${product.nome}</h3>
            <p class="product-size">Tamanho: ${product.tamanho}</p>
            <p class="product-stock">Estoque: <span class="product-stock-value">${product.estoque}</span></p>
            <p class="product-price">${formatCurrency(product.preco)}</p>
          </div>
          <button class="add-to-cart-btn">Adicionar ao Carrinho</button>
        `;

        // Adiciona o evento de clique que chama a nossa função de API.
        card.querySelector('.add-to-cart-btn').addEventListener('click', () => {
            addToCart(product.id, product.nome);
        });

        productContainer.appendChild(card);
      });

    } catch (error) {
      console.error('Falha ao carregar produtos:', error);
      productContainer.innerHTML = `<p class="error-message">Falha ao carregar produtos.</p>`;
    }
  }

  // Funções a serem executadas quando a página carregar
  loadProducts();
  updateCartCount();
  connectWebSocket();
});