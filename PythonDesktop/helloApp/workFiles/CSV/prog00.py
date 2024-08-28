import csv
name_file ='test.csv'

file1 = open(name_file)

csvreader = csv.reader(file1)

for row in csvreader:
    for data in row:
        print(data)
    print('---')
    row.append(row)
    