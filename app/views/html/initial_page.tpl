<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alure - Streetwear</title>

  <style>
    :root {
      --roxo: #6A1B9A;
      --preto: #000000;
      --cinza: #f5f5f5;
      --cinza-claro: #cccccc;
      --branco: #ffffff;
    }

    html, body {
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--preto);
      color: var(--branco);
    }

    header {
      background-color: var(--preto);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--roxo);
    }

    .logo img {
      height: 50px;
    }

    nav ul {
      list-style: none;
      display: flex;
      gap: 2rem;
      margin: 0;
      padding: 0;
    }

    nav a {
      text-decoration: none;
      color: var(--branco);
      font-weight: bold;
      transition: color 0.2s;
    }

    nav a:hover {
      color: var(--roxo);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .header-actions input[type="search"] {
      border: none;
      border-radius: 20px;
      padding: 0.5rem 1rem;
      background-color: var(--cinza-claro);
      color: var(--preto);
    }

    .header-actions a {
      font-size: 1.5rem;
      color: var(--branco);
    }

    main {
      padding: 3rem 2rem;
    }

    h2 {
      font-size: 2rem;
      text-align: center;
      color: var(--roxo);
      margin-bottom: 2rem;
    }

    .category-grid, .product-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .category-item, .product-card {
      background-color: #1a1a1a;
      border: 1px solid var(--roxo);
      border-radius: 10px;
      overflow: hidden;
      text-align: center;
      transition: transform 0.3s ease;
    }

    .category-item:hover, .product-card:hover {
      transform: scale(1.02);
    }

    .category-item img, .product-card img {
      width: 100%;
      height: auto;
    }

    .category-item h3, .product-card h3 {
      padding: 1rem;
      margin: 0;
      color: var(--branco);
    }

    .price {
      font-size: 1.2rem;
      font-weight: bold;
      color: var(--roxo);
      margin-bottom: 1rem;
    }

    .product-card button {
      background-color: var(--roxo);
      color: var(--branco);
      border: none;
      padding: 0.7rem 1.5rem;
      margin-bottom: 1rem;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    .product-card button:hover {
      background-color: #8e24aa;
    }

    footer {
      background-color: #111;
      color: var(--cinza-claro);
      padding: 3rem 2rem;
    }

    .footer-columns {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .footer-columns h3 {
      color: var(--roxo);
    }

    .footer-columns a {
      color: var(--cinza-claro);
      text-decoration: none;
      transition: color 0.3s;
    }

    .footer-columns a:hover {
      color: var(--roxo);
    }

    .newsletter-form input {
      width: 100%;
      padding: 0.5rem;
      border: none;
      border-radius: 3px;
      margin-bottom: 0.5rem;
    }

    .newsletter-form button {
      width: 100%;
      padding: 0.5rem;
      background-color: var(--roxo);
      color: var(--branco);
      border: none;
      border-radius: 3px;
      cursor: pointer;
    }

    .footer-bottom {
      text-align: center;
      margin-top: 2rem;
      padding-top: 1rem;
      border-top: 1px solid #333;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>

  <header>
    <a href="/" class="logo">
      <img src="/static/images/logo.jpg" alt="Logo da Alure">
    </a>

    <nav>
      <ul>
        <li><a href="#">Novidades</a></li>
        <li><a href="#">Feminino</a></li>
        <li><a href="#">Masculino</a></li>
        <li><a href="#">Drops</a></li>
      </ul>
    </nav>

    <div class="header-actions">
      <form action="#" method="get">
        <input type="search" name="q" placeholder="Buscar">
      </form>
      <a href="#">👤</a>
      <a href="#">🛒</a>
    </div>
  </header>

  <main>
    <section class="category-section">
      <h2>Categorias</h2>
      <div class="category-grid">
        <a href="#" class="category-item">
          <img src="https://via.placeholder.com/400x400.png/1a1a1a/ffffff?text=Streetwear" alt="Streetwear">
          <h3>Streetwear</h3>
        </a>
        <a href="#" class="category-item">
          <img src="https://via.placeholder.com/400x400.png/1a1a1a/ffffff?text=Camisetas" alt="Camisetas">
          <h3>Camisetas</h3>
        </a>
        <a href="#" class="category-item">
          <img src="https://via.placeholder.com/400x400.png/1a1a1a/ffffff?text=Acessórios" alt="Acessórios">
          <h3>Acessórios</h3>
        </a>
      </div>
    </section>

    <section class="featured-products-section">
      <h2>Lançamentos</h2>
      <div class="product-grid">
        <div class="product-card">
          <a href="#">
            <img src="https://via.placeholder.com/400x500.png/1a1a1a/ffffff?text=Produto+1" alt="Produto 1">
            <h3>Jaqueta Oversized</h3>
            <p class="price">R$ 399,90</p>
          </a>
          <button>Adicionar</button>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="footer-columns">
      <div class="column">
        <h3>Sobre</h3>
        <ul>
          <li><a href="#">A Alure</a></li>
          <li><a href="#">Política de Privacidade</a></li>
          <li><a href="#">Trocas e Devoluções</a></li>
        </ul>
      </div>
      <div class="column">
        <h3>Contato</h3>
        <p>Email: contato@alure.com</p>
        <p>WhatsApp: (11) 99999-9999</p>
      </div>
      <div class="column">
        <h3>Redes</h3>
        <a href="#">Instagram</a><br>
        <a href="#">TikTok</a><br>
        <a href="#">YouTube</a>
      </div>
      <div class="column">
        <h3>Receba Novidades</h3>
        <form class="newsletter-form">
          <input type="email" placeholder="Seu e-mail">
          <button type="submit">Cadastrar</button>
        </form>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025 Alure. Todos os direitos reservados.</p>
    </div>
  </footer>

</body>
</html>
