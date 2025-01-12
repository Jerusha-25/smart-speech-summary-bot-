import os
from flask import Flask, render_template, request, session
from transformers import BartForConditionalGeneration, BartTokenizer, BertTokenizer, BertForQuestionAnswering
import speech_recognition as sr
import torch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.urandom(24)  # Required for session to work

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models for summarization and chatbot
summarization_model_name = 'facebook/bart-large-cnn'
summarization_tokenizer = BartTokenizer.from_pretrained(summarization_model_name)
summarization_model = BartForConditionalGeneration.from_pretrained(summarization_model_name)

chatbot_model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
chatbot_tokenizer = BertTokenizer.from_pretrained(chatbot_model_name)
chatbot_model = BertForQuestionAnswering.from_pretrained(chatbot_model_name)

@app.route('/')
def index():
    return render_template('index.html', qa_history=session.get('qa_history', []))

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio_file']
    if audio_file:
        # Save uploaded audio file
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_path)

        # Process audio: Transcription
        transcription = transcribe_audio(audio_path)

        # Process transcription: Summarization
        summary = summarize_large_text(transcription)

        return render_template('index.html', transcription=transcription, summary=summary, qa_history=session.get('qa_history', []))
    return "No file uploaded", 400

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.form['question']
    context = request.form['context']

    # Get answer from BERT chatbot
    answer = get_bert_answer(question, context)

    # Store the question and answer in the session
    if 'qa_history' not in session:
        session['qa_history'] = []

    session['qa_history'].append({'question': question, 'answer': answer})

    # Save session changes
    session.modified = True

    return render_template('index.html', transcription=context, summary="", qa_history=session['qa_history'])

def transcribe_audio(audio_path):
    """
    Function to transcribe the audio file to text using SpeechRecognition.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Google Speech Recognition service error: {e}"

def summarize_large_text(text):
    """
    Function to summarize large text using the BART model.
    """
    inputs = summarization_tokenizer.encode(text, return_tensors="pt", truncation=True)
    summary_ids = summarization_model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return summarization_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def get_bert_answer(question, context):
    """
    Function to get the answer from BERT based on the question and context.
    """
    inputs = chatbot_tokenizer.encode_plus(question, context, return_tensors="pt", truncation=True, max_length=512)
    input_ids = inputs["input_ids"].tolist()[0]
    outputs = chatbot_model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    start_idx = torch.argmax(start_scores)
    end_idx = torch.argmax(end_scores) + 1

    answer = chatbot_tokenizer.convert_tokens_to_string(
        chatbot_tokenizer.convert_ids_to_tokens(input_ids[start_idx:end_idx])
    )
    return answer.strip()

if __name__ == "__main__":
    app.run(debug=True, threaded=False)
