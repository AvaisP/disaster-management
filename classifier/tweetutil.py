import re
from string import punctuation

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpPXx/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpPxX/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

username_string = r"""(?:@[\w_]*\:?)"""

hashedtag_string = r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""

url_string = r"""https?://.*[\s]*"""

html_string = r"""(&\w+;)"""

escape_string = r"""(?:ESCOMMA|ESRETURN)"""

textinbrkt_string = r"""(?:\[.*\]|\(.*\))"""

def remove_stop_words(tweets):
    tokens = tweets.split();
    tokens = [t for t in tokens if t not in ['a', 'an', 'the']]
    return ' '.join(tokens)

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def attach_negation(tokens):
    # attach
    i = 0
    while i < len(tokens):
        if tokens[i] == 'no' or tokens[i] == 'not':
            if i == 0:
                tokens[i+1] = tokens[i] + '+' + tokens[i+1]
            elif i == len(tokens) - 1:
                tokens[i-1] = tokens[i-1] + '+' + tokens[i]
            else:
                tokens[i+1] = tokens[i] + '+' + tokens[i+1]
                tokens[i-1] = tokens[i-1] + '+' + tokens[i]
        i += 1
    # delete original
    new_tokens = [t for t in tokens if t not in ['no','not']]

    return new_tokens
	
def tweet_cleaning(tweet):
    # remove url
    clean_tweet = re.sub(url_string, '', tweet)
    # remove hashed tag
    clean_tweet = re.sub(hashedtag_string, '', clean_tweet)
    # remove username reference
    clean_tweet = re.sub(username_string, '', clean_tweet)
    # remove html
    clean_tweet = re.sub(html_string, '', clean_tweet)
    # remove escape placeholder
    clean_tweet = re.sub(escape_string, ' ,', clean_tweet)
    # remove brackets
    clean_tweet = re.sub(textinbrkt_string, '', clean_tweet)
    # remove non-ascii characters
    clean_tweet = removeNonAscii(clean_tweet)
    # remove emoticon
    clean_tweet = re.sub(emoticon_string, ' ', clean_tweet)
    # remove RT
    clean_tweet.replace('RT', ' ')
    # remove punctuation
    clean_tweet = "".join(c for c in clean_tweet if c not in punctuation)
    # remove duplicate whitespace
    clean_tweet = " ".join(clean_tweet.split())
    # remove stop words
    clean_tweet = remove_stop_words(clean_tweet)
	
    return clean_tweet

def get_bigram_bag(tweet):
    clean_tweet = tweet_cleaning(tweet)
    
    # tokenize
    tokens = clean_tweet.lower().split()

    bigrams = []
    if len(tokens) > 1:
        # attach negation
        tokens = attach_negation(tokens)
        
        i = 0
        while i < len(tokens) - 1:
            bigram = tokens[i] + ' ' + tokens[i+1]
            bigrams.append(bigram)
            i += 1

    return bigrams
