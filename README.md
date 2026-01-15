<div align="center">

# 🤖 S.A.K.H.I
### *Smart AI Knowledge & Human Interface*

[![Python](https://img.shields.io/badge/Language-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/AI_Engine-Groq_LPU-orange?style=for-the-badge&logo=fastapi&logoColor=white)](https://groq.com/)
[![HuggingFace](https://img.shields.io/badge/Models-Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

<br />

> **"Your Intelligent Voice-Activated Desktop Companion."**

[🚀 Features](#-features) · [🛠 Installation](#-installation) · [💻 Usage](#-usage) · [🔑 API Setup](#-api-setup)

</div>

---

## ⚡ Overview

**S.A.K.H.I** is a powerful Python-based desktop assistant designed to bridge the gap between human speech and digital execution. Utilizing the blazing fast speed of **Groq's LPU** and the versatility of **Hugging Face** models, S.A.K.H.I listens to your voice commands, processes complex queries, and responds in natural human-like speech.

It's not just a chatbot; it's a productivity booster that lives on your desktop.

## 💎 Features

| Capability | Description |
| :--- | :--- |
| 🗣️ **Voice Interaction** | Seamless **Speech-to-Text** (Input) and **Text-to-Speech** (Output). |
| 🧠 **Advanced AI** | Powered by **Groq API** for ultra-low latency responses. |
| 🤖 **NLP Engine** | Leverages **Hugging Face** transformers for context understanding. |
| 💻 **Desktop Control** | Can launch applications and perform system tasks. |
| 💬 **Dual Mode** | Supports both voice commands and text-based chat. |
| ⚡ **Real-time** | Optimized for immediate response generation. |

## 🛠️ Tech Stack

Built with a robust ecosystem of Python libraries:

* **Core:** `Python`
* **LLM Inference:** `Groq API` (Llama 3 / Mixtral)
* **Models:** `Hugging Face Hub`
* **Voice Recognition:** `SpeechRecognition`
* **Audio Synthesis:** `pyttsx3` / `gTTS`

## 📂 Project Structure

```text
AI_assistant_Sakhi/
├── main.py              # Entry point of the assistant
├── engine/              # Core logic for speech and processing
│   ├── command.py       # Speech recognition logic
│   └── speak.py         # Text-to-speech engine
├── config/              # Configuration and API keys
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
