from tweetutil import *
from classifier.models import Positive, Negative
from decimal import *
import math

small_number = Decimal(10e-7)
threshold = Decimal(0.8)

def get_log_prob(feature):
    if feature.freq > 0:
        return feature.get_prob().ln() / Decimal(math.log(2))
    else:
        return Decimal(small_number).ln() / Decimal(math.log(2))

def get_prob(feature):
    if feature.freq > 0:
        return feature.get_prob()
    else:
        return Decimal(small_number)

def get_salience(p_feature, n_feature):
    return Decimal(1) - min(get_prob(p_feature), get_prob(n_feature)) / max(get_prob(p_feature), get_prob(n_feature))

def get_pos_feature(b):
    try:
        p_feature = Positive.objects.get(bigram=b)
    except Positive.DoesNotExist:
        p_feature = Positive(bigram=b, freq=0)
    return p_feature

def get_neg_feature(b):
    try:
        n_feature = Negative.objects.get(bigram=b)
    except Negative.DoesNotExist:
        n_feature = Negative(bigram=b, freq=0)
    return n_feature

def get_bigram_log_likelihood(bigrams):
    p_likelihood = 0
    n_likelihood = 0
    for b in bigrams:
        p_feature = get_pos_feature(b)     
        n_feature = get_neg_feature(b)
        if get_salience(p_feature, n_feature) > threshold:
            p_likelihood += get_log_prob(p_feature)
            n_likelihood += get_log_prob(n_feature)
    return p_likelihood, n_likelihood

def tagger(tweet):
    bigrams = get_bigram_bag(tweet)
    p_likelihood, n_likelihood = get_bigram_log_likelihood(bigrams)
    if p_likelihood < n_likelihood:
        return -1, p_likelihood, n_likelihood
    elif p_likelihood > n_likelihood:
        return 1, p_likelihood, n_likelihood
    else:
        return 0, p_likelihood, n_likelihood

def get_tag_string(tag):
    if tag == -1:
        return 'Negative'
    elif tag == 1:
        return 'Positive'
    else:
        return 'Maybe neutral'
	
