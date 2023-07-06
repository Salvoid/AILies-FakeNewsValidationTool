import gui_module as guiModule # Software GUI
import fetcher_module as fetcherModule # Post Fetcher
import process_module as processModule # Main Software Processes
import other_module as otherModule # Other needed functions
import pandas as pd # For Dataset Manipulation
import os # Miscellaneous Operating System Interfaces


def main():
    setup_initial()

    tkgui_window = guiModule.display_widget_main(process_urlcontent)
    guiModule.set_widget_options(tkgui_window)

def process_urlcontent(in_socialMedia, in_url):
    # processStatus
        # None --> Unknown Error Occured
        # *0 --> Success
        # *1 --> URL Field is Empty
        # *2 --> Wrong URL Format Length
        # *3 --> No Social Media selected
        # *4 --> URL Format Doesn't Match Twitter Tweet URL Format
        # *5 --> URL Format Doesn't Match Facebook Post URL Format
        # *6 --> Correct Twitter Tweet URL
        # *7 --> Correct Text/Image Facebook Post URL
        # *8 --> Group Facebook Post
        # *9 --> Video Facebook Post
        # 10 --> Twitter Tweet doesn't Exist
        # 11 --> Facebook Post doesn't Exist
        # 12 --> Twitter Tweet Fetch Failed
        # 13 --> Facebook Post Fetch Failed
    processStatus = None
    urlContentValidation = None

    processStatus = otherModule.check_url(in_socialMedia, in_url)

    if (processStatus==6):
        guiModule.print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        guiModule.print_console(False, True, "Requesting Content from Twitter...", 'textTag_process')
        tweet_html = fetcherModule.fetch_tweet(in_url)
        if (not tweet_html==None): # Check if Twitter Tweet Exists
            guiModule.print_console(True, False, "Content Fetch Status: ", 'textTag_task')
            guiModule.print_console(False, True, "Fetching Content...", 'textTag_process')
            try: # Try fetching Twitter Tweet content
                guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                guiModule.print_console(False, True, "Cleaning Content...", 'textTag_process')
                tweet_content = fetcherModule.clean_tweet_content(tweet_html)
                guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                guiModule.print_console(False, True, "Validating Content...", 'textTag_process')
                urlContentValidation = check_validity(tweet_content, "twitter")[0]
                processStatus = 0
            except: # If fetching Twitter Tweet content failed
                processStatus = 12
        else: # If Twitter Tweet doesn't Exist
            processStatus = 10
    elif (processStatus==7) or (processStatus==8) or (processStatus==9):
        guiModule.print_console(True, False, "Content Fetch Status: ", 'textTag_task')
        guiModule.print_console(False, True, "Requesting Content from Facebook...", 'textTag_process')
        fbpost_html = fetcherModule.fetch_fbpost(in_url)
        if (not fbpost_html==None): # Check if Facebook Post Exists
            guiModule.print_console(True, False, "Content Fetch Status: ", 'textTag_task')
            guiModule.print_console(False, True, "Fetching Content...", 'textTag_process')
            try: # Try fetching Facebook Post content
                if (processStatus==7):
                    guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                    guiModule.print_console(False, True, "Cleaning Content...", 'textTag_process')
                    fbpost_content = fetcherModule.clean_fbpost_content(fbpost_html, "posts")
                    guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                    guiModule.print_console(False, True, "Validating Content...", 'textTag_process')
                    urlContentValidation = check_validity(fbpost_content, "facebook")[0]
                elif (processStatus==8):
                    guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                    guiModule.print_console(False, True, "Cleaning Content...", 'textTag_process')
                    fbpost_content = fetcherModule.clean_fbpost_content(fbpost_html, "groups")
                    guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                    guiModule.print_console(False, True, "Validating Content...", 'textTag_process')
                    urlContentValidation = check_validity(fbpost_content, "facebook")[0]
                elif (processStatus==9):
                    guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                    guiModule.print_console(False, True, "Cleaning Content...", 'textTag_process')
                    fbpost_content = fetcherModule.clean_fbpost_content(fbpost_html, "videos")
                    guiModule.print_console(True, False, "Content Validation Status: ", 'textTag_task')
                    guiModule.print_console(False, True, "Validating Content...", 'textTag_process')
                    urlContentValidation = check_validity(fbpost_content, "facebook")[0]
                processStatus = 0
            except: # If fetching Facebook Post content failed
                processStatus = 13
        else: # If Facebook Post doesn't Exist
            processStatus = 11

    return processStatus, urlContentValidation

