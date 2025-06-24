function calculateFrete(CEP) {
    // Verifica se o CEP tem pelo menos 8 dígitos
    if (!CEP || CEP.toString().replace(/\D/g, '').length < 8) {
        alert('Por favor, digite um CEP válido com 8 dígitos.');
        return 0;
    }

    const firstDigit = CEP.charAt(0);
    
    const regions = {
        '0': 'SP/MG',
        '1': 'DF/GO/MT/MS',
        '2': 'RJ/ES',
        '3': 'MG',
        '4': 'BA/SE',
        '5': 'PE/AL/PB/RN',
        '6': 'CE/PI/MA',
        '7': 'DF/GO/MT/MS',
        '8': 'PR/SC',
        '9': 'RS'
    };

    const shippingRates = {
        'SP/MG': 15.90,
        'RJ/ES': 20.90,
        'DF/GO/MT/MS': 25.90,
        'DEFAULT': 29.90
    };
    
    const region = regions[firstDigit] || 'DEFAULT';
    const shippingRate = shippingRates[region];

    // Atualiza o valor do frete na interface
    const freteElement = document.getElementById('frete');
    if (freteElement) {
        freteElement.textContent = `R$ ${shippingRate.toFixed(2).replace('.', ',')}`;
    }
    
    // Recalcula os totais
    calculateTotals();
    
    return shippingRate;
}

function calculateTotals() {
    const items = document.querySelectorAll('.cart-item');
    let subtotal = 0;

    items.forEach((item) => {
        const priceElement = item.querySelector('.item-price span');
        const quantityElement = item.querySelector('.quantity');
        
        if (priceElement && quantityElement) {
            const price = parseFloat(priceElement.textContent.replace('R$ ', '').replace(',', '.'));
            const quantity = parseInt(quantityElement.textContent);
            subtotal += price * quantity;
        }
    });

    // Obtém o elemento do frete
    const freteElement = document.getElementById('frete');
    let frete = 0;
    
    // Verifica se o frete já foi calculado
    if (freteElement && freteElement.textContent.trim() !== '') {
        // Se o subtotal for maior ou igual a 200, frete grátis
        if (subtotal >= 200) {
            frete = 0;
            freteElement.textContent = 'Grátis';
        } else {
            frete = parseFloat(freteElement.textContent.replace('R$ ', '').replace('.', '').replace(',', '.')) || 0;
        }
    }
    
    const total = subtotal + frete;
    
    // Atualiza os totais na interface
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    
    if (subtotalElement) {
        subtotalElement.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    }
    
    if (totalElement) {
        totalElement.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    }
}

function aplicarMascara(inputId, pattern) {
    const input = document.getElementById(inputId);
    if (input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            e.target.value = pattern(value);
        });
    }
}

const mascaras = {
    cep: value => {
        value = value.replace(/\D/g, '');
        if (value.length > 5) {
            return value.replace(/^(\d{5})(\d{0,3}).*/, '$1-$2');
        }
        return value;
    }
};

// Inicializar máscara de CEP quando o DOM estiver carregado
function finalizarCompra() {
    // Verifica se há itens no carrinho
    //const cartItems = document.querySelectorAll('.cart-item');
    //if (cartItems.length === 0) {
        //alert('Seu carrinho está vazio. Adicione itens antes de finalizar a compra.');
        //return;
    //}

    // Redireciona para a página de checkout
    window.location.href = '/checkout';
}

// Adiciona o event listener para o botão de finalizar compra
document.addEventListener('DOMContentLoaded', function() {
    aplicarMascara('cep', mascaras.cep);
    
    const finalizarBtn = document.getElementById('finalizar-compra-btn');
    if (finalizarBtn) {
        finalizarBtn.addEventListener('click', finalizarCompra);
    }
});