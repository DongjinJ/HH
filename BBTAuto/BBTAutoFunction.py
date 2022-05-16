from audioop import findfactor
import math
import os

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

def scanTargetCSV(filePath, fileName, targetFilePath, logBox, vendor, mergedPath):
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
                    logBox.append(' => Find ' + targetPath + '\n')
                    collectData(targetPath, dataBuffer)
        else:
            if (i.find(fileName) != -1):
                targetPath = subdirPath + '/' + i
                logBox.append(' => Find ' + targetPath + '\n')
                collectData(targetPath, dataBuffer)
    convDataBuffer = list(map(list, zip(*dataBuffer)))
    logBox.append(' => Success Scan CSV Data\n')
    print(convDataBuffer)

    logBox.append('>> Calculating Average Value...')
    avgData = calculationAverage(convDataBuffer)
    logBox.append(' => Success!\n')

    logBox.append('>> Calculating Variance Value...')
    varianceData = calculationVariance(convDataBuffer, avgData)
    logBox.append(' => Success!\n')

    logBox.append('>> Calculating Standard Value...')
    standardData = calculationStandard(varianceData)
    logBox.append(' => Success!\n')
    
    logBox.append('>> Calculating Cutline Value...')
    cutlineData = calculationCutlineData(avgData, standardData)
    logBox.append(' => Success!\n')

    logBox.append('>> Filtering Data')
    filteredData = filterData(convDataBuffer, cutlineData)
    logBox.append(' => Success!\n')
    
    logBox.append('>> Save Filtered Data')
    savePath = targetFilePath + '/target_' + fileName
    logBox.append('>> Save Path: ' + savePath)
    targetFile = open(savePath, 'w')
    for i in range(len(filteredData)):
        for j in range(len(filteredData[i])):
            if(j == 0):
                writeHeader = '"\'' + filteredData[i][j] + '",'
                print(writeHeader)
                targetFile.write('"\'' + filteredData[i][j] + '",')
            else:
                targetFile.write(filteredData[i][j] + ',')
        targetFile.write('\n')
    targetFile.close()
    logBox.append(' => Complete save File\n')

    calculationResultData(filteredData, vendor, logBox, mergedPath, fileName)

def calculationResultData(dataBuffer, vendor, logBox, mergedPath, fileName):
    resultData = []
    if vendor == 'SEC':
        logBox.append('>> SEC 기준 결과값 산출 중..')
        resultAvg = calculationAverage(dataBuffer)
        resultVariance = calculationVariance(dataBuffer, resultAvg)
        resultSigma = calculationStandard(resultVariance)
        for i in range(len(resultAvg)):
            curAvg = resultAvg[i][1]
            curSigma = resultSigma[i][1]
            if curAvg < 30:
                calValue = curAvg + 20
            elif curAvg >= 30 and curAvg <= 100:
                calValue = curAvg * 1.8
            elif curAvg > 100 and curAvg <= 1000:
                calValue = curAvg + 5 * curSigma
            elif curAvg > 1000 and curAvg <= 1500:
                calValue = curAvg + 4.7 * curSigma
            else:
                calValue = curAvg + 4.5 * curSigma
            resultData.append([resultAvg[i][0], calValue])

    elif vendor == 'Hynix':
        logBox.append('>> Hynix 기준 결과값 산출 중..')
        resultAvg = calculationAverage(dataBuffer)
        resultVariance = calculationVariance(dataBuffer, resultAvg)
        resultSigma = calculationStandard(resultVariance)
        for i in range(len(resultAvg)):
            curAvg = resultAvg[i][1]
            curSigma = resultSigma[i][1]
            if curAvg < 30:
                calValue = curAvg + 20
            elif curAvg >= 30 and curAvg <= 100:
                calValue = curAvg * 1.8
            else:
                calValue = curAvg + 6 * curSigma
            resultData.append([resultAvg[i][0], calValue])
    else:
        logBox.append('! [Error]: 계산 기준 Vendor Option 확인 필요')
    
    logBox.append('>> Save Result Data')
    savePath = mergedPath + '/target_' + fileName
    logBox.append('>> Save Path: ' + savePath)
    targetFile = open(savePath, 'w')
    for i in range(len(resultData)):
        for j in range(len(resultData[i])):
            if(j == 0):
                writeHeader = '"\'' + resultData[i][j] + '",'
                print(writeHeader)
                targetFile.write('"\'' + resultData[i][j] + '",')
            else:
                targetFile.write(str(resultData[i][j]) + ',')
        targetFile.write('\n')
    targetFile.close()
    logBox.append(' => Complete save File\n')


def calculationAverage(dataBuffer):
    avgData = []
    # Calculate Average #
    tempLabel = ''
    tempAvg = 0.0
    for i in range(len(dataBuffer)):
        tempLabel = dataBuffer[i][0]
        for j in range(1, len(dataBuffer[i])):
            tempAvg += float(dataBuffer[i][j])
        tempAvg = tempAvg / (len(dataBuffer[i]) - 1)
        avgData.append([tempLabel, tempAvg])
        tempAvg = 0.0

    print('평균 값 계산')
    print(avgData)

    return avgData

def calculationVariance(dataBuffer, avgData):
    varianceData = []

    # Calculate Variance #
    tempLabel = ''
    tempVariance = 0.0
    for i in range(len(dataBuffer)):
        tempLabel = dataBuffer[i][0]
        for j in range(1, len(dataBuffer[i])):
            tempVariance = tempVariance + (float(dataBuffer[i][j]) - avgData[i][1]) ** 2
        tempVariance = tempVariance / (len(dataBuffer[i]) - 1) 
        varianceData.append([tempLabel, tempVariance])
        tempVariance = 0.0
    
    print('분산 값 계산')
    print(varianceData)

    return varianceData

def calculationStandard(varianceData):
    standardData = []
    # Calculate Standard #
    tempStandard = 0.0
    for i in range(0, len(varianceData)):
        tempStandard = math.sqrt(varianceData[i][1])
        standardData.append([varianceData[i][0], tempStandard])

    print('표준편차 계산')
    print(standardData)

    return standardData

def calculationCutlineData(avgData, standardData):
    cutlineData = []
    # Calculate Cutline #
    tempCutline = 0.0
    for i in range(0, len(standardData)):
        tempCutline = avgData[i][1] + 3 * standardData[i][1]
        cutlineData.append([standardData[i][0], tempCutline])

    print('Cutline 기준 계산')
    print(cutlineData)

    return cutlineData

def filterData(dataBuffer, cutlineData):
    filteredData = []

    # Filter Data #
    tempArray = []
    for i in range(len(dataBuffer)):
        tempArray = dataBuffer[i]
        for j in range(len(dataBuffer[i])-1, 0):
            if (float(tempArray[j]) >= cutlineData[i][1]):
                del tempArray[j]
        filteredData.append(tempArray)
    
    print('-- Filtered Data --')
    #print(filteredData)

    return filteredData


def collectData(targetPath, dataBuffer):
    try:
        csvFile = open(targetPath, 'r')
        print('File Open: ' + targetPath)

        line = csvFile.readline()
        if(len(dataBuffer) == 0):
            line = line.replace('\n', '')
            line = line.replace(' ', '')
            line = line.replace('"', ' ')
            print(line)
            tempList = line.split(' , ')
            header = []
            for i in tempList:
                header.append(i.replace(' ', ''))
            dataBuffer.append(header)
            
        while True:
            line = csvFile.readline()
            if not line:
                break
            line = line.replace('\n', '')
            #print(line)
            dataBuffer.append(line.split(','))
        csvFile.close()
    except:
        print('Invalid File Path')