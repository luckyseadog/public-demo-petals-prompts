import { createMessageGroupReceived, createMessageGroupSent} from "./drawMessages.mjs";


const sendMessageButton = document.getElementById("sendMessageButton");
const chatArea = document.getElementById("chat-area");
var chatFields = document.getElementsByClassName("chat-element-link");
var chatIdParam = "0";
var ws = null;

Array.from(chatFields).forEach(function (chatField) {
    
    chatField.addEventListener("click", function() {
        const chatId= chatField.getAttribute("chat_id")
        var queryParams = new URLSearchParams(window.location.search);
        queryParams.set("chat_id", chatId);
        history.replaceState(null, null, "?"+queryParams.toString());
    });
});


function openSession() {
    ws = new WebSocket("ws://localhost:8125/chat/api/add-message-websocket");
    console.log("NEW CONNECT");
    ws.onopen = () => {
        sendReplica();
    }
}

function sendReplica() {
    if (ws === null) {
        openSession();
        return;
        
    }
    const chatIdParamInt = parseInt(chatIdParam, 10);

    const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value;
    let inputs = {"chat_id": chatIdParamInt, "content": messageText}
    console.log(inputs)
    receiveReplica(inputs);
}
function receiveReplica(inputs) {
    ws.send(JSON.stringify(inputs));
    let createMessage = false;
    let message = null;
    ws.onmessage = event => {
        if (!createMessage) {
            console.log(event); // how event looks like??????
            message = createMessageGroupReceived(event.data);
            chatArea.appendChild(message);
            createMessage = true;
        } else
            message.querySelector('.message-received-text').textContent = message.querySelector('.message-received-text').textContent + event.data;
    };
}
    

sendMessageButton.addEventListener("click", function() {
	const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value;
    console.log(messageText);
    chatArea.appendChild(createMessageGroupSent(messageText));
    sendReplica();
	messageInput.value = '';
});

function draw_messages(chatIdParam) {
    console.log(chatIdParam)
    fetch("http://localhost:8125/chat/api" + "?chat_id=" + chatIdParam)
        .then(res => res.json())
        .then(messages => {
            const chatArea = document.getElementById('chat-area');
            chatArea.innerHTML = ''; // Clear the chat area
            for (const message of messages) {
                console.log(message)
				if (message.is_ai == false){
				 chatArea.appendChild(createMessageGroupSent(message.content));
				} else {
				 chatArea.appendChild(createMessageGroupReceived(message.content));


				}
            }
        });
}

function getChatIdParam() {
    const searchParams = new URLSearchParams(window.location.search);
    var newChatIdParam = searchParams.get('chat_id');
    newChatIdParam = newChatIdParam ? newChatIdParam : "0"
    if (newChatIdParam !== chatIdParam) {
        chatIdParam = newChatIdParam;
        draw_messages(chatIdParam);
    }
}

getChatIdParam()
draw_messages(chatIdParam)

setInterval(() => {
    getChatIdParam()
}, 200);






