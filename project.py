import nltk
from nltk.corpus import movie_reviews, stopwords, wordnet
import string, random
from stanford_parser import parser as sp
parser = sp.Parser()


def generate_opinion_keywords():
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
    opinion_keywords = []
    f = open('opinions.txt', 'w')
    for opinion, presence in classifier.most_informative_features(n=len(featurelist)):
        if presence == 1: 
            opinion_keywords.append(opinion) 
            print opinion
        f.write("%s\n" % opinion)

    return opinion_keywords


def generate_feature_keywords():
    #via Zhuang et all. "Movie Review Mining and Summarization"
    features = ['film', 'movie', 'story', 'plot', 'script', 'storyline', 
        'dialogue', 'screenplay', 'ending', 'line', 'scene', 'tale', 
        'character', 'characterization', 'role', 'fight-scene', 'action-scene', 
        'action-sequence', 'set', 'battle-scene', 'picture', 'scenery', 
        'setting','visual-effects', 'color', 'background', 'image', 'music', 
        'score', 'song', 'sound', 'soundtrack', 'theme', 'special-effects', 
        'effect', 'CGI', 'SFX']

    f = open('features.txt', 'w')
    for word in features:
        f.write("%s\n" % word)

    return features

def load_feature_keywords():
    try:
        with open('features.txt', 'r') as features:
            return [word.strip() for word in features.readlines()]
    except:
        print "Generating feature keywords."
        return generate_feature_keywords()

def load_opinion_keywords():
    try:
        with open('opinions.txt', 'r') as opinions:
            return [word.strip() for word in opinions.readlines()]
    except:
        print "Generating opinion keywords. Might take a while."
        return generate_opinion_keywords()

def shortest_path(sentence, opinion, feature):
    parsed = parser.parseToStanfordDependencies(sentence)
    dependencies = [(rel, gov.text, dep.text) for rel, gov, dep in parsed.dependencies]
    for rel, gov, dep in dependencies:
        if (gov == opinion and dep == feature) or (gov == feature and dep == opinion):
            return rel, gov, dep


def keyword_opinion_pairs():
    opinions = set(load_opinion_keywords()[:100])
    features = set(load_feature_keywords())

    for sent in movie_reviews.sents()[:2000]:
        try: 
            words = set(sent)
            if words & opinions != set() and words & features != set():
                sent_str = string.join(sent, ' ')
                for word in sent:
                    if word in opinions:
                        opinion = word
                    if word in features:
                        feature = word
                # print sent_str
                shortest_path(sent_str, opinion, feature)
                print "Success for sentence with length %i" % len(sent)
        except:
            print "Failure for sentence with length %i" % len(sent)
                # print shortest_path(sent_str, opinion, feature)

keyword_opinion_pairs()
# generate_feature_keywords()
# generate_opinion_keywords()
# print type(x[0])
# opinion_keywords()
