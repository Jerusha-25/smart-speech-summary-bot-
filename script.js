// Speech-to-Text
document.getElementById('recordBtn').addEventListener('click', async () => {
    const response = await fetch('/transcribe', { method: 'POST' });
    const data = await response.json();
    if (data.success) {
        document.getElementById('transcription').innerText = data.transcription;
    } else {
        alert('Error: ' + data.error);
    }
});

// Text Summarization
document.getElementById('summarizeBtn').addEventListener('click', async () => {
    const text = document.getElementById('textInput').value;
    const response = await fetch('/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    const data = await response.json();
    document.getElementById('summaryOutput').innerText = data.summary;
});

// Ask Question
document.getElementById('askBtn').addEventListener('click', async () => {
    const question = document.getElementById('questionInput').value;
    const context = document.getElementById('transcription').innerText;
    const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, context })
    });
    const data = await response.json();
    document.getElementById('answerOutput').innerText = data.answer;
});
