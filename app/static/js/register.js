document.getElementById("registerForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const data = {
    name: this.name.value,
    email: this.email.value,
    password: this.password.value
  };

  const res = await fetch("/api/users/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  if (res.ok) {
    window.location.href = "/perfil";
  } else {
    alert(result.error || "Erro ao registrar.");
  }
});
