// Função para buscar um Pokémon específico
async function buscarPokemon(nomePokemon = null) {
  // Se vier um nome pelo botão, usa ele. Senão, pega do input
  const input =
    nomePokemon || document.getElementById("pokemonInput").value.trim();

  // Seleciona o card onde os dados serão exibidos
  const card = document.getElementById("pokemonCard");

  // Validação: se não digitou nada
  if (!input) {
    alert("Digite o nome de um Pokémon");
    return;
  }

  try {
    // Faz requisição para a API (backend)
    const response = await fetch(`/api/pokemon/${input}`);
    console.log("fetch response:", response);

    // Converte resposta para JSON
    const data = await response.json();

    console.log("API response ok:", response.ok, "data:", data);

    // Se a resposta não for OK (erro da API)
    if (!response.ok) {
      card.classList.remove("hidden");
      card.innerHTML = `<p>${data.error}</p>`;
      return;
    }

    // Exibe o card com os dados do Pokémon
    card.classList.remove("hidden");

    // Monta HTML dinamicamente com os dados recebidos
    card.innerHTML = `
      <h3>${data.name}</h3>
      <img src="${data.image}" alt="${data.name}" style="width: 120px; display: block; margin: 10px auto;">
      <p><strong>Tipo:</strong> ${data.types ? data.types.join(", ") : "Desconhecido"}</p>
      <p><strong>Altura:</strong> ${data.height}</p>
      <p><strong>Peso:</strong> ${data.weight}</p>
    `;

    console.log("Pokémon exibido:", data);
  } catch (error) {
    alert(error.message);
    console.error("Erro na requisição:", error);

    card.classList.remove("hidden");
    card.innerHTML = `<p>Erro ao buscar Pokémon.</p>`;
  }
}
