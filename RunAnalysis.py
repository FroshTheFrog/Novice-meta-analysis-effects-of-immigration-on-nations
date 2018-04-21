import matplotlib.pyplot as plt
import os

#reads a file and returns its contents
#string -> list of list of string
def readFile(filename):

    #open the file in the relative path
    scriptDir = os.path.dirname(__file__) #<-- absolute dir the script is in
    filename = os.path.join(scriptDir, filename)

    file = open(filename)
    data = []
    for line in file:
        data.append(line.split(","))
    file.close()
    return data

#returns if the given string can be cast to a float
#string -> bool
def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

#return a dictionary containing the country names as a
#key and their code as the value
#null -> dictionary
def getCountryCodes():

    data = readFile("countryCodes.txt")

    #remove the header
    data = data[2:len(data)]

    MyDic = {}

    for line in data:
        code = line[7]
        MyDic[line[2]] = code

    return MyDic

#breaks some world bank data into a readable formate
#this is a dictionary of dictionary where
#the key is contry code for the first one
#and the date is the code for the second one
#data start is the index of where the data start to be looked at
#list of list of string, int -> dictionary of dictionaries
def interpretWorldBankData(data, dateStart):

    #have to look up the country codes because not all the codes are in the same place in the data set
    countrycodes = getCountryCodes()

    #get a list of dates the dates that are used
    dates = data[4][dateStart:len(data[4])]

    #remove the data top rows
    data = data[5:len(data)]

    #the dictionary filled with the data
    dataDic = {}

    for line in data:
        country = line[0]
        country = country.strip("\"") #remove the quotes
        
        if country in countrycodes:
            key = countrycodes[country]
            dataDic[key] = {}
        else:
            continue


        for num in range(len(dates)):
            value = line[num + dateStart].strip("\"").strip("\n")
            if RepresentsFloat(value):
                dataDic[key][dates[num].strip("\"")] = float(value)

                
    return dataDic

#breaks the homicides per capita data into a readable formate
#this is a dictionary of dictionary where
#the key is contry code for the first one
#and the date is the code for the second one
#list of list of string -> dictionary of dictionaries
def interpretHomicides(data):
    countrycodes = getCountryCodes()

    #remove header
    del data[0]

    dataDic = {}

    for line in data:

        #remove the quotes
        country = line[0].strip("\"")
        
        if country in countrycodes:
            key = countrycodes[country]
            if not key in dataDic:
                dataDic[key] = {}
            dataDic[key][line[1].strip("\"")] = float(line[2].strip("\""))

    return dataDic

#breaks the international migration data into a readable formate
#this is a dictionary of dictionary where the 
#key is contry code for the first one
#and the date is the code for the second one
#this data set was taken from the xls version 
#of the data and then converted into a .csv
#list of list of string -> dictionary of dictionaries
def interpretMigration(data):

    #save the dates that correspond to each value
    dates = data[0]

    countrycodes = getCountryCodes()

    del data[0]
    
    dataDic = {}

    for line in data:

        key = line[0]

        key = countrycodes[key]
        
        dataDic[key] = {}

        for num in range(len(dates)):
            dataDic[key][dates[num].strip("\n")] = float(line[num+2])

    return dataDic

#break data that follow the basic fromat into a readable formate
#this is a dictionary of dictionary where 
#the key is contry code for the first one
#and the date is the code for the second one
#list of list of string -> dictionary of dictionaries
def interpret(data):

    #remove the header
    del data[0]

    dataDic = {}

    for line in data:
        if (line[0] != "Mexico" and line[0] != "Turkey"): #there are some issues with these countries data sets

            key = line[1]

            if not key in dataDic:
                dataDic[key] = {}
                
            value = line[3].strip("\n")

            dataDic[key][line[2]] = float(value)

    return dataDic

#normalize and convert to a percent given data for given a 
#dictionary of other values
#dictionary of dictionaries, dictionary of dictionaries -> 
#dictionary of dictionaries
def normalize(actOn, divideTo):

    newDic = {}

    for key in actOn:
        if not ("MEX" == key or "TUR" == key): #there are some issues with these countries data sets
            for secondKey in actOn[key]:

                if not key in newDic:
                    newDic[key] = {}

                newDic[key][secondKey] = (actOn[key][secondKey]/divideTo[key][secondKey]) * 100
    return newDic

#change a data set to the data set representing the change in a value
#this is meant to isolate the effect of immigration more
#dictionary of dictionaries -> dictionary of dictionaries
def changeToGrowth(dic):
    previousValue = "null"
    newDic = {}

    for key in dic:
        for secondKey in dic[key]:
            if previousValue != "null":

                if not key in newDic:
                    newDic[key] = {}

                #finding the percent does not work because some of the values are 0
                newDic[key][secondKey] = dic[key][secondKey] - previousValue

            previousValue = dic[key][secondKey]
        previousValue = "null"
    
    return newDic

