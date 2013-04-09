import nltk
from nltk.corpus import movie_reviews, stopwords
import string, random

def opinion_keywords():
    def determine_features(review, featurelist):
        result = {}
        for f in featurelist:
            if f in review:
                result[f] = 1
            else:
                result[f] = 0
        return result

    stopword_set = stopwords.words('english')
    words =  movie_reviews.words()
    fdist = nltk.FreqDist(word.lower() for word in movie_reviews.words()
                    if word.lower() not in stopword_set and \
                    word not in string.punctuation)
    featurelist = [word for word in fdist.keys()[:3000]
                    if nltk.pos_tag([word])[0][1] == 'JJ']
    
    pos_reviews = [([word for word in movie_reviews.words(fileid)], 'pos') 
                            for fileid in movie_reviews.fileids('pos')]
    neg_reviews = [([word for word in movie_reviews.words(fileid)], 'neg') 
                            for fileid in movie_reviews.fileids('neg')]

    all_reviews = pos_reviews + neg_reviews
    random.shuffle(all_reviews)

    featuresets =[(determine_features(review, featurelist), label) 
                    for review, label in all_reviews]

    nreviews = len(all_reviews)
    ntrain = int(nreviews * .75)
    train, test = featuresets[:ntrain], featuresets[ntrain:]
    classifier = nltk.NaiveBayesClassifier.train(train)
    
    print "Accuracy of bayes classifier is: "
    print nltk.classify.accuracy(classifier, test)
    classifier.show_most_informative_features(100)
    # ntest = nreviews

    # classifier = nltk.NaiveBayesClassifier.train(train)

def feature_keywords():
    #via Zhuang et all. "Movie Review Mining and Summarization"
    features = ['film', 'movie', 'story', 'plot', 'script', 'storyline', 
        'dialogue', 'screenplay', 'ending', 'line', 'scene', 'tale', 
        'character', 'characterization', 'role', 'fight-scene', 'action-scene', 
        'action-sequence', 'set', 'battle-scene', 'picture', 'scenery', 
        'setting','visual-effects', 'color', 'background', 'image', 'music', 
        'score', 'song', 'sound', 'soundtrack', 'theme', 'special-effects', 
        'effect', 'CGI', 'SFX']

    return features

# opinion_keywords()