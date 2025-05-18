const fastapiFetchBtn = document.getElementById('fastapiFetchBtn');
const fastapiCreateBtn = document.getElementById('fastapiCreateBtn');
const fastapiResponse = document.getElementById('fastapiResponse');
const FASTAPI_SERVER_URL = 'http://127.0.0.1:8001';
//fetch data from data from entire database
fastapiFetchBtn.addEventListener('click', async () => {
    try {
        fastapiResponse.textContent = 'Loading...';

        const response = await fetch(`${FASTAPI_SERVER_URL}/api/messages`);
        const data = await response.json();

        fastapiResponse.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        fastapiResponse.textContent = `Error: ${error.message}\n\nMake sure the FastAPI server is running on port 8001`;
        console.error('Error fetching from FastAPI server:', error);
    }
});
// create data and put into database
fastapiCreateBtn.addEventListener('click', async () => {
    try {
        fastapiResponse.textContent = 'Creating...';

        const messageText = prompt('Enter a message:', 'Hello from browser!');
        if (!messageText) {
            fastapiResponse.textContent = 'Message creation cancelled';
            return;
        }

        const response = await fetch(`${FASTAPI_SERVER_URL}/api/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: messageText })
        });
        if (!response.ok) {
            const errorData = await response.json();
            fastapiResponse.textContent = `error: ${response.status} - ${errorData.detail}`;
            return;
        }
        const newMessage = await response.json();
        fastapiResponse.textContent = `Message created successfully:\n${JSON.stringify(newMessage, null, 2)}`;

    } catch (error) {
        fastapiResponse.textContent = `Error: ${error.message}\n\nMake sure the FastAPI server is running on port 8001`;
        console.error('Error creating message:', error);
    }
});