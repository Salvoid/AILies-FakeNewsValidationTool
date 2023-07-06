import process_module as processModule # Main Software Processes
import other_module as otherModule # Other needed functions
import sys # System-specific Parameters & Functions
import pandas as pd # For Dataset Manipulation


def main():
    # Print console text to text file
    sys.stdout =  open(otherModule.define_relativepath(True,".\\output\\twitter_news_politics\\twitter_news_politics_console.txt"), 'w')

    # Import Dataset
    df_dataset_wordset = processModule.import_dataset("twitter")

    # Split Dataset
    import random
    randomInt = random.randint(0,100)
    testSize = 0.20
    df_dataset_wordset_train, df_dataset_wordset_test = processModule.train_test_split(df_dataset_wordset,test_size= testSize, random_state=randomInt)
    df_dataset_wordset_train.reset_index(drop=True, inplace=True) # Reset Dataframe Indexing without adding New Index Column
    df_dataset_wordset_test.reset_index(drop=True, inplace=True) # Reset Dataframe Indexing without adding New Index Column

    # Set Features and Target Values
    # Features = X_dataset = df_dataset_words.iloc[:,1] = word
    # Target = y_dataset = df_dataset_words.iloc[:,0] = label

    # Save Training and Testing Dataset BEFORE Text Cleansing
    df_dataset_wordset_train_raw = pd.DataFrame(
        {
            'True Values': df_dataset_wordset_train.iloc[:, 0], 
            'Content': df_dataset_wordset_train.iloc[:, 1]
        }
    )
    df_dataset_wordset_test_raw = pd.DataFrame(
        {
            'True Values': df_dataset_wordset_test.iloc[:, 0], 
            'Content': df_dataset_wordset_test.iloc[:, 1]
        }
    )
    df_dataset_wordset_train_raw.to_csv(".\\output\\twitter_news_politics\\twitter_news_politics_dataset_train_raw.csv")
    df_dataset_wordset_test_raw.to_csv(".\\output\\twitter_news_politics\\twitter_news_politics_dataset_test_raw.csv")

    # Training and Testing Dataset Text Cleansing
    content_count = 0
    for df_dataset_wordset_train_content in df_dataset_wordset_train.iloc[:, 1]:
        df_dataset_wordset_train_content = otherModule.clean_characters(df_dataset_wordset_train_content)
        df_dataset_wordset_train.iloc[content_count, 1] = otherModule.clean_string(df_dataset_wordset_train_content)
        content_count += 1
    content_count = 0
    for df_dataset_wordset_test_content in df_dataset_wordset_test.iloc[:, 1]:
        df_dataset_wordset_test_content = otherModule.clean_characters(df_dataset_wordset_test_content)
        df_dataset_wordset_test.iloc[content_count, 1] = otherModule.clean_string(df_dataset_wordset_test_content)
        content_count += 1

    # Prepare Training Dataset
    cv_countVect_twitter, tf_tfidfTransformer_twitter, X_dataset_train_tfidf, y_dataset_train_values = processModule.process_dataset_train(df_dataset_wordset_train)

    # Training Model
    model_naivebayes_multinomial_twitter = processModule.train_model(X_dataset_train_tfidf, y_dataset_train_values)

    # Save Twitter Model, Count Vector Object, and Transformer Object to Directory
    processModule.save_training(model_naivebayes_multinomial_twitter, cv_countVect_twitter, tf_tfidfTransformer_twitter, "twitter")

    # Load Twitter Model, Count Vector Object, and Transformer Object to Directory
    model_naivebayes_multinomial_twitter, cv_countVect_twitter, tf_tfidfTransformer_twitter = processModule.load_training("twitter")
    
    # Prepare Testing Dataset
    X_dataset_test_tfidf, y_dataset_test_values = processModule.process_dataset_test(cv_countVect_twitter, tf_tfidfTransformer_twitter, df_dataset_wordset_test)

    # Predicting Using Model
    y_dataset_prediction = processModule.predict_model(model_naivebayes_multinomial_twitter, X_dataset_test_tfidf)

    # Compute Accuracy
    processModule.compute_accuracy(y_dataset_test_values, y_dataset_prediction, ".\\output\\twitter_news_politics\\twitter_news_politics_cm.png")

    # Print Extra Details
    print("==================================================")
    print("Is Testing Dataset From Training Dataset: No")
    print("Training Dataset / Testing Dataset Percentage: ", 100-(100*testSize), "% :", 100*testSize, "%")
    print("Random Seed: ", randomInt)
    print("Training Dataset Number of Posts: ", len(df_dataset_wordset_train.index))
    print("Testing Dataset Number of Posts: ", len(df_dataset_wordset_test.index))
    print("==================================================")
    print("Testing Dataset ACTUAL Validity Values: \n", y_dataset_test_values.to_numpy())
    print("==================================================")
    print("Testing Dataset PREDICTION Validity Values: \n", y_dataset_prediction)
    print("==================================================")

    # Save Training and Testing Dataset AFTER Text Cleansing
    df_dataset_wordset_train_clean = pd.DataFrame(
        {
            'True Values': df_dataset_wordset_train.iloc[:, 0], 
            'Content': df_dataset_wordset_train.iloc[:, 1]
        }
    )
    df_dataset_wordset_test_clean_final = pd.DataFrame(
        {
            'True Values': y_dataset_test_values.to_numpy(), 
            'Predicted Values': y_dataset_prediction, 
            'Content': df_dataset_wordset_test.iloc[:, 1]
        }
    )
    df_dataset_wordset_train_clean.to_csv(".\\output\\twitter_news_politics\\twitter_news_politics_dataset_train_clean.csv")
    df_dataset_wordset_test_clean_final.to_csv(".\\output\\twitter_news_politics\\twitter_news_politics_dataset_test_clean.csv")


if __name__ == "__main__":
    main()
