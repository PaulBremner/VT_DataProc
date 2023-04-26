import glob

jsonfiles = glob.glob('TimeData/*.json')
#print(jsonfiles[0][8:])

for jsonfile in jsonfiles:
    with open(jsonfile, "r") as file:
        line = file.read().replace('}', '}\n')

    with open('FixedTimeData/' + jsonfile[9:], 'w') as file:
        file.write(line)
