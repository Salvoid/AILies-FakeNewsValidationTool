import requests
import other_module as otherModule # Other needed functions

def fetch_tweet(in_tweet_url):
    requests_url = 'https://publish.twitter.com/oembed?url=%s' % in_tweet_url
    response_tweet_page = requests.get(requests_url)
    tweet_html = None

    if response_tweet_page.status_code == 200:
        json_tweet_page = response_tweet_page.json()
        tweet_html = json_tweet_page['html']

    return tweet_html

def clean_tweet_content(in_tweet_html):
    tweet_html = otherModule.remove_newline(in_tweet_html)
    tweet_html = otherModule.prepare_html_twitter(tweet_html)
    out_tweet_content = otherModule.remove_html_twitter(tweet_html)
    out_tweet_content = otherModule.remove_characters_twitter(out_tweet_content)
    out_tweet_content = otherModule.clean_characters(out_tweet_content)
    out_tweet_content = otherModule.clean_string(out_tweet_content)

    return out_tweet_content

def fetch_fbpost(in_fbpost_url):
    response_fbpost_page = requests.get(in_fbpost_url)
    fbpost_html = None

    if response_fbpost_page.status_code == 200:
        fbpost_html = response_fbpost_page.text

    return fbpost_html

def clean_fbpost_content(in_fbpost_html, in_fbpost_type):
    fbpost_html = otherModule.remove_newline(in_fbpost_html)
    out_fbpost_content = otherModule.remove_html_facebook(fbpost_html, in_fbpost_type)
    out_fbpost_content = otherModule.clean_characters(out_fbpost_content)
    out_fbpost_content = otherModule.clean_string(out_fbpost_content)

    return out_fbpost_content
