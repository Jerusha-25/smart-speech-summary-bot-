# 🎙️ Speech-to-Text Summarization and Question Identification for Enhanced Chatbot Interactions

## 📌 Overview

This project integrates **speech recognition**, **text summarization**, and a **BERT-based question-answering chatbot** into a single web application. It enables users to:

- 🎤 Record speech input
- ✏️ Transcribe speech to text
- 📝 Summarize the transcribed text
- 🤖 Ask intelligent questions about the summarized content

This solution is ideal for accessible AI assistants, educational platforms, and productivity tools.

---

## 📰 Publication

📄 **Published in**: *IEEE Conference on Knowledge Engineering and Communication Systems (KECS)*  
🆔 **Paper ID**: 645

---

## 🚀 Features

- 🎙️ **Speech-to-Text**: Converts spoken words to text using Google Speech Recognition.
- 🔍 **Text Summarization**: Uses `facebook/bart-large-cnn` to generate concise summaries.
- 💬 **Chatbot (Q&A)**: Allows users to ask questions about the summarized content using BERT (`bert-large-uncased-whole-word-masking-finetuned-squad`).
- 🌐 **Flask Web App**: Clean UI with real-time feedback for each step.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Flask**
- **Transformers (Hugging Face)**
- **SpeechRecognition**
- **PyTorch**
- **SoundDevice**
- **HTML + JavaScript**



