from textblob import TextBlob
from local import json_load
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import transformers
import numpy 

def calculate_sentiment_similarity(text1, text2):
    blob1 = TextBlob(text1)
    blob2 = TextBlob(text2)

    sentiment1 = blob1.sentiment.polarity
    sentiment2 = blob2.sentiment.polarity

    # Normalize sentiment values to be between 0 and 1
    normalized_sentiment1 = (sentiment1 + 1) / 2
    normalized_sentiment2 = (sentiment2 + 1) / 2

    # Calculate the absolute difference in sentiment scores
    sentiment_difference = abs(normalized_sentiment1 - normalized_sentiment2)

    # The lower the difference, the more similar the sentiments
    sentiment_similarity = 1 - sentiment_difference

    return sentiment_similarity

def tfidf(text1, text2):
    import sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Convert the texts into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    # Calculate the cosine similarity between the vectors
    similarity = cosine_similarity(vectors)
    return similarity

def bert_score(text1, text2):
    model = transformers.BertModel.from_pretrained('bert-base-uncased')

    # Tokenize and encode the texts
    text1 = "This is the first text."
    text2 = "This is the second text."
    encoding1 = model.encode(text1, max_length=512)
    encoding2 = model.encode(text2, max_length=512)

    # Calculate the cosine similarity between the embeddings
    similarity = numpy.dot(encoding1, encoding2) / (numpy.linalg.norm(encoding1) * numpy.linalg.norm(encoding2))
    return similarity

def calculate_similarity(text1, text2):
    return tfidf(text1, text2)


def remove_stop_words(text) -> str:
    stop_words = set(stopwords.words('english'))
 
    word_tokens = word_tokenize(text)
    # converts the words in word_tokens to lower case and then checks whether 
    #they are present in stop_words or not
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    return ' '.join(filtered_sentence)


def main():
    fp = r".\data.json"
    data = json_load(fp)
    for row in data:
        song = remove_stop_words(row["songs"])
        headline = remove_stop_words(row["headline"])
        row["similarity"] = calculate_similarity(song, headline)
        print(row["similarity"])


    sim_scores = [row["similarity"] for row in data]
    # if we compare randomly how similar are the results?
    import random

    diff_scores = []
    for i in range(1000):
        song_data = random.choice(data)
        headline_data = random.choice(data)
        if song_data != headline_data:
            song = remove_stop_words(song_data["songs"])
            headline = remove_stop_words(headline_data["headline"])
            score = calculate_similarity(song, headline)
            diff_scores.append(score)
            print(score)
    print(f"Songs | Head Line Pairs: {sum(sim_scores)/len(sim_scores)}")
    print(f"Songs | Head Line AntiPairs: {sum(diff_scores)/len(diff_scores)}")

    bp = 0   

if __name__ == "__main__":
    main()