# [Imports]====================================================================================================
from genericpath import exists
import os # Miscellaneous Operating System Interfaces
import sys # System-specific Parameters & Functions
import re # Regular Expressions
import string # String
import nltk # Natural Language Toolkit for Natural Language Processing
from nltk.corpus import stopwords # Stopwords for removing them
from nltk.tokenize import word_tokenize # Tokenize string/sentences into word arrays


# [Functions]====================================================================================================
# [Defines the relative path from the absolute path of local files.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def define_relativepath(in_toCreate, in_path_relative):
    try:
        # path_base = sys._MEIPASS
        # path_base = getattr(sys, '_MEIPASS', os.getcwd())
        path_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        path_base = os.path.abspath(".")
    
    return path_base + in_path_relative

# [Import Text Files to Array.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def import_text(in_path):
    out_text_array = []
    with open(define_relativepath(False,in_path), 'r', encoding="utf8") as file:
        temp_text_array = file.readlines()
        for temp_text in temp_text_array:
            out_text_array.append(temp_text.replace('\n', ''))
    
    return out_text_array

# [Declarations & Initializations]====================================================================================================
xmlhtml_charEntities = import_text("\\assets\\textcleansing\\xmlhtml_charEntities.txt") # Import XML/HTML Character Entities for referencing
english_stopWords = set(stopwords.words('english')) # Set English Stopwords Words for referencing
english_wholeWords = set(nltk.corpus.words.words()) # Set English Whole Words for referencing
tagalog_stopWords = import_text("\\assets\\textcleansing\\tagalog_stopWords.txt") # Import Tagalog Stopwords Words for referencing
tagalog_wholeWords = import_text("\\assets\\textcleansing\\tagalog_wholeWords.txt") # Import Tagalog Whole Words for referencing

# [Functions]====================================================================================================
# [Remove New Lines from Strings.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def remove_newline(in_string):
    return in_string.replace('\n', ' ')

# [Remove Unwanted Characters from Strings.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def clean_characters(in_string):
    # Remove Non UTF-8 Characters
    out_string_object = in_string.encode('utf-8', errors='ignore')
    out_string = out_string_object.decode('utf-8')

    # Remove Non ASCII Characters
    ascii_chars = set(string.printable)
    out_string = ''.join(filter(lambda x: x in ascii_chars, out_string))

    # Remove XML/HTML ASCII Characters
    out_string = re.sub(r'&#([0-1]?[0-9]?[0-9]|[2][0-5][0-9]|[2][5][0-5]);', '', out_string) # Remove "&#0;" - "&#255;"
    
    # Remove XML/HTML Character Entities
    for xmlhtml_charEntity in xmlhtml_charEntities:
        out_string = out_string.replace(xmlhtml_charEntity, '')
    
    return out_string

# [Clean Strings based on Dictionaries.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def clean_string(in_string):
    # Convert all Uppercase Letters to Lowercase Letters
    out_string = in_string.lower()

    # Accepts only words that are (Alphabetical) and is (part of the English Dictionary that is not an English Stop Word) or is (part of the Filipino Dictionary that is not a Filipino Stop Word)
    out_string_wordTokens = word_tokenize(out_string) # Tokenize string/sentences into word arrays
    temp_wordTokens = []
    for out_string_word in out_string_wordTokens:
        if (out_string_word.isalpha()) and (
            ((out_string_word not in english_stopWords) and (out_string_word in english_wholeWords)) or 
            ((out_string_word not in tagalog_stopWords) and (out_string_word in tagalog_wholeWords))
        ):
            temp_wordTokens.append(out_string_word)
    out_string = ' '.join(temp_wordTokens)

    return out_string

# [Prepare Twitter String for HTML Tag Removal.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def prepare_html_twitter(in_string):
    out_string = in_string.replace('</blockquote>', '<blockquote>')
    out_string = out_string.replace('</p>', '<p>')

    return out_string

# [Remove HTML Tags from Twitter Strings.](https://stackoverflow.com/a/27801023)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def remove_html_twitter(in_string):
    # replace <tag>...</tag>, possibly more than once
    done = False
    while not done:
        temp = re.sub(r'<([^/]\S*)[^>]*>[\s\S]*?</\1>', '', in_string)
        done = temp == in_string
        in_string = temp
    # replace remaining standalone tags, if any
    in_string = re.sub(r'<[^>]*>', '', in_string)
    in_string = re.sub(r'\s{2,}', ' ', in_string)
    
    return in_string.strip()

# [Remove Twitter Characters from Strings.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def remove_characters_twitter(in_string):
    # Remove Twitter Username Signature After A Tweet by finding the last occurrence of the "&mdash;"(Em dash/Mutton dash) character
    out_string = re.sub(r'&mdash;(?:.(?!&mdash;))+$', '', in_string)

    return out_string

# [Remove HTML Tags from Facebook Strings.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def remove_html_facebook(in_string, in_fbpost_type):
    if in_fbpost_type == "posts": # Match for Posts only
        in_string = re.search(r'(?<=_3576)(.*)(?=_3x-2)', in_string)
        in_string = re.search(r'(?<=<p>)(.*)(?=</p>)', in_string.group())
        out_string = in_string.group()
    elif in_fbpost_type == "groups": # Match for Group Posts
        in_string = re.search(r'(?<=og:image:alt" content=")(.*)(?=" /><meta property="og:locale)[\s\S]', in_string)
        out_string = in_string.group()
    elif in_fbpost_type == "videos": # Match for Video Posts
        in_string = re.search(r'(?<="title":")(.*)(?=\\u00b7)[\s\S]', in_string)
        out_string = in_string.group()

    return out_string

