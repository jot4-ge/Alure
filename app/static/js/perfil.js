/*
 * Este arquivo contém a lógica para interatividade na página de perfil,
 * como logout, exclusão de conta e edição de perfil.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Seletores dos botões e elementos
    const logoutBtn = document.getElementById('logoutBtn');
    const deleteAccountBtn = document.getElementById('deleteAccountBtn');

    // Lógica para o botão de Logout
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/users/logout', { method: 'POST' });

                if (response.ok) {
                    alert('Você foi desconectado com sucesso.');
                    window.location.href = '/login'; // Redireciona para a página de login
                } else {
                    const errorData = await response.json();
                    alert(`Falha ao fazer logout: ${errorData.error || 'Erro desconhecido'}`);
                }
            } catch (error) {
                console.error('Erro de rede ao tentar fazer logout:', error);
                alert('Ocorreu um erro de rede. Tente novamente.');
            }
        });
    }

    // Lógica para o botão de Deletar Conta
    if (deleteAccountBtn) {
        const profileSection = document.querySelector('.profile-section');
        const userId = profileSection ? profileSection.dataset.userId : null;

        if (userId) {
            deleteAccountBtn.addEventListener('click', async () => {
                if (confirm('Tem certeza de que deseja deletar sua conta? Esta ação é irreversível.')) {
                    try {
                        const response = await fetch(`/api/users/${userId}`, { method: 'DELETE' });

                        if (response.ok) {
                            alert('Sua conta foi deletada com sucesso.');
                            window.location.href = '/initial_page'; // Redireciona para a página inicial
                        } else {
                            const errorData = await response.json();
                            alert(`Falha ao deletar a conta: ${errorData.error || 'Erro desconhecido'}`);
                        }
                    } catch (error) {
                        console.error('Erro de rede ao tentar deletar a conta:', error);
                        alert('Ocorreu um erro de rede. Tente novamente.');
                    }
                }
            });
        } else {
            // Se não encontrarmos o ID do usuário, desabilitamos o botão para evitar erros.
            deleteAccountBtn.disabled = true;
            deleteAccountBtn.title = "Não foi possível identificar o usuário para deletar.";
            console.warn('User ID não encontrado no atributo data-user-id. O botão de deletar foi desabilitado.');
        }
    }
});