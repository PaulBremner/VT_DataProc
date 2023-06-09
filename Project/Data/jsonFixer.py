import glob

jsonfiles = glob.glob('TimeData/*.json')


for jsonfile in jsonfiles:
    with open(jsonfile, "r") as file:
        line = file.read().replace('}', '}\n')

    with open('FixedData/' + jsonfile, 'w') as file:
        file.write(line)
