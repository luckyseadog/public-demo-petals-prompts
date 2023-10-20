
const sendMessageButton = document.getElementById("sendMessageButton");
const chatArea = document.getElementById('chat-area');

sendMessageButton.addEventListener("click", function() {
	const messageInput = document.getElementById("messageInput");

    const messageText = messageInput.value;


 	const url = 'http://localhost:8094/chat/add_message';
    const data = {"content": messageText }; // Wrap the messageText in an object

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


function draw_messages() {
    fetch("http://localhost:8094/chat")
        .then(res => res.json())
        .then(messages => {
            const chatArea = document.getElementById('chat-area');
            chatArea.innerHTML = ''; // Clear the chat area
            for (const message of messages) {
                console.log(message);
				if (message.is_ai == false){
				 chatArea.appendChild(createMessageGroupSent(message));
				} else {
				 chatArea.appendChild(createMessageGroupReceived(message));


				}
            }
        });
}

draw_messages()
setInterval(draw_messages, 2000)
