f = open('C:\\Users\\exon9\\Downloads\\SamplingSource\\MS2210433-25\\Sample-SVP1B111.CSV', 'r')

line = f.readline()

editList = line.split('","')

print(editList[0])

f.close()
