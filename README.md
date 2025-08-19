This project implements a retrieval-based chatbot in Python for a focused domain. The chatbot responds to user queries by matching them with pre-defined knowledge base entries using TF-IDF and cosine similarity. It also maintains a user profile to personalize interactions.

Features

Domain-Specific Chatbot: Focused on a particular subject area to provide accurate and relevant responses.

TF-IDF + Cosine Similarity: Uses TF-IDF vectorization for the knowledge base and cosine similarity to select the most appropriate response.

Web Data Collection: Scraped data from 20+ websites using BeautifulSoup to build a rich knowledge base.

User Profiling: Stores user queries, names, likes, and dislikes in a JSON-based profile to personalize responses and maintain conversational context.

High Precision: Achieved 90.2% precision in response accuracy.
