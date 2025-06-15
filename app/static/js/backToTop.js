document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('backToTop');

    // Esconde o botão ou mostra com base na posição da pagina
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 150) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });

    // Scrolla de maneira suave para o topo da pagina
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});
