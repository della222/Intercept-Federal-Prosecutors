import os
from google.cloud import storage
from dotenv import load_dotenv


# get list of misconduct words
def get_misconduct_words(file):
    with open(file) as f:
        keywords = f.readlines()
    keywords = [word.strip('\n') for word in keywords]
    return keywords


# gets decision text from gcs
def pull_text_from_gcs(circuit, decision):
    credentials = os.getenv("credentials")
    storage_client = storage.Client.from_service_account_json(credentials)
    blobs = storage_client.list_blobs("intercept", prefix=f"texts/{circuit}/{decision}/{decision}.txt")
    blob_list = [i for i in blobs]
    text = blob_list[0].download_as_string().decode("utf-8") 
    return text


# takes in a decision txt file and finds keywords for misconduct/non-misconduct
# returns number of keywords mentioned
def find_misconduct_count(decision, words):
    count = 0
    for word in words:
        if word in decision:
            count += 1
    return count



if __name__ == "__main__":
    load_dotenv(override=True)
    circuit = 'ca6'
    decision = '09-06234'

    # keywords for misconduct
    misconduct_words = get_misconduct_words('misconduct_words.txt')
    # keywords against misconduct
    no_misconduct_words = get_misconduct_words('no_misconduct_words.txt')
    # get example of decision
    decision_text = pull_text_from_gcs(circuit, decision)

    print(decision)
    print('Number of Misconduct Words:')
    print(find_misconduct_count(decision_text, misconduct_words))
    print('Number of No Misconduct Words:')
    print(find_misconduct_count(decision_text, no_misconduct_words))