

export function createMessageGroupReceived(message) {
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

export function createMessageGroupSent(message) {
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