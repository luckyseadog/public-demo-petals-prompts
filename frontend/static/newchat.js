const sendMessageButton = document.getElementById("sendMessageButton");
const chatArea = document.getElementById("chat-area");
var chatFields = document.getElementsByClassName("chat-element-link");
var chatIdParam = "0";
// var ws = null;
ws = new WebSocket("ws://localhost:8094/chat/api/add-massage-websocket");

Array.from(chatFields).forEach(function(chatField) {
    chatField.addEventListener("click", function() {
        const chatId= chatField.getAttribute("chat_id")
        var queryParams = new URLSearchParams(window.location.search);
        queryParams.set("chat_id", chatId);
        history.replaceState(null, null, "?"+queryParams.toString());
    });
});


function openSession() {
    ws = new WebSocket("ws://localhost:8094/chat/api/add-massage-websocket");
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
            console.log(event) // how event looks like??????
            message = createMessageGroupReceived({"content": event.data});
            chatArea.appendChild(message)
            createMessage = true;
        } else
            message.querySelector('.message-received-text').textContent = message.querySelector('.message-received-text').textContent + event.data
    };
}
    

sendMessageButton.addEventListener("click", function() {
	const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value;
    sendReplica()
    chatArea.appendChild(createMessageGroupSent({"content": messageText}));
    console.log(messageText);
	messageInput.value = '';
});

function draw_messages(chatIdParam) {
    fetch("http://localhost:8094/chat/api" + "?chat_id=" + chatIdParam)
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


function createMessageGroupReceived(message) {
    const messageGroupReceived = document.createElement('div');
    messageGroupReceived.classList.add('message-group-received');

    const avatarDiv = document.createElement('div');
    const avatarImg = document.createElement('img');
    avatarImg.src = "https://api.dicebear.com/7.x/pixel-art-neutral/svg?seed=Rascal&backgroundColor=b68655";
    avatarImg.alt = "avatar";
    avatarDiv.appendChild(avatarImg);

    const messageDiv =  document.createElement('div');
    const messageReceived = document.createElement('div');
    messageReceived.classList.add('message-received');
    messageDiv.appendChild(messageReceived);

    const messageReceivedText = document.createElement('div');
    messageReceivedText.classList.add('message-received-text');
    messageReceivedText.textContent = message;

    messageReceived.appendChild(messageReceivedText);
    messageGroupReceived.appendChild(avatarDiv);
    messageGroupReceived.appendChild(messageDiv);

    return messageGroupReceived;
}

function createMessageGroupSent(message) {
    const messageGroupSent = document.createElement('div');
    messageGroupSent.classList.add('message-group-sent');

    const messageSent = document.createElement('div');
    messageSent.classList.add('message-sent');

    const messageSentText = document.createElement('div');
    messageSentText.classList.add('message-sent-text');
    messageSentText.textContent = message;

    messageSent.appendChild(messageSentText);
	messageGroupSent.appendChild(messageSent);

    return messageGroupSent;
}



