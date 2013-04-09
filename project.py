import nltk
from nltk.corpus import movie_reviews, stopwords, wordnet
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

    def words_in_synset(word):
        possible_synsets = wordnet.synsets(word)
        if len(possible_synsets) == 0:
            return word.lower()
        else:
            return [syn.lower() for syn in possible_synsets[0].lemma_names]

    stopword_set = stopwords.words('english')
    words =  movie_reviews.words()
    fdist = nltk.FreqDist(word.lower() for word in movie_reviews.words()
                    if word.lower() not in stopword_set and \
                    word not in string.punctuation)
    featurelist = fdist.keys()[:1000]

    featurelist_with_synset_words = []
    for feature in featurelist:
        featurelist_with_synset_words.extend(words_in_synset(feature))
    
    pos_reviews = [([word for word in movie_reviews.words(fileid)], 'pos') for fileid in movie_reviews.fileids('pos')]
    neg_reviews = [([word for word in movie_reviews.words(fileid)], 'neg') for fileid in movie_reviews.fileids('neg')]
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
    classifier.show_most_informative_features(10)


opinion_keywords()