def check_url(in_socialMedia, in_url):
    # processStatus
        # None --> Unknown Error Occured
        # 0 --> Success
        # 1 --> URL Field is Empty
        # 2 --> Wrong URL Format Length
        # 3 --> No Social Media selected
        # 4 --> URL Format Doesn't Match Twitter Tweet URL Format
        # 5 --> URL Format Doesn't Match Facebook Post URL Format
        # 6 --> Correct Twitter Tweet URL
        # 7 --> Correct Text/Image Facebook Post URL
        # 8 --> Group Facebook Post
        # 9 --> Video Facebook Post
        # *10 --> Twitter Tweet doesn't Exist
        # *11 --> Facebook Post doesn't Exist
        # *12 --> Twitter Tweet Fetch Failed
        # *13 --> Facebook Post Fetch Failed
    
    if in_url == "": # If url is empty
        return 1

    in_url = in_url.lower()
    url_parts = in_url.split('/')
    # Twitter Tweets
        # in_socialMedia --> "Twitter"
            # url_parts[0] --> "http" / "https"
            # url_parts[1] --> ""
            # url_parts[2] --> "www.twitter.com"/"twitter.com"
            # url_parts[3] --> (Twitter User)
            # url_parts[4] --> "status"
            # url_parts[5] --> (Tweet Number)
            # url_parts[6-*] --> (Others)
            # https://twitter.com/FabrizioRomano/status/1671449786099040256
    # Facebook Posts
        # in_socialMedia --> "Facebook"
            # url_parts[0] --> "http" / "https"
            # url_parts[1] --> ""
            # url_parts[2] --> "www.facebook.com"/"facebook.com"
            # Text/Image Facebook Post
                # url_parts[3] --> (Facebook User)
                    # url_parts[4] --> "posts"
                    # url_parts[5] --> (Facebook Post Number)
                    # url_parts[6-*] --> (Others)
                    # https://www.facebook.com/facebook/posts/pfbid0uESe8tVgfsapK9hNEvcjLVcZWVdeZLksKmW6FudfUMwuERzd8Qyn5Panzazk2Pq4l
            # Group Facebook Post
                # url_parts[3] --> "groups"
                    # url_parts[4] --> (Facebook Group Number)
                    # url_parts[5] --> "posts"
                    # url_parts[6] --> (Facebook Post Number)
                    # url_parts[7-*] --> (Others)
                    # https://www.facebook.com/groups/238372536862155/posts/1231351064230959/
            # Video Facebook Post
                # url_parts[3] --> (Facebook Group)
                    # url_parts[4] --> "videos"
                    # url_parts[5] --> (Facebook Post Short Description)
                    # url_parts[6] --> (Facebook Post Number)
                    # url_parts[7-*] --> (Others)
                    # https://www.facebook.com/memes/videos/that-mustve-hurt-via-leraisterica-patasvantner/7123558154325356/

    if (
        (len(url_parts) >= 6) and 
        (
            (url_parts[0]=="http:") or 
            (url_parts[0]=="https:")
        ) and 
        (url_parts[1]=="")
    ): # Check if it fits the required url length and has the "http"/"https" extension
        if in_socialMedia == "Twitter": # Match for Twitter Tweets only
            if (
                (
                    (url_parts[2]=="www.twitter.com") or 
                    (url_parts[2]=="twitter.com")
                ) and 
                (not url_parts[3]=="") and 
                (url_parts[4]=="status") and 
                (not url_parts[5]=="")
            ): # Check if it fits the required url format for a Twitter Tweet
                return 6
            else: # If it doesn't fits the required url format for a Twitter Tweet
                return 4
        elif in_socialMedia == "Facebook": # Match for Facebook Posts only
            if (
                (url_parts[2]=="www.facebook.com") or 
                (url_parts[2]=="facebook.com")
            ): # Check if it fits the required url format for a Facebook Post
                if (
                    (url_parts[3]=="groups") and 
                    (not url_parts[4]=="") and 
                    (url_parts[5]=="posts") and 
                    (not url_parts[6]=="")
                ): # Group Facebook Post
                    return 8
                elif (not url_parts[3]==""): # Text/Image Facebook Post or Video Facebook Post
                    if (
                        (url_parts[4]=="posts") and 
                        (not url_parts[5]=="")
                    ): # Text/Image Facebook Post
                        return 7
                    elif (
                        (url_parts[4]=="videos") and 
                        (not url_parts[5]=="") and 
                        (not url_parts[6]=="")
                    ): # Video Facebook Post
                        return 9
                    else: # If it doesn't fits the required url format for a Facebook Post
                        return 5
                else: # If it doesn't fits the required url format for a Facebook Post
                    return 5
            else: # If it doesn't fits the required url format for a Facebook Post
                return 5
        else: # If no Social Media selected
            return 3
    else: # If url does not fits the required url length and has no "http"/"https" extension
        return 2
