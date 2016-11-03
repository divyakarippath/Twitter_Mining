import string
import collections
import codecs
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import math
import pickle
import nltk.metrics
from nltk.metrics import precision
from nltk.metrics import recall
from nltk.metrics import f_measure

PUNCTUATION = set(string.punctuation)
ps = PorterStemmer()
ad_words = []
pers_words = []


# tokenize the tweet messages into words and remove punctuations and stem words
def tokenize(line):
    token_words = word_tokenize(line)
    punct_rem_words = [w for w in token_words if not w in PUNCTUATION]
    stem_rem_words = [ps.stem(w) for w in punct_rem_words]
    return stem_rem_words


# extract features
def get_features(word_features, words):
    features_set = {}
    for w in words:
        features_set[w] = (w.lower() in word_features)
    return features_set


# identify top 3000 words
def get_best_features(ad_words, pers_words):
    all_words = ad_words + pers_words
    all_words = [w.lower() for w in all_words]
    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:3000]
    return word_features


# Generate the feature set
def generateFeatureSet(word_features):
    ad_featureset = []
    pers_featureset = []
    for line in codecs.open("Diabetes-Ad.txt", encoding='latin1'):
        adWords = line.strip().split()
        feature = get_features(word_features, adWords)
        ad_featureset.append((feature, 'ad'))
    for line in codecs.open("Diabetes-Personal.txt", encoding='latin1'):
        persWords = line.strip().split()
        feature = get_features(word_features, persWords)
        pers_featureset.append((feature, 'personal'))
    return ad_featureset, pers_featureset


# Create test and training data
def createTestTrainDataset():
    posCutoff = int(math.floor(len(ad_featureset) * 3 / 4))
    negCutoff = int(math.floor(len(pers_featureset) * 1 / 4))
    training_set = ad_featureset[:posCutoff] + pers_featureset[:negCutoff]
    testing_set = ad_featureset[posCutoff:] + pers_featureset[negCutoff:]
    return training_set, testing_set


def buildClassifier(training_set, testing_set):
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    accuracy = nltk.classify.accuracy(classifier, testing_set)  # calculates accuracy of the classifier
    print accuracy
    # precision and recall claculation
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    
    for i, (feats, label) in enumerate(testing_set):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
    
    print 'personal precision:', precision(refsets['personal'], testsets['personal'])
    print 'personal recall:', recall(refsets['personal'], testsets['personal'])
    print 'personal F-measure:', f_measure(refsets['personal'], testsets['personal'])
    print 'ad precision:', precision(refsets['ad'], testsets['ad'])
    print 'ad recall:', recall(refsets['ad'], testsets['ad'])
    print 'ad F-measure:', f_measure(refsets['ad'], testsets['ad'])
    return classifier


# read the training data and tokenize them into words
for line in codecs.open("Diabetes-Ad.txt", encoding='latin1'):
    ad_words.extend(tokenize(line))
for line in codecs.open("Diabetes-Personal.txt", encoding='latin1'):
    pers_words.extend(tokenize(line))

# fetch top 3000 relevant words
word_features = get_best_features(ad_words, pers_words)

# generate personal and advertisement feature set (words included in best 3000 words)
ad_featureset, pers_featureset = generateFeatureSet(word_features)

# Split the features into train and test data
training_set, testing_set = createTestTrainDataset()

# Build Naive Bayes classifier and save the classifier as Pickle object
classifier = buildClassifier(training_set, testing_set)
classifier_file = open("naiveBayes.pickle", "wb")
pickle.dump(classifier, classifier_file)
classifier_file.close()
