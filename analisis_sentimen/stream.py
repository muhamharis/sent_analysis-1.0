from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from nltk.tokenize import WordPunctTokenizer
import json
import re
import sentiment_mod as s

# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = "-"
asecret = ""


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        if 'extended_tweet' in all_data:
            if 'retweeted_status' in all_data:
                tweet = all_data['retweeted_status']['full_text']
            else:
                tweet = all_data['extended_tweet']['full_text']
        else:
            tweet = all_data['text']
        cleaned_tweets = clean_tweets(tweet)
        sentiment_value = s.sentiment(cleaned_tweets)
        print(cleaned_tweets, sentiment_value)

        output = open("twitter-out.txt", "a")
        output.write(sentiment_value)
        output.write('\n')
        output.close()
        return True

    def on_error(self, status):
        print(status)


def clean_tweets(tweet):
    rt_removed = re.sub('RT @[\w_]+: ', '', tweet)
    user_removed = re.sub(r'@[A-Za-z0-9]+', '', rt_removed)
    link_removed = re.sub('https?://[A-Za-z0-9./]+', '', user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet = number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    words = s.lemmatize_verbs(words)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, Listener(), tweet_mode='extended')
twitterStream.filter(track=["happy"], languages=["en"])
