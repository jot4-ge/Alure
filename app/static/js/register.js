document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById("registerForm");
  const submitButton = form.querySelector('button[type="submit"]');
  const messageDiv = document.getElementById('form-message');

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Desabilitar o botão e mostrar estado de carregamento
    submitButton.disabled = true;
    submitButton.textContent = 'Registrando...';
    messageDiv.hidden = true;

    const data = {
      username: this.username.value,
      email: this.email.value,
      password: this.password.value,
      telephone_num: this.telephone.value
    };

    try {
      const res = await fetch("/api/users/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (res.ok) {
        messageDiv.textContent = 'Registro bem-sucedido! Redirecionando...';
        messageDiv.className = 'form-message success';
        messageDiv.hidden = false;
        setTimeout(() => {
          window.location.href = "/perfil"; // Redireciona após o usuário ver a mensagem
        }, 2000);
      } else {
        messageDiv.textContent = result.error || "Ocorreu um erro ao registrar.";
        messageDiv.className = 'form-message error';
        messageDiv.hidden = false;
        submitButton.disabled = false;
        submitButton.textContent = 'Registrar';
      }
    } catch (error) {
      messageDiv.textContent = 'Falha na comunicação com o servidor. Tente novamente.';
      messageDiv.className = 'form-message error';
      messageDiv.hidden = false;
      submitButton.disabled = false;
      submitButton.textContent = 'Registrar';
    }
  });
});
