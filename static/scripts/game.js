var FTG_API;
(function (FTG_API) {
    FTG_API.baseURL = `https://www.freetogame.com/api/`;
})(FTG_API || (FTG_API = {}));
document.addEventListener("DOMContentLoaded", async () => {
    loadGame();
});
async function loadGame() {
    const gameIDField = document.getElementById("gameID");
    const gameID = gameIDField.value;
    const response = await fetch(`${FTG_API.baseURL}game?id=${gameID}`);
    const game = await vJSON(response);
    const thumbnailIMG = document.getElementById("gameIMG");
    thumbnailIMG.src = game.thumbnail;
}
async function vJSON(response) {
    if (response.ok) {
        return response.json();
    }
    else {
        return Promise.reject(response);
    }
}
