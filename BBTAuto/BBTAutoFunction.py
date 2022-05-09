from audioop import findfactor
import math
import os, csv

def scanCSVFile(filePath):
    fileList = os.listdir(filePath)
    fileCSVList = []
    for i in fileList:
        if os.path.isdir(filePath + '/' + i):
            subdirPath = filePath + '/' + i
            subdirList = os.listdir(subdirPath)
            for j in subdirList:
                if (j.find('.CSV') != -1) or (j.find('.csv') != -1):
                    findFlag = False
                    for k in fileCSVList:
                        if k == j:
                            findFlag = True
                            break
                    if findFlag == False:
                        fileCSVList.append(j)
        else:
            if (i.find('.CSV') != -1) or (i.find('.csv') != -1):
                findFlag = False
                for j in fileCSVList:
                    if i == j:
                        findFlag = True
                        break
                if findFlag == False:
                    fileCSVList.append(i)
                    
    return fileCSVList

def scanTargetCSV(filePath, fileName):
    fileList = os.listdir(filePath)
    dataBuffer = []
    avgData = []
    varianceData = []
    standardData = []
    cutlineData = []
    filteredData = []

    for i in fileList:
        if os.path.isdir(filePath + '/' + i):
            subdirPath = filePath + '/' + i
            subdirList = os.listdir(subdirPath)
            for j in subdirList:
                if (j.find(fileName) != -1):
                    targetPath = subdirPath + '/' + j
                    print(targetPath)
                    collectData(targetPath, dataBuffer)
                    print('Complete!')
                    print(dataBuffer)
        else:
            if (i.find(fileName) != -1):
                targetPath = subdirPath + '/' + i
                print(targetPath)
                collectData(targetPath, dataBuffer)
                print('Complete!')
                print(dataBuffer)

    # Calculate Average #
    tempLabel = ''
    tempAvg = 0.0
    for i in range(0, len(dataBuffer[0])):
        for j in range(0, len(dataBuffer)):
            if(j == 0):
                tempLabel = dataBuffer[j][i]
            else:
                tempAvg += float(dataBuffer[j][i])
        tempAvg = tempAvg / (len(dataBuffer) - 1) 
        print(tempLabel, tempAvg)
        avgData.append([tempLabel, tempAvg])
        tempLabel = ''
        tempAvg = 0.0
    print(avgData)

    # Calculate Variance #
    tempVariance = 0.0
    for i in range(0, len(dataBuffer[0])):
        for j in range(0, len(dataBuffer)):
            if(j == 0):
                tempLabel = dataBuffer[j][i]
            else:
                tempVariance = tempVariance + (float(dataBuffer[j][i]) - avgData[i][1]) ** 2
        tempVariance = tempVariance / (len(dataBuffer) - 1) 
        print('tempVar: ', tempVariance)

        print(tempLabel, tempVariance)
        varianceData.append([tempLabel, tempVariance])
        tempLabel = ''
        tempVariance = 0.0
    print(varianceData)

    # Calculate Standard #
    tempStandard = 0.0
    for i in range(0, len(varianceData)):
        tempStandard = math.sqrt(varianceData[i][1])
        standardData.append([varianceData[i][0], tempStandard])
    print(standardData)

    # Calculate Cutline #
    tempCutline = 0.0
    for i in range(0, len(standardData)):
        tempCutline = avgData[i][1] + 3 * standardData[i][1]
        cutlineData.append([varianceData[i][0], tempCutline])
    print(cutlineData)

    # Filter Data #
    filteredData.append([dataBuffer[0]])
    tempArray = []
    for i in range(1, len(dataBuffer)):
        for j in range(0, len(dataBuffer[i])):
            if float(dataBuffer[i][j]) <= cutlineData[j][1]:
                tempArray.append(dataBuffer[i][j])
        

    mergedFile = open("merged_" + fileName + ".csv", 'w')
    for i in range(len(avgData)):
        writeData = avgData[i][0] + ',' + str(avgData[i][1]) + '\n'
        mergedFile.write(writeData)
    mergedFile.close()

def collectData(targetPath, dataBuffer):
    try:
        csvFile = open(targetPath, 'r')
        print('File Open: ' + targetPath)

        line = csvFile.readline()
        if(len(dataBuffer) == 0):
            line = line.replace('\n', '')
            print(line)
            dataBuffer.append(line.split(','))
            
        while True:
            line = csvFile.readline()
            if not line:
                break
            line = line.replace('\n', '')
            print(line)
            dataBuffer.append(line.split(','))
        csvFile.close()
    except:
        print('Invalid File Path')