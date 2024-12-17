var io: any;

namespace SocketChat {
    const game_id = document.getElementById("game_id").innerText;

    // maining the socket connection in this namespace
    export let socket = io.connect(`/forum/${game_id}`);
    socket.id = game_id;

    // define interfaces matching the message formats used on socket events
    export interface OutStatus {
        text: string;
    }
    export interface Status extends OutStatus {
        user: string;
        type: string;
    }
    export interface OutMessage {
        text: string;
    }
    export interface Message extends OutMessage {
        user: string;
        timestamp: string;
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    //const forumLink = <HTMLAnchorElement> document.getElementById("forum-link");

    // attach standard event listeners to the socket
    SocketChat.socket.on("connect", joinRoom);
    SocketChat.socket.on("disconnect", leaveRoom);
    // attach custom event listeners to this socket based on planned protocol
    SocketChat.socket.on("receive-message", receiveMessage);

    // attach event listeners to input elements to send messages
    const msgField = document.getElementById("post-field");
    msgField.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

function joinRoom() {
    // log the successful connection and the socket's id
    console.log(`Connected: Socket ${SocketChat.socket.id}`);
}

function leaveRoom() {
    // log the successful disconnection and the socket's id
    console.log(`Disconnected: Socket ${SocketChat.socket.id}`);
}

function sendMessage() {
    // get the text of the message to be sent from the message field
    const msgField = <HTMLInputElement> document.getElementById('message-field')
    const msgText = msgField.value;
    // if the message is all whitespace, do nothing
    if (msgText.trim().length === 0) { return; }
    // prepare a message object with this text
    const msg: SocketChat.OutMessage = {'text': msgText};
    // create a new send-message event on the server with this message
    SocketChat.socket.emit("send-message", msg);
    // delete the text in the message field to show the message was sent
    msgField.value = "";
}

function receiveMessage(msg: SocketChat.Message) {
    // get a reference to the chat window and add a paragraph element
    const forum = document.getElementById("forum");
    const messageRow = document.createElement("tr");

    const usernameCell = messageRow.insertCell();
    usernameCell.innerText = msg.user;

    const messageCell = messageRow.insertCell();
    messageCell.innerText = msg.text;

    const timestampCell = messageRow.insertCell();
    timestampCell.innerText = msg.timestamp;

    forum.appendChild(messageRow);

    // scroll the chat window to ensure the new message is displayed
    forum.scrollTop = forum.scrollHeight;
}