# 📚 PaperPilot AI – Multi-Agent Research Paper Assistant

## Overview

PaperPilot AI is a Python-based multi-agent research paper assistant designed to help students understand, analyze, and present academic research papers.

The application uses specialized agents to generate research summaries, extract important technical concepts, create PowerPoint presentations, and prepare viva questions and answers.

It provides a simple and interactive interface built using Streamlit.

## ✨ Features

### 1. Research Paper Upload
- Upload research papers in PDF format.
- Extract text from uploaded research papers.
- Display extracted character count.

### 2. Research Paper Summarizer
- Generate structured summaries.
- Explain the research problem and methodology.
- Present important findings and experimental results.

### 3. Concept Extractor
- Identify important technical concepts.
- Provide explanations for each concept.
- Explain the importance of each concept.

### 4. PowerPoint Presentation Generator
- Automatically create a PowerPoint presentation.
- Generate slides containing important research information.
- Include diagrams explaining technical components.
- Download the generated presentation.

### 5. Viva Preparation Agent
- Generate important viva questions and answers.
- Display answers with source references.
- Help students prepare for research paper presentations and examinations.

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Ollama
- Llama 3.2 (1B)
- PyMuPDF
- Python-PPTX
- ChromaDB

## 📁 Project Structure

```text
PaperPilot-AI/
│
├── agents/
│   ├── summarizer.py
│   ├── concept_extractor.py
│   ├── slide_generator.py
│   ├── viva_agent.py
│   └── verified_slide_content.py
│
├── rag/
│   ├── pdf_processor.py
│   ├── embeddings.py
│   └── retriever.py
│
├── utils/
│   ├── llm.py
│   └── prompts.py
│
├── data/
│   └── uploaded_papers/
│
├── vectorstore/
│
├── app.py
├── requirements.txt
├── README.md
└── test_setup.py
```

## ⚙️ Installation and Setup

### Prerequisites

- Python installed
- Ollama installed
- Git installed (for GitHub setup)

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PaperPilot-AI
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Environment

**Windows PowerShell:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Download the Ollama Model

```bash
ollama pull llama3.2:1b
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🚀 How to Use

1. Launch PaperPilot AI.
2. Upload a research paper in PDF format.
3. Click **Read and Process Research Paper**.
4. Open the Summary tab to generate a summary.
5. Open the Concepts tab to explore important concepts.
6. Open the Presentation tab to generate and download PowerPoint slides.
7. Open the Viva Questions tab to prepare for examinations.

## 📖 Sample Research Paper

The project was developed and tested using:

**Attention Is All You Need**

Authors: Ashish Vaswani et al.

Published: NeurIPS 2017

## 🎯 Project Objective

The objective of PaperPilot AI is to simplify the process of understanding academic research papers by dividing tasks among specialized agents.

It aims to help students save time, understand technical concepts, prepare presentations, and practice viva questions.

## 🔮 Future Enhancements

- Support for multiple research papers.
- Dynamic concept extraction for different papers.
- Improved retrieval-augmented generation (RAG).
- More advanced multi-agent collaboration.
- Export summaries and questions into downloadable documents.

## 👨‍💻 Project Information

**Project Name:** PaperPilot AI

**Project Type:** AI-Based Multi-Agent Research Assistant

**Interface:** Streamlit

**Language:** Python

---

*PaperPilot AI – Making Research Papers Easier to Understand.*
