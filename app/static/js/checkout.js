// Função para atualizar quantidade
function updateQuantity(itemId, change) {
    const quantityElement = document.querySelectorAll('.quantity')[itemId - 1];
    let currentQuantity = parseInt(quantityElement.textContent);
    const newQuantity = Math.max(1, currentQuantity + change);
    quantityElement.textContent = newQuantity;
    calculateTotals();
}

// Função para calcular totais
function calculateTotals() {
    const items = document.querySelectorAll('.cart-item');
    let subtotal = 0;

    items.forEach((item) => {
        const price = parseFloat(item.querySelector('.item-price span').textContent.replace('R$ ', '').replace(',', '.'));
        const quantity = parseInt(item.querySelector('.quantity').textContent);
        subtotal += price * quantity;
    });

    const frete = 29.90;
    const total = subtotal + frete;

    document.getElementById('subtotal').textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    document.getElementById('total').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
}

// Função para finalizar pedido
function finalizarPedido() {
    alert('Pedido finalizado com sucesso!');
}

// Máscara para campos
function aplicarMascara(inputId, pattern) {
    const input = document.getElementById(inputId);
    if (input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            e.target.value = pattern(value);
        });
    }
}

function BuscarCEP() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert('CEP não encontrado');
                } else {
                    document.getElementById('rua').value = data.logradouro;
                    document.getElementById('bairro').value = data.bairro;
                    document.getElementById('cidade').value = data.localidade;
                    document.getElementById('estado').value = data.uf;
                }
            })
            .catch(error => {
                console.error('Erro ao buscar CEP:', error);
            });
    }
}

// Aplicar máscaras
const mascaras = {
    cpf: value => value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4'),
    telefone: value => value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3'),
    cep: value => value.replace(/(\d{5})(\d{3})/, '$1-$2')
};

Object.entries(mascaras).forEach(([id, pattern]) => aplicarMascara(id, pattern));

// Função para carregar itens do carrinho
function loadCartItems() {
  // Esta função será implementada para buscar os itens do carrinho do backend
  // Por enquanto, vamos apenas garantir que os totais sejam calculados
  calculateTotals();
  
  // Aqui você pode adicionar uma chamada para buscar os itens do carrinho
  // Exemplo:
  // fetch('/api/carrinho')
  //   .then(response => response.json())
  //   .then(items => renderCartItems(items))
  //   .catch(error => console.error('Erro ao carregar itens:', error));
}

// Função para renderizar os itens do carrinho
function renderCartItems(items) {
  const container = document.getElementById('cart-items-container');
  const emptyMessage = container.querySelector('.empty-cart-message');
  
  if (!items || items.length === 0) {
    emptyMessage.style.display = 'block';
    return;
  }
  
  emptyMessage.style.display = 'none';
  container.innerHTML = ''; // Limpa os itens atuais
  
  items.forEach((item, index) => {
    const itemElement = document.createElement('div');
    itemElement.className = 'cart-item';
    itemElement.innerHTML = `
      <img src="${item.imagem}" alt="${item.nome}">
      <div class="item-details">
        <h4>${item.nome}</h4>
        ${item.tamanho ? `<p>Tamanho: ${item.tamanho}</p>` : ''}
        ${item.cor ? `<p>Cor: ${item.cor}</p>` : ''}
        <div class="quantity-controls">
          <button class="qty-btn" onclick="updateQuantity(${index}, -1)">-</button>
          <span class="quantity">${item.quantidade || 1}</span>
          <button class="qty-btn" onclick="updateQuantity(${index}, 1)">+</button>
        </div>
      </div>
      <div class="item-price">
        <span>R$ ${item.preco?.toFixed(2).replace('.', ',') || '0,00'}</span>
      </div>
    `;
    container.appendChild(itemElement);
  });
  
  // Atualiza os totais após renderizar os itens
  calculateTotals();
}

// Inicializar a página
window.addEventListener('DOMContentLoaded', () => {
  loadCartItems();
  calculateTotals();
});