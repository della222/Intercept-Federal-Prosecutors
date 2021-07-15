# Intercept-Federal-Prosecutors
A Nationwide Investigation for Federal Prosecutors

Code for BU Spark! Summer 2021

Run in this order: (Date last scraped: July 14)
    1. ScrapeDecisions.py: Sumbits GET Requests to API to find all new cases and save their PDF links in a spreadsheet called NewCases.csv 
    2. download_pdfs_v2.py: Downloads all PDFs from NewCases.csv and uploads to GCS (~50 minutes for 6,000 cases)
    3. FilterDecisions.py: Extracts all text from PDFs using Vision API, saves text if and only if it mentions prosecutorial misconduct and saves a copy of the NewCases spreadsheet with only the cases that had mentions. (14 hr for ~6000 cases)