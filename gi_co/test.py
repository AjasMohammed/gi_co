import csv

with open('gi_co/data.csv') as file:
    content = csv.reader(file)
    for line in content:
        print(line)