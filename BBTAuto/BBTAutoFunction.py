import os, csv

def scanCSVFile(filePath):
    fileList = os.listdir(filePath)
    fileCSVList = []
    for i in fileList:
        if os.path.isdir(filePath + '/' + i):
            subdirPath = filePath + '/' + i
            subdirList = os.listdir(subdirPath)
            for j in subdirList:
                if (j.find('.CSV') != -1) or (j.find('.xlsx') != -1):
                    fileOpen = open(subdirPath + '/' + j, 'r')
                    print(subdirPath + '/' + j)
                    while(True):
                        lines = fileOpen.readlines()
                        if not lines:
                            break
                        
                        #print(lines)
                    fileOpen.close()
                        
 
    print(fileCSVList)