import pandas as pd
import re
import emoji
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import numpy as np
def clean_text(text):
    """
    
    remove null values and non-ASCII characters
    """
    if pd.isnull(text):
        return ""
    
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')  # removes all emojis
    
    # Remove non-ASCII characters (Amharic, etc.)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remove non-alphanumeric characters (except basic punctuation)
    text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', ' ', text)

    # Keep only letters and whitespace
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

class SentimentAnalysis:
    sid = SentimentIntensityAnalyzer()
    nltk.download('vader_lexicon')
    nlp = spacy.load("en_core_web_sm")
    def get_sentiment(self, text):
        """
        Compute sentiment for a given text.
        Returns:
        sentiment_label: 'positive', 'neutral', or 'negative'
        sentiment_score: compound score as a float
        """
        scores = self.sid.polarity_scores(text)
        compound = scores['compound']
        # Define thresholds for sentiment labels
        if compound >= 0.05:
            label = 'positive'
        elif compound <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        return label, compound


    """
    Preprocessing includes lemmatization and stopword removal, 
    which improves keyword extraction quality.
    """
    def preprocess_text(self, text):
        
        
        """
        Preprocess the input text:
        - Lowercase
        - Remove stopwords
        - Lemmatize
        - Keep only alphabetic tokens
        """
        # Check if the input is a string
        if not isinstance(text, str):
            return ""
        
        # Use spaCy to process the text
        doc = self.nlp(text.lower())
        
        # Token filtering: remove stopwords and non-alphabetic tokens, apply lemmatization
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        
        # Join tokens back to a string
        return " ".join(tokens)
   

def handle_missing_values(text):
    if pd.isna(text):
        return ''
    else:
        return text
    


class ThematicAnalysis:
    def assign_theme(self, keywords_list):
            theme_mapping = {
            'stability': ['crash', 'freeze', 'error'],
            'performance': ['slow', 'lag', 'delay'],
            'ui': ['ui', 'interface', 'design'],
            'support': ['support', 'help', 'service']
            }
            themes = []
            for keywords in keywords_list:
                found_themes = set()
                for theme, key_terms in theme_mapping.items():
                    if any(term in keywords for term in key_terms):
                        found_themes.add(theme)
                themes.append(', '.join(found_themes) if found_themes else 'General')
            return themes
    def extract_keywords(self, reviews, top_n=5):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(reviews)
        features = np.array(vectorizer.get_feature_names_out())
        keywords_list = []
        for idx in range(X.shape[0]):
            weights = X[idx].toarray().ravel()
            top_idx = weights.argsort()[-top_n:]
            keywords_list.append(features[top_idx])
        return keywords_list