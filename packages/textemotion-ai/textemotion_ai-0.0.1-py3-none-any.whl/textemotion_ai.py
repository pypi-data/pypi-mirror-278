from textblob import TextBlob
 
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"
 
def main():
    print("Enter text for sentiment analysis (or 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        sentiment = analyze_sentiment(user_input)
        print(f"Sentiment: {sentiment}")
 
if __name__ == "__main__":
    main()