def setup_initial():
    model_naivebayes_multinomial_twitter_exist = os.path.exists(otherModule.define_relativepath(True,"assets\\training\\model_naivebayes_multinomial_twitter.pickle"))
    cv_countVect_twitter_exist = os.path.exists(otherModule.define_relativepath(True,"assets\\training\\cv_countVect_twitter.pickle"))
    tf_tfidfTransformer_twitter_exist = os.path.exists(otherModule.define_relativepath(True,"assets\\training\\tf_tfidfTransformer_twitter.pickle"))
    model_naivebayes_multinomial_facebook_exist = os.path.exists(otherModule.define_relativepath(True,"assets\\training\\model_naivebayes_multinomial_facebook.pickle"))
    cv_countVect_facebook_exist = os.path.exists(otherModule.define_relativepath(True,"assets\\training\\cv_countVect_facebook.pickle"))
    tf_tfidfTransformer_facebook_exist = os.path.exists(otherModule.define_relativepath(True,"assets\\training\\tf_tfidfTransformer_facebook.pickle"))

    if (not model_naivebayes_multinomial_twitter_exist) and (not cv_countVect_twitter_exist) and (not tf_tfidfTransformer_twitter_exist):
        # Import Training Dataset for Twitter
        df_dataset_wordset = processModule.import_dataset("twitter")
        # Training Twitter Model
        cv_countVect_twitter, tf_tfidfTransformer_twitter, model_naivebayes_multinomial_twitter = process_training(df_dataset_wordset)
        # Save Twitter Model, Count Vector Object, and Transformer Object to Directory
        processModule.save_training(model_naivebayes_multinomial_twitter, cv_countVect_twitter, tf_tfidfTransformer_twitter, "twitter")

    if (not model_naivebayes_multinomial_facebook_exist) and (not cv_countVect_facebook_exist) and (not tf_tfidfTransformer_facebook_exist):
        # Import Training Dataset for Facebook
        df_dataset_wordset = processModule.import_dataset("facebook")
        # Training Facebook Model
        cv_countVect_facebook, tf_tfidfTransformer_facebook, model_naivebayes_multinomial_facebook = process_training(df_dataset_wordset)
        # Save Facebook Model, Count Vector Object, and Transformer Object to Directory
        processModule.save_training(model_naivebayes_multinomial_facebook, cv_countVect_facebook, tf_tfidfTransformer_facebook, "facebook")

def check_validity(in_content, in_socialMedia):
    if in_socialMedia == "twitter":
        # Load Twitter Model, Count Vector Object, and Transformer Object to Directory
        model_naivebayes_multinomial_twitter, cv_countVect_twitter, tf_tfidfTransformer_twitter = processModule.load_training("twitter")
        # Predict using Twitter Model
        y_dataset_prediction = process_testing(in_content, model_naivebayes_multinomial_twitter, cv_countVect_twitter, tf_tfidfTransformer_twitter)
    elif in_socialMedia == "facebook":
        # Load Facebook Model, Count Vector Object, and Transformer Object to Directory
        model_naivebayes_multinomial_facebook, cv_countVect_facebook, tf_tfidfTransformer_facebook = processModule.load_training("facebook")
        # Predict using Facebook Model
        y_dataset_prediction = process_testing(in_content, model_naivebayes_multinomial_facebook, cv_countVect_facebook, tf_tfidfTransformer_facebook)
    
    return y_dataset_prediction

def process_training(in_df_dataset_wordset):
    # Training Dataset Preprocessing
    df_dataset_wordset_train = pd.DataFrame(
        {
            'True Values': in_df_dataset_wordset.iloc[:, 0], 
            'Content': in_df_dataset_wordset.iloc[:, 1]
        }
    )
    df_dataset_wordset_train.reset_index(drop=True, inplace=True) # Reset Dataframe Indexing without adding New Index Column

    # Training Dataset Text Cleansing
    content_count = 0
    for df_dataset_wordset_train_content in df_dataset_wordset_train.iloc[:, 1]:
        df_dataset_wordset_train_content = otherModule.clean_characters(df_dataset_wordset_train_content)
        df_dataset_wordset_train.iloc[content_count, 1] = otherModule.clean_string(df_dataset_wordset_train_content)
        content_count += 1

    # Prepare Training Dataset
    cv_countVect, tf_tfidfTransformer, X_dataset_train_tfidf, y_dataset_train_values = processModule.process_dataset_train(df_dataset_wordset_train)

    # Training Model
    model_naivebayes_multinomial = processModule.train_model(X_dataset_train_tfidf, y_dataset_train_values)

    return cv_countVect, tf_tfidfTransformer, model_naivebayes_multinomial

def process_testing(in_content, in_model_naivebayes_multinomial, in_cv_countVect, in_tf_tfidfTransformer):
    # Testing Dataset Preprocessing
    df_dataset_wordset_test = pd.DataFrame(
        {
            'True Values': [None], 
            'Content': [in_content]
        }
    )

    # Prepare Testing Dataset
    X_dataset_test_tfidf, y_dataset_test_values = processModule.process_dataset_test(in_cv_countVect, in_tf_tfidfTransformer, df_dataset_wordset_test)

    # Predicting Using Model
    y_dataset_prediction = processModule.predict_model(in_model_naivebayes_multinomial, X_dataset_test_tfidf)

    return y_dataset_prediction


if __name__ == "__main__":
    main()
