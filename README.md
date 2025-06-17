# 💬 Azure OpenAI Embedding Project

This project uses the Azure OpenAI API to generate text embeddings. Sensitive credentials are stored securely using a `.env` file.

## 📦 Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/)
- Azure OpenAI credentials

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Create a .env file

In the project root, create a .env file with the following content:
```bash
AZURE_OPENAI_API_KEY=6bR0hwgRDji8eZlHCkA6zo6bZM2MUZ6WT1h8dnd4TxLvaAjo6DKIJQQJ99BFACHYHv6XJ3w3AAAAACOGc5f1
AZURE_OPENAI_ENDPOINT=https://litao-mbnnzbvd-eastus2.cognitiveservices.azure.com
AZURE_OPENAI_API_VERSION1=2023-05-15
AZURE_OPENAI_API_VERSION2=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=text-embedding-ada-002
```
⚠️ Do not commit this file. It's excluded via .gitignore.

### 4. Run the project

```bash
poetry run python app.py
```

🔐 Security

Your API keys are stored in .env and never exposed.<br>
.env is included in .gitignore.


