from SentimentClassification import Analyzer

analyzer = Analyzer()

while __name__ == "__main__":
    user = input(" 아무거나 써보세요! > ")
    feeling = analyzer.analyze(user)[0]

    print(feeling)