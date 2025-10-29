## UTS PI 1

import os
import json
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.query import Or
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re

class IRSystem:
    def __init__(self, dataset_path="dataset", index_dir="indexdir"):
        self.dataset_path = dataset_path
        self.index_dir = index_dir
        self.documents = []
        self.vectorizer = CountVectorizer()
        self.doc_vectors = None
        
        # Stopword
        self.stopwords = set([
            'yang', 'untuk', 'pada', 'ke', 'para', 'namun', 'menurut', 'antara', 
            'dengan', 'dari', 'adalah', 'ini', 'itu', 'akan', 'atau', 'dan', 
            'di', 'dalam', 'oleh', 'juga', 'ada', 'dapat', 'telah', 'tersebut',
            'seperti', 'tidak', 'lebih', 'karena', 'sudah', 'saat', 'bisa',
            'tersebut', 'bila', 'jika', 'maka', 'serta', 'sebagai', 'yaitu'
        ])
        
    def preprocess_text(self, text):
        """
        Text preprocessing:
        - Case folding
        - Tokenization
        - Stopword removal
        """
        # Case folding
        text = text.lower()
        
        # Hapus karakter spesial dan angka
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Tokenisasi
        tokens = text.split()
        
        # Penghapusan stopword
        tokens = [token for token in tokens if token not in self.stopwords and len(token) > 2]
        
        return ' '.join(tokens)
    
    def load_dataset(self, dataset_name):
        """Load documents from a specific CSV dataset file"""
        dataset_file = os.path.join(self.dataset_path, f"{dataset_name}.csv")
        docs = []

        if not os.path.exists(dataset_file):
            print(f"Warning: Dataset file '{dataset_file}' not found!")
            return docs

        print(f"Loading dataset: {dataset_name}...")

        try:
            df = pd.read_csv(dataset_file, encoding='utf-8')
            for idx, row in df.iterrows():
                title = str(row['judul']).strip()
                content = str(row['konten']).strip()
                if content:
                    docs.append({
                        'id': f"{dataset_name}_{idx}",
                        'title': title,
                        'content': content,
                        'source': dataset_name,
                        'path': dataset_file
                    })
        except Exception as e:
            print(f"Error reading {dataset_file}: {e}")

        print(f"Loaded {len(docs)} documents from {dataset_name}")
        return docs
    
    def load_all_datasets(self):
        """Load all five required datasets"""
        datasets = ['etd_usk', 'etd_ugm', 'kompas', 'tempo', 'mojok']
        self.documents = []

        print("\n=== Loading All Datasets ===")
        for dataset in datasets:
            docs = self.load_dataset(dataset)
            self.documents.extend(docs)

        print(f"\nTotal documents loaded: {len(self.documents)}")
        return len(self.documents)
    
    def create_index(self):
        """Create Whoosh index for all documents"""
        if not self.documents:
            print("No documents to index!")
            return False
        
        print("\n=== Creating Index ===")
        
        # Membuat direktori index jika tidak ada
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
        
        # Definisikan schema
        schema = Schema(
            doc_id=ID(stored=True, unique=True),
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            source=TEXT(stored=True),
            preprocessed=TEXT(stored=True)
        )
        
        # Membuat atau membuat ulang index
        ix = create_in(self.index_dir, schema)
        writer = ix.writer()
        
        print("Indexing documents...")
        for i, doc in enumerate(self.documents):
            preprocessed = self.preprocess_text(doc['content'])
            writer.add_document(
                doc_id=doc['id'],
                title=doc['title'],
                content=doc['content'],
                source=doc['source'],
                preprocessed=preprocessed
            )
            if (i + 1) % 100 == 0:
                print(f"Indexed {i + 1}/{len(self.documents)} documents")
        
        writer.commit()
        print(f"Indexing complete! Total: {len(self.documents)} documents")
        
        # Membuat vektor dokumen untuk cosine similarity
        self._create_vectors()
        
        return True
    
    def _create_vectors(self):
        """Create BoW vectors for all documents"""
        print("\n=== Creating Document Vectors (BoW) ===")
        preprocessed_docs = [self.preprocess_text(doc['content']) for doc in self.documents]
        self.doc_vectors = self.vectorizer.fit_transform(preprocessed_docs)
        print(f"Vocabulary size: {len(self.vectorizer.vocabulary_)}")
        print(f"Document vectors shape: {self.doc_vectors.shape}")
    
    def search(self, query_text, top_k=5):
        """
        Mencari dokumen dengan Whoosh dan me ranking menggunakan cosine similarity
        """
        if not exists_in(self.index_dir):
            print("Index tidak ditemukan! Silakan muat dan indeks dataset terlebih dahulu.")
            return []
        
        if self.doc_vectors is None:
            print("Vektor dokumen tidak ditemukan! Silakan muat dan indeks dataset terlebih dahulu.")
            return []
        
        print(f"\n=== Mencari: '{query_text}' ===")
        
        # Preprocess query
        preprocessed_query = self.preprocess_text(query_text)
        print(f"Preprocessed query: '{preprocessed_query}'")
        
        # Whoosh search to get candidate documents
        ix = open_dir(self.index_dir)
        with ix.searcher() as searcher:
            # Search in preprocessed field
            query = QueryParser("preprocessed", ix.schema).parse(preprocessed_query)
            results = searcher.search(query, limit=None)
            
            if len(results) == 0:
                print("No documents found matching the query.")
                return []
            
            print(f"Found {len(results)} candidate documents from Whoosh")
            
            # Mendapatkan indeks dokumen yang cocok
            candidate_ids = [hit['doc_id'] for hit in results]
        
        # Menghitung cosine similarity untuk ranking
        query_vector = self.vectorizer.transform([preprocessed_query])
        
        # Mencari indeks dokumen kandidat
        candidate_indices = []
        for i, doc in enumerate(self.documents):
            if doc['id'] in candidate_ids:
                candidate_indices.append(i)
        
        if not candidate_indices:
            return []
        
        # menghitung kemiripan
        similarities = cosine_similarity(query_vector, self.doc_vectors[candidate_indices])[0]
        
        # Membuat hasil dengan skor
        ranked_results = []
        for idx, similarity in zip(candidate_indices, similarities):
            if similarity > 0:  # Hanya menyertakan dokumen dengan kemiripan positif
                ranked_results.append({
                    'doc': self.documents[idx],
                    'score': similarity
                })
        
        # urut berdasarkan skor
        ranked_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top k results
        return ranked_results[:top_k]
    
    def display_results(self, results):
        """Menampilkan hasil pencarian dalam format yang rapi"""
        if not results:
            print("\nTidak ada dokumen yang relevan ditemukan.")
            return
        
        print(f"\n=== Top {len(results)} Results ===\n")
        for i, result in enumerate(results, 1):
            doc = result['doc']
            score = result['score']
            
            print(f"Rank {i}:")
            print(f"  Title: {doc['title']}")
            print(f"  Source: {doc['source']}")
            print(f"  Score: {score:.4f}")
            
            # Menampilkan potongan konten
            content_preview = doc['content'][:200].replace('\n', ' ')
            print(f"  Preview: {content_preview}...")
            print(f"  Path: {doc.get('path', 'N/A')}")
            print()


