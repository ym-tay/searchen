import os
import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from flask import Flask, render_template, request
import PyPDF2

# Ensure NLTK resources are downloaded
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

class SearchEngine:
    def __init__(self, corpus_dir: str, use_stemming: bool = False, use_lemmatization: bool = False):
        self.corpus_dir = corpus_dir
        self.index = defaultdict(list)  # Reverse index
        self.documents = {}  # Stores document contents
        self.use_stemming = use_stemming
        self.use_lemmatization = use_lemmatization
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.load_corpus()
        self.build_index()

    def preprocess_text(self, text: str):
        """Tokenize, remove stopwords, and apply stemming or lemmatization."""
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in self.stop_words]
        if self.use_stemming:
            return [self.stemmer.stem(word) for word in filtered_words]
        elif self.use_lemmatization:
            return [self.lemmatizer.lemmatize(word) for word in filtered_words]
        return filtered_words

    def load_corpus(self):
        for root, _, files in os.walk(self.corpus_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.documents[file] = content
                elif file.endswith('.pdf'):
                    try:
                        with open(file_path, 'rb') as f:
                            reader = PyPDF2.PdfReader(f)
                            content = " ".join(page.extract_text() for page in reader.pages)
                            self.documents[file] = content
                    except Exception as e:
                        print(f"Failed to extract content from {file}: {e}")
                elif file.endswith(('.docx', '.html')):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.documents[file] = content
                elif file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    self.documents[file] = f"Image file at {file_path}"

    def build_index(self):
        """Build a reverse index from the loaded documents."""
        for doc_id, content in self.documents.items():
            if isinstance(content, str):
                words = self.preprocess_text(content)
                for word in words:
                    self.index[word].append(doc_id)

    def search(self, query: str):
        """Perform a simple search for the query in the indexed documents."""
        query_words = self.preprocess_text(query)
        results = set(self.index[query_words[0]]) if query_words else set()
        for word in query_words[1:]:
            results &= set(self.index[word])
        return list(results)

# Flask App
app = Flask(__name__)
corpus_directory = "./corpus"  # Replace with your corpus directory
search_engine = SearchEngine(corpus_directory, use_stemming=True, use_lemmatization=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = search_engine.search(query)
        return render_template('results.html', query=query, results=results)
    return render_template('search.html')

if __name__ == "__main__":
    app.run(debug=True)
