function sendMessage() {
    // Get the input value
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    // If the input is not empty, create a new chat message
    if (message !== '') {
        const chatBox = document.getElementById('chatBox');
        const historyContainer = document.getElementById('history-content'); // Corrected ID

        // Create the chat message element
        const newMessage = document.createElement('div');
        newMessage.className = 'chat-message mb-3';
        newMessage.innerHTML = `
            <div class="d-flex justify-content-end">
                <div class="message bg-primary text-white p-2">${message}</div>
                <div class="user-icon bg-primary text-white rounded ms-2">
                    <i class="bi bi-person-fill fs-3"></i>
                </div>
            </div>
        `;

        // Append the new message to the chat box
        chatBox.appendChild(newMessage);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear the input field
        input.value = '';

        // Create a new history item and prepend it to the historyContainer
        const newHistoryItem = document.createElement('div');
        newHistoryItem.className = 'content';
        newHistoryItem.innerHTML = `<div class="content">${message}</div>`;
        historyContainer.insertBefore(newHistoryItem, historyContainer.firstChild);

        // Scroll to the top of the history container to show the most recent item
        historyContainer.scrollTop = 0;
    }
}

function clearHistory() {
    const historyContainer = document.getElementById('chatBox');

    // Remove all child elements from historyContainer
    while (historyContainer.firstChild) {
        historyContainer.removeChild(historyContainer.firstChild);
    }
}
