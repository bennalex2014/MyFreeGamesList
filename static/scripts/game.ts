namespace FTG_API {
    export const baseURL: string = `https://www.freetogame.com/api/`;
    
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
    loadGame();
});

async function loadGame() {
    const gameIDField = <HTMLInputElement> document.getElementById("gameID");
    const gameID = gameIDField.value;

    // fetch all games and pass them to appendComment in order
    const response = await fetch(`${FTG_API.baseURL}game?id=${gameID}`);
    const game = <FTG_API.Game> await vJSON(response);

    // get the img body
    const thumbnailIMG = <HTMLImageElement> document.getElementById("gameIMG");

    thumbnailIMG.src = game.thumbnail;
}

async function vJSON(response: Response): Promise<any> {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}