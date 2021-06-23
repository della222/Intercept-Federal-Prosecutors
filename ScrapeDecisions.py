import json
import requests
from datetime import datetime, timedelta


def query(circuit, year):
    return requests.get(f'https://www.govinfo.gov/wssearch/rb//uscourts/appellate/{circuit}/{year}?fetchChildrenOnly=1&offset=0')


def getNewCases(response, startingDate):

    # create dictionary where key is the title of a decision and value is a list contianing the case date and pdf link
    allCases = {}
    for i in range(len(response['childNodes'])):
        date = response['childNodes'][i]['nodeValue']['publishdate']
        title = response['childNodes'][i]['nodeValue']['title']
        pdf = "https://www.govinfo.gov/content/pkg/" + response['childNodes'][i]['nodeValue']['pdffile']
        allCases[title] = [date, pdf]

    # turn dates to datetime objects
    for case in allCases:
        date = allCases[case][0]
        dateObj = datetime.strptime(date, '%B %d, %Y')
        allCases[case][0] = dateObj

    # get cases past startingDate
    cases = {}
    for case in allCases:
        start = datetime.strptime(startingDate, '%B %d, %Y')
        if allCases[case][0] > start:
            cases[case] = allCases[case]

    for case in cases:
        print(case)
        print(cases[case])
        print()


circuit = "ca1"
year = "2021"
response = query(circuit, year).json()
getNewCases(response, 'March 1, 2021')

