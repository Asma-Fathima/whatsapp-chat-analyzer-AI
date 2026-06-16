# AI-Powered WhatsApp Chat Analyzer

An interactive data analytics dashboard built with Python and Streamlit that parses raw WhatsApp chat exports, visualizes communication trends, and uses Google's Gemini 2.5 Flash model to generate an intelligent executive summary of the conversations.

## Features
- **Raw Data Parsing:** Uses regex to structure messy WhatsApp text logs and multi-line timestamps into clean data frames.
- **Visual Analytics:** Generates timeline activity tracking and member participation charts using Matplotlib and Seaborn.
- **AI Smart Digest:** Connected to the Gemini API via the official Google GenAI SDK to automatically pull main topics, group tone, and key decisions.

## How to Run Locally

1. Clone this repository or download the files.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
