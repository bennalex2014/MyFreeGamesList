var FreeToGameAPI;
(function (FreeToGameAPI) {
    FreeToGameAPI.baseURL = `https://www.freetogame.com/api/games`;
})(FreeToGameAPI || (FreeToGameAPI = {}));
document.addEventListener("DOMContentLoaded", async () => {
    loadGames();
});
async function loadGames() {
    const response = await fetch(FreeToGameAPI.baseURL);
    const gameIndex = await validateJSON(response);
    const gameTable = document.getElementById("game-table-body");
    for (const game of gameIndex) {
        const row = document.createElement("tr");
        gameTable.appendChild(row);
        fillRow(game, row);
    }
}
async function fillRow(game, row) {
    const nameCell = row.insertCell();
    const gameLink = document.createElement("a");
    gameLink.href = `/game/${game.id}`;
    gameLink.innerText = game.title;
    nameCell.appendChild(gameLink);
    const thumbnailCell = row.insertCell();
    const thumbnailLink = document.createElement("img");
    thumbnailLink.src = game.thumbnail;
    thumbnailLink.alt = game.title;
    thumbnailLink.width = 100;
    thumbnailCell.appendChild(thumbnailLink);
    const descriptionCell = row.insertCell();
    descriptionCell.innerText = game.short_description;
    const genreCell = row.insertCell();
    genreCell.innerText = game.genre;
    const platformCell = row.insertCell();
    platformCell.innerText = game.platform;
    const publisherCell = row.insertCell();
    publisherCell.innerText = game.publisher;
    const developerCell = row.insertCell();
    developerCell.innerText = game.developer;
    const releaseDateCell = row.insertCell();
    releaseDateCell.innerText = game.release_date;
}
async function validateJSON(response) {
    if (response.ok) {
        return response.json();
    }
    else {
        return Promise.reject(response);
    }
}
