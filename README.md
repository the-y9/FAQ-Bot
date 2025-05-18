# 📚 FAQ-Bot

FAQ-Bot is a lightweight, semantic search-based chatbot designed to answer frequently asked questions using sentence embeddings. It uses [Sentence-Transformers](https://www.sbert.net/) to find the most relevant answer from a set of predefined FAQs.

---

## 🚀 Features

* ✅ Semantic similarity matching via `all-MiniLM-L6-v2` transformer
* ✅ Efficient embedding caching using `pickle`
* ✅ Simple CLI-based interaction
* ✅ Easily customizable with your own FAQ data
* ✅ Embedding similarity visualization with optional plotting (cosine similarity)

---

## 🧱 Structure

```bash
FAQ-Bot/
├── main.py                 # CLI entry point
├── v1/
│   ├── faq_data.py         # Active FAQ dataset (structured Q&A)
│   ├── faq_bot.py          # Core bot logic and matching
│   └── main.py   
├── v2/
│   ├── faq_data.py         # Embedding creation + caching
│   ├── faq_bot.py          # Updated bot logic and matching
│   ├── viz_utils.py        # Visualization for embeddings (optional)
│   └── main.py        
├── embeddings_cache/
│   └── faq_embeddings.pkl  # Cached embeddings
└── requirements.txt        # Python dependencies
```

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/the-y9/FAQ-Bot.git
cd FAQ-Bot
```

2. **(Optional) Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Start the chatbot via CLI:

```bash
python main.py
```

Type a question into the terminal. The bot will return the best-matching answer using semantic similarity. Type `exit` or `quit` to end the session.

---

## 🧠 How It Works

1. **Data loading & embedding**:

   * The bot loads FAQ entries from `v1/faq_data.py`
   * Questions are encoded using a SentenceTransformer model
   * Embeddings are cached for performance (`./embeddings_cache/faq_embeddings.pkl`)

2. **Question Matching**:

   * When the user asks a question, it's converted into an embedding
   * The bot computes cosine similarity between the user’s embedding and all cached FAQ embeddings
   * The most similar question is returned, if similarity > 0.3

3. **(Optional) Embedding Visualization**:

   * If `viz_utils.py` is configured, the bot can plot the user query and matched question embeddings

---

## 🛠️ Customize FAQ Data

You can edit or add Q\&A entries in `v1/faq_data.py`. Each entry is structured like:

```python
faq_data = [
    {
        "q": "How do I reset my password?",
        "a": "Click on 'Forgot Password' at login and follow the instructions."
    },
    ...
]
```

After editing, embeddings will automatically regenerate on next run, as it uses hashing.

---

## 📊 Requirements

* Python 3.7+
* sentence-transformers
* torch
* numpy
* matplotlib (optional, for visualization)

---

## 🤝 Contributing

Feel free to fork the repo and submit a pull request!