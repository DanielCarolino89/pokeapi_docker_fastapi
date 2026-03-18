async function buscarPokemon() {
  const input = document.getElementById("pokemonInput").value.trim();
  const card = document.getElementById("pokemonCard");

  if (!input) {
    alert("Digite o nome de um Pokémon");
    return;
  }

  try {
    const response = await fetch(`/api/pokemon/${input}`);
    const data = await response.json();

    if (!response.ok) {
      card.classList.remove("hidden");
      card.innerHTML = `<p>${data.error}</p>`;
      return;
    }

    card.classList.remove("hidden");
    card.innerHTML = `
      <h3>${data.name}</h3>
      <img src="${data.image}" alt="${data.name}">
      <p><strong>Tipos:</strong> ${data.types.join(", ")}</p>
      <p><strong>Altura:</strong> ${data.height}</p>
      <p><strong>Peso:</strong> ${data.weight}</p>
    `;
  } catch (error) {
    card.classList.remove("hidden");
    card.innerHTML = `<p>Erro ao buscar Pokémon.</p>`;
  }
}

async function carregarPokemons() {
  const list = document.getElementById("pokemonList");

  try {
    const response = await fetch("/api/pokemons");
    const data = await response.json();

    list.innerHTML = "";

    data.forEach((pokemon) => {
      const div = document.createElement("div");
      div.className = "pokemon-item";
      div.innerHTML = pokemon.name;
      list.appendChild(div);
    });
  } catch (error) {
    list.innerHTML = "<p>Erro ao carregar Pokémons.</p>";
  }
}

carregarPokemons();
