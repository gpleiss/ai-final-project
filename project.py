import nltk
from nltk.corpus import movie_reviews, stopwords, wordnet
import string, random
from stanford_parser import parser as sp
from jpype import JavaException


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





def construct_dependency_tree(parsed):
    root = parsed.dependencies_root
    dependencies = set([(rel, gov.text, dep.text) for rel, gov, dep in parsed.dependencies])
    children = [(rel, gov, dep) for (rel, gov, dep) in dependencies if gov == root]
    dependencies = dependencies - set(children)

    remaining_nodes = [nltk.Tree(dep, []) for (rel, gov, dep) in children]
    tree = nltk.Tree(root, remaining_nodes)

    while dependencies != set():
        #find current node and its children
        node = remaining_nodes.pop(0)
        children = [(rel, gov, dep) for (rel, gov, dep) in dependencies if gov == node.node]
        children_nodes = [nltk.Tree(dep, []) for (rel, gov, dep) in children]
        
        #update relevant structures
        remaining_nodes.extend(children_nodes)
        node.extend(children_nodes)
        dependencies = dependencies - set(children)
    return tree

def val_in_tree(tree, val):
    if (tree.node == val):
        return True
    for child in tree:
        if val_in_tree(child, val):
            return True
    return False

def dist_to_root(tree, val):
    if tree.node == val:
        return 0
    for child in tree:
        if val_in_tree(child, val):
            return 1 + dist_to_root(child, val)

def dist_btwn_feature_and_opinion(feature, opinion, sentence, parser):
    parsed = parser.parseToStanfordDependencies(sentence)
    tree = construct_dependency_tree(parsed)
    subtrees = tree.subtrees(filter=lambda t: val_in_tree(t,feature) and val_in_tree(t,opinion))

    smallest_tree, height = None, 10000
    for subtree in subtrees:
        if subtree.height() < height:
            smallest_tree = subtree
            height = subtree.height()
    distance = dist_to_root(smallest_tree, feature) + dist_to_root(smallest_tree, opinion)
    return distance

def find_summary_sentence(fileid, opinions, features, parser):
    summary_sents = [sent for sent in movie_reviews.sents(fileid)
                     if (set(sent) & opinions != set()) and (set(sent) & features != set())]
    summary_sents_with_feature_opinion_dist = []
    for sent in summary_sents:
        try:
            sent_str = string.join(sent, ' ')
            for word in sent:
                if word in opinions:
                    opinion = word
                elif word in features:
                    feature = word
            distance = dist_btwn_feature_and_opinion(feature, opinion, sent_str, parser)
            summary_sents_with_feature_opinion_dist.append((distance, sent_str))
        except JavaException:
            # print "Failure: sentence is too long (len = %i)" % len(sent)
            pass
        except AssertionError:
            # print "Failure: could not find root"
            pass

    summary_sents_with_feature_opinion_dist.sort()
    if len(summary_sents_with_feature_opinion_dist) > 0:
        return summary_sents_with_feature_opinion_dist[0][1]
    else:
        return None


if __name__ == '__main__':
    parser = sp.Parser()
    opinions = set(load_opinion_keywords()[:100])
    features = set(load_feature_keywords())
    for fileid in movie_reviews.fileids():
        print "\nReview:", fileid
        print "Summary:\n", find_summary_sentence(fileid, opinions, features, parser)
