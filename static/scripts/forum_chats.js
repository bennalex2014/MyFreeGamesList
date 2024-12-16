var io;
var SocketChat;
(function (SocketChat) {
    SocketChat.socket = io.connect("/forum/");
})(SocketChat || (SocketChat = {}));
document.addEventListener("DOMContentLoaded", async () => {
    const forumLink = document.getElementById("forum-link");
    SocketChat.socket = io.connect(forumLink.href);
    SocketChat.socket.on("connect", joinRoom);
    SocketChat.socket.on("disconnect", leaveRoom);
    SocketChat.socket.on("receive-message", receiveMessage);
    const msgField = document.getElementById("post-field");
    msgField.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
function joinRoom() {
    console.log(`Connected: Socket ${SocketChat.socket.id}`);
}
function leaveRoom() {
    console.log(`Disconnected: Socket ${SocketChat.socket.id}`);
}
function sendMessage() {
    const msgField = document.getElementById('message-field');
    const msgText = msgField.value;
    if (msgText.trim().length === 0) {
        return;
    }
    const msg = { 'text': msgText };
    SocketChat.socket.emit("send-message", msg);
    msgField.value = "";
}
function receiveMessage(msg) {
    const forum = document.getElementById("forum");
    const messageRow = document.createElement("tr");
    const usernameCell = messageRow.insertCell();
    usernameCell.innerText = msg.user;
    const messageCell = messageRow.insertCell();
    messageCell.innerText = msg.text;
    const timestampCell = messageRow.insertCell();
    timestampCell.innerText = msg.timestamp;
    forum.appendChild(messageRow);
    forum.scrollTop = forum.scrollHeight;
}
