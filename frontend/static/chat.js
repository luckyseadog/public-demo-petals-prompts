const sendMessageButton = document.getElementById("sendMessageButton");
const chatArea = document.getElementById("chat-area");
var chatFields = document.getElementsByClassName("chat-element-link");
var chatIdParam = "0";

Array.from(chatFields).forEach(function(chatField) {
    chatField.addEventListener("click", function() {
        const chatId= chatField.getAttribute("chat_id")
        var queryParams = new URLSearchParams(window.location.search);
        queryParams.set("chat_id", chatId);
        history.replaceState(null, null, "?"+queryParams.toString());
    });
});

sendMessageButton.addEventListener("click", function() {
    // const searchParams = new URLSearchParams(window.location.search);
    // const chatIdParam = searchParams.get('chat_id');
    const chatIdParamInt = parseInt(chatIdParam, 10);


	const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value;


 	const url = 'http://localhost:8094/chat/add_message';
    const data = {"chat_id": chatIdParamInt, "content": messageText};

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
        console.log('Сервер ответил:', responseData);
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
	// chatArea.appendChild(createMessageGroupSent(data));
	// chatArea.appendChild(createMessageGroupReceived(data));

	messageInput.value = '';


});

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
    messageReceivedText.textContent = message['content'];

    messageReceived.appendChild(messageReceivedText);
    messageGroupReceived.appendChild(avatarDiv);
    messageGroupReceived.appendChild(messageDiv);

    return messageGroupReceived;
}

function createMessageGroupSent(message) {
    const messageGroupReceived = document.createElement('div');
    messageGroupReceived.classList.add('message-group-sent');

    const messageReceived = document.createElement('div');
    messageReceived.classList.add('message-sent');

    const messageReceivedText = document.createElement('div');
    messageReceivedText.classList.add('message-sent-text');
    messageReceivedText.textContent = message['content'];

    messageReceived.appendChild(messageReceivedText);
	messageGroupReceived.appendChild(messageReceived);

    return messageGroupReceived;
}


function draw_messages(chatIdParam) {
    fetch("http://localhost:8094/chat" + "?chat_id=" + chatIdParam)
        .then(res => res.json())
        .then(messages => {
            const chatArea = document.getElementById('chat-area');
            chatArea.innerHTML = ''; // Clear the chat area
            for (const message of messages) {
				if (message.is_ai == false){
				 chatArea.appendChild(createMessageGroupSent(message));
				} else {
				 chatArea.appendChild(createMessageGroupReceived(message));


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
    }
}

getChatIdParam()
draw_messages(chatIdParam)


setInterval(() => {
    getChatIdParam()
}, 200);

setInterval(() => {
    draw_messages(chatIdParam);
}, 2000);


// window.addEventListener('pushstate', function(event) {
//     const searchParams = new URLSearchParams(window.location.search);
//     const newChatIdParam = searchParams.get('chat_id') || "1"; // Use "1" as default if chat_id is not found
//     if (newChatIdParam !== chatIdParam) {
//         // If chat_id has changed, update chatIdParam and call draw_messages
//         chatIdParam = newChatIdParam;
//         draw_messages(chatIdParam);
//     }
// });


// window.onpopstate = function (event) {
//     // Get the current chat_id from the URL and update the chatIdParam
//     const searchParams = new URLSearchParams(window.location.search);
//     const newChatIdParam = searchParams.get('chat_id') || "1"; // Use "1" as default if chat_id is not found
//     if (newChatIdParam !== chatIdParam) {
//         // If chat_id has changed, update chatIdParam and call draw_messages
//         chatIdParam = newChatIdParam;
//         draw_messages(chatIdParam);
//     }
// };