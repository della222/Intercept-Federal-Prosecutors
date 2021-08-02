# Intercept-Federal-Prosecutors
A Nationwide Investigation for Federal Prosecutors

Code for BU Spark! Summer 2021

The code for this project relies on the Google Cloud Vision Api. To install and get started with it, please follow steps 1-6 in this codelab for the API. Use this link to set up the API Authentication Key and save it to your computer (and be sure to set the path as an environment variable using a .env file): https://cloud.google.com/vision/docs/libraries 

## Run in this order: (Date last scraped: July 14)
    1. ScrapeDecisions.py: Submits GET requests to API to find all new cases on appellate court website and saves their PDF links in a spreadsheet called NewCases.csv 
    2. download_pdfs_v2.py: Downloads all PDFs from NewCases.csv and uploads to GCS (~50 minutes for 6,000 cases)
    3. FilterDecisions.py: Extracts all text from PDFs using Vision API, saves text if and only if it mentions prosecutorial misconduct and saves a copy of the NewCases spreadsheet with only the cases that had mentions. (14 hr for ~6000 cases)
    4. FindDecisionKeywords.py: Checks the text of all cases given by a spreadsheet for certain keywords and adds score columns based on the frequency of certain keywords.
