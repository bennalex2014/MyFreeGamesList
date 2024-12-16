namespace FreeToGameAPI {
    export const baseURL: string = `https://www.freetogame.com/api/games`;
    
    // define interfaces to match the API
    export interface Game {
        id: number;
        title: string;
        thumbnail: string;
        short_description: string;
        game_url: string;
        genre: string;
        platform: string;
        publisher: string;
        developer: string;
        release_date: string;
        freetogame_profile_url: string;
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    loadGames();
});

async function loadGames() {   
    // fetch all games and pass them to appendComment in order
    const response = await fetch(FreeToGameAPI.baseURL);
    const gameIndex = <Array<FreeToGameAPI.Game>> await validateJSON(response);

    // get the table body
    const gameTable = <HTMLTableElement> document.getElementById("game-table-body");

    for (const game of gameIndex) {
        const row = gameTable.insertRow();
        fillRow(game, row);
    }
}

async function fillRow(game: FreeToGameAPI.Game, row: HTMLTableRowElement) {
    const nameCell = row.insertCell();
    const gameLink = document.createElement("a");
    gameLink.href = `/game/${game.id}`;
    gameLink.innerText = game.title;
    nameCell.appendChild(gameLink);

    const thumbnailCell = row.insertCell();
    const thumbnailLink = document.createElement("img")
    thumbnailLink.src = `static/thumbnails/${game.id}.jpg`;
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

async function validateJSON(response: Response): Promise<any> {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}