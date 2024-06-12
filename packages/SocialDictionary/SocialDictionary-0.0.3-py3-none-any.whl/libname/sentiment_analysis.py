import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Certifique-se de baixar os recursos necessários do nltk se ainda não o fez
import nltk
nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.emoji_emocao_dict = dict(zip(self.df['Design'], self.df['emotion']))
        self.analyzer = SentimentIntensityAnalyzer()

    def substituir_emoji_por_emocao(self, texto):
        for emoji, emocao in self.emoji_emocao_dict.items():
            texto = texto.replace(emoji, emocao)
        return texto

    def analise_sentimentos(self, texto):
        scores = self.analyzer.polarity_scores(texto)
        sentimento = scores['compound']
        return sentimento

    def analisar_texto(self, texto):
        texto_modificado = self.substituir_emoji_por_emocao(texto)
        sentimento = self.analise_sentimentos(texto_modificado)
        return texto_modificado, sentimento