#return the correlation between dictionaries
#using Pearson Correlation Coefficient
#dictionary dictionary -> float
def findCorrelation(dic1, dic2):

    #find the average values of each data set
    aveargeValue1 = 0
    aveargeValue2 = 0
    valueNum1 = 0
    valueNum2 = 0

    for value in dic1.values():
        for secondValue in value.values():
            aveargeValue1 += secondValue
        valueNum1 += len(value.values())

    for value in dic2.values():
        for secondValue in value.values():
            aveargeValue2 += secondValue
        valueNum2 += len(value.values())
    
    aveargeValue1 /= valueNum1
    aveargeValue2 /= valueNum2

    #find the Pearson Correlation Coefficient:
    topOfEquation = 0
    bottomOfEquationOne = 0
    bottomOfEquationTwo = 0

    for key in dic1:
        for secondKey in dic1[key]:
            if key in dic2 and secondKey in dic2[key]:
                dicOneVariance = dic1[key][secondKey] - aveargeValue1
                dicTwoVariance = dic2[key][secondKey] - aveargeValue2

                topOfEquation += dicOneVariance * dicTwoVariance
                bottomOfEquationOne += dicOneVariance ** 2
                bottomOfEquationTwo += dicTwoVariance ** 2
    
    bottomOfEquation = (bottomOfEquationOne * bottomOfEquationTwo) ** .5

    if bottomOfEquation != 0:
        return topOfEquation / bottomOfEquation
    return 0

def main():

    #read in all the data and interpret it
    gdpGrowthData = interpretWorldBankData(readFile("gdpGrowth.csv"), 35)
    homicidesData = interpretHomicides(readFile("homicidesPerCapita.csv"))
    inequalityOfIncomesData = interpret(readFile("inequalityOfIncomes.csv"))
    lifeSatisfactionData = interpret(readFile("lifeSatisfaction.csv"))
    migrationData = interpretMigration(readFile("Migration.csv"))
    populationData = interpret(readFile("population.csv"))
    satisfiedPercentData = interpret(readFile("satisfiedPercent.csv"))
    socialSpendingData = interpret(readFile("socialSpending.csv"))
    unemploymentData = interpretWorldBankData(readFile("unemployment.csv"), 45)
    
    #normalize the data that is need
    migrationData = normalize(migrationData, populationData)

    #finds coraliton with the characteristics of
    #countries to have a lot of immigration
    #it does this by not attempted to isolate the effect of immigration
    gdpGrowthDataCorrelationCurrentState = findCorrelation(migrationData, 
    gdpGrowthData)
    homicidesCorrelationCurrentState = findCorrelation(migrationData, 
    homicidesData)
    inequalityOfIncomesCorrelationCurrentState = findCorrelation(migrationData, 
    inequalityOfIncomesData)
    lifeSatisfactionCorrelationCurrentState = findCorrelation(migrationData, 
    lifeSatisfactionData)
    satisfiedPercentCorrelationCurrentState = findCorrelation(migrationData, 
    satisfiedPercentData)
    socialSpendingCorrelationCurrentState = findCorrelation(migrationData, 
    socialSpendingData)
    unemploymentCorrelationCurrentState = findCorrelation(migrationData, 
    unemploymentData)

    CorrelationCurrentState = [gdpGrowthDataCorrelationCurrentState, 
    homicidesCorrelationCurrentState, 
    inequalityOfIncomesCorrelationCurrentState, 
    lifeSatisfactionCorrelationCurrentState, 
    satisfiedPercentCorrelationCurrentState, 
    socialSpendingCorrelationCurrentState,
    unemploymentCorrelationCurrentState]

    #change all the data to only measure the change of the value
    #this will allow for the analysis
    #to more effectively measure an effect of immigration,
    #without taking into account the current state
    gdpGrowthData = changeToGrowth(gdpGrowthData)
    homicidesData = changeToGrowth(homicidesData)
    inequalityOfIncomesData = changeToGrowth(inequalityOfIncomesData)
    lifeSatisfactionData = changeToGrowth(lifeSatisfactionData)
    satisfiedPercentData = changeToGrowth(satisfiedPercentData)
    socialSpendingData = changeToGrowth(socialSpendingData)
    unemploymentData = changeToGrowth(unemploymentData)
    migrationData = changeToGrowth(migrationData)

    gdpGrowthCorrelation = findCorrelation(migrationData, gdpGrowthData)
    homicidesCorrelation = findCorrelation(migrationData, homicidesData)
    inequalityOfIncomesCorrelation = findCorrelation(migrationData, 
    inequalityOfIncomesData)
    lifeSatisfactionCorrelation = findCorrelation(migrationData, 
    lifeSatisfactionData)
    satisfiedPercentCorrelation = findCorrelation(migrationData, 
    satisfiedPercentData)
    socialSpendingCorrelation = findCorrelation(migrationData, 
    socialSpendingData)
    unemploymentCorrelation = findCorrelation(migrationData, 
    unemploymentData)

    Correlation = [gdpGrowthCorrelation, 
    homicidesCorrelation, 
    inequalityOfIncomesCorrelation, 
    lifeSatisfactionCorrelation, 
    satisfiedPercentCorrelation, 
    socialSpendingCorrelation, 
    unemploymentCorrelation]

    #plot the bar charts
    xAxis = ["GDP Growth", "Homicides", "Inequality Of Incomes", 
    "Life Satisfaction", "Satisfied Percent", "Social Spending", "Unemployment"]

    #(having trouble keeping everything under 80 chars)
    title = "Correlation between immigration"
    title += " increases and variable in countries changes"
    
    plt.title(title)
    plt.bar(xAxis, Correlation)
    plt.show()

    plt.title("Correlation between immigration and societal characteristics")
    plt.bar(xAxis, CorrelationCurrentState)
    plt.show()

main()