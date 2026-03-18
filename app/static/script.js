// Função para buscar um Pokémon específico
async function buscarPokemon() {
  // Pega o valor digitado no input e remove espaços
  const input = document.getElementById("pokemonInput").value.trim();

  // Seleciona o card onde os dados serão exibidos
  const card = document.getElementById("pokemonCard");

  // Validação: se não digitou nada
  if (!input) {
    alert("Digite o nome de um Pokémon");
    return; // para a execução
  }

  try {
    // Faz requisição para a API (backend)
    const response = await fetch(`/api/pokemon/${input}`);

    // Converte resposta para JSON
    const data = await response.json();

    // Se a resposta não for OK (erro da API)
    if (!response.ok) {
      card.classList.remove("hidden"); // mostra o card
      card.innerHTML = `<p>${data.error}</p>`; // exibe erro
      return;
    }

    // Exibe o card com os dados do Pokémon
    card.classList.remove("hidden");

    // Monta HTML dinamicamente com os dados recebidos
    card.innerHTML = `
      <h3>${data.name}</h3>
      <img src="${data.image}" alt="${data.name}">
      <p><strong>Tipos:</strong> ${data.types.join(", ")}</p>
      <p><strong>Altura:</strong> ${data.height}</p>
      <p><strong>Peso:</strong> ${data.weight}</p>
    `;
  } catch (error) {
    // Caso dê erro na requisição (ex: servidor fora)
    card.classList.remove("hidden");
    card.innerHTML = `<p>Erro ao buscar Pokémon.</p>`;
  }
}

// Função para carregar lista de Pokémons
async function carregarPokemons() {
  // Seleciona a lista onde os pokémons serão exibidos
  const list = document.getElementById("pokemonList");

  try {
    // Faz requisição para buscar todos os pokémons
    const response = await fetch("/api/pokemons");

    // Converte para JSON
    const data = await response.json();

    // Limpa a lista antes de preencher
    list.innerHTML = "";

    // Percorre cada Pokémon retornado
    data.forEach((pokemon) => {
      // Cria uma div para cada item
      const div = document.createElement("div");

      // Adiciona classe CSS
      div.className = "pokemon-item";

      // Coloca o nome do Pokémon
      div.innerHTML = pokemon.name;

      // Adiciona na lista
      list.appendChild(div);
    });
  } catch (error) {
    // Caso ocorra erro
    list.innerHTML = "<p>Erro ao carregar Pokémons.</p>";
  }
}

// Chama a função automaticamente ao carregar a página
carregarPokemons();
