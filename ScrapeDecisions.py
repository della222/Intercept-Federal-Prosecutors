import csv
import requests
from datetime import datetime, timedelta

# get json file of appellates based on circuit and year
def query(circuit, year):
    return requests.get(f'https://www.govinfo.gov/wssearch/rb//uscourts/appellate/{circuit}/{year}?fetchChildrenOnly=1&offset=0')


# get new appellates for a specific circuit after a specific starting date
def getNewCases(circuit, response, startingDate):

    # create a list contianing appellate info: title, circuit, date, case id, and pdf link
    allCases = []
    for i in range(len(response['childNodes'])):
        date = response['childNodes'][i]['nodeValue']['publishdate']
        title = response['childNodes'][i]['nodeValue']['title']
        if len(circuit) < 4:
            id = response['childNodes'][i]['nodeValue']['granuleid'][13:21]
        else:
            id = response['childNodes'][i]['nodeValue']['granuleid'][14:21]
        pdf = "https://www.govinfo.gov/content/pkg/" + response['childNodes'][i]['nodeValue']['pdffile']
        allCases.append([title, circuit, date, id, pdf])

    # turn dates to datetime objects
    for case in allCases:
        date = case[2]
        dateObj = datetime.strptime(date, '%B %d, %Y')
        case[2] = dateObj

    # get cases past startingDate
    cases = []
    for case in allCases:
        start = datetime.strptime(startingDate, '%B %d, %Y')
        if case[2] > start:
            cases.append(case)

    # turn dates back to string for readability
    for case in cases:
        case[2] = case[2].strftime("%B %d %Y")

    #for case in cases:
    #    print(case)
    #    print()

    return cases


# convert data to csv file
def convertCSV(cases_list):
    with open('newCases.csv', 'w') as f:
        csv.writer(f).writerows(cases_list)


# scrape all appellates in a circuit and return list of fields
def scrapeAll(circuit, year, startingDate):
    response = query(circuit, year).json()
    circuit_cases = getNewCases(circuit, response, startingDate)
    return circuit_cases


def main():
    year = "2021"
    startingDate = 'March 1, 2021'

    # list of all new cases
    all_new_cases = []

    # get appellates from circuits 1 - 11
    for i in range(1,12):
        circuit = "ca"+str(i)
        circuit_i_cases = scrapeAll(circuit, year, startingDate)
        all_new_cases += circuit_i_cases
    
    # get appellate from DC circuit and Federal circuit
    all_new_cases += scrapeAll('caDC', year, startingDate)
    all_new_cases += scrapeAll('ca13', year, startingDate)

    convertCSV(all_new_cases)


if __name__ == "__main__":
    main()
