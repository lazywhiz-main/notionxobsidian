import re
from typing import List, Dict, Any

class ContentAnalyzer:
    def __init__(self):
        # Simple text processing without external dependencies
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'these', 'they', 'them',
            'their', 'there', 'then', 'than', 'or', 'but', 'not', 'have',
            'had', 'do', 'does', 'did', 'can', 'could', 'would', 'should'
        }

    def preprocess_text(self, text: str) -> str:
        # Simple text preprocessing without spaCy
        text = text.lower()
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]
        return " ".join(filtered_words)

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        # Simple keyword extraction based on word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out stop words and short words
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
        # Count frequency and return top keywords
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        # Sort by frequency and return top_n
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]

    def calculate_similarity(self, texts: List[str]) -> List[List[float]]:
        # Simple similarity calculation based on word overlap
        preprocessed_texts = [self.preprocess_text(text) for text in texts]
        if not preprocessed_texts or all(not t.strip() for t in preprocessed_texts):
            return []
        
        similarity_matrix = []
        for i, text1 in enumerate(preprocessed_texts):
            row = []
            words1 = set(text1.split())
            for j, text2 in enumerate(preprocessed_texts):
                words2 = set(text2.split())
                if not words1 or not words2:
                    similarity = 0.0
                else:
                    intersection = len(words1.intersection(words2))
                    union = len(words1.union(words2))
                    similarity = intersection / union if union > 0 else 0.0
                row.append(similarity)
            similarity_matrix.append(row)
        return similarity_matrix

    def detect_duplicates(self, texts: List[str], threshold: float = 0.8) -> List[Dict[str, Any]]:
        if len(texts) < 2:
            return []
        similarity_matrix = self.calculate_similarity(texts)
        duplicates = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if similarity_matrix[i][j] >= threshold:
                    duplicates.append({
                        "index_a": i,
                        "index_b": j,
                        "similarity": similarity_matrix[i][j],
                        "text_a_snippet": texts[i][:100], # Add snippets for context
                        "text_b_snippet": texts[j][:100]
                    })
        return duplicates

    def analyze_sentiment(self, text: str) -> str:
        # Simple sentiment analysis based on keyword matching
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'best'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing', 'poor'}
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"