def main():
    """Main CLI interface"""
    ir_system = IRSystem()
    
    while True:
        print("\n" + "="*40)
        print("=== INFORMATION RETRIEVAL SYSTEM ===")
        print("="*40)
        print("[1] Load & Index Dataset")
        print("[2] Search Query")
        print("[3] Exit")
        print("="*40)
        
        choice = input("\nSelect menu [1-3]: ").strip()
        
        if choice == '1':
            num_docs = ir_system.load_all_datasets()
            if num_docs > 0:
                ir_system.create_index()
            else:
                print("\nTidak ada dokumen ditemukan! Silakan periksa struktur folder dataset Anda.")
                print("Expected structure:")
                print("dataset/")
                print("  ├── etd_usk.csv")
                print("  ├── etd_ugm.csv")
                print("  ├── kompas.csv")
                print("  ├── tempo.csv")
                print("  └── mojok.csv")
        
        elif choice == '2':
            query = input("\nMasukkan query pencarian Anda: ").strip()
            if query:
                results = ir_system.search(query, top_k=5)
                ir_system.display_results(results)
            else:
                print("Query tidak boleh kosong!")
        
        elif choice == '3':
            print("\nThank you for using Information Retrieval System!")
            print("Goodbye!")
            break
        
        else:
            print("\nPilihan tidak valid! Silakan pilih 1, 2, atau 3.")


if __name__ == "__main__":
    main()