import csv
import os
from data.models import AreaHousingPrice


def deal_file(filename):
    with open(filename, 'r') as csvFile:
        spamrendeer = csv.reader(csvFile)
        for row in spamrendeer:
            print('deal ....')
            ahp = AreaHousingPrice()
            ahp.area_name = row[0]
            ahp.dealAvgPrice = float(row[3])
            ahp.saleAvgPrice = float(row[2])
            ahp.total = int(row[8])
            ahp.date = row[-1]
            ahp.data_source = 'lianjia'
            print('-'*20)
            ahp.save()


def main():
    path = 'data/util/price_data/'
    filepath = [os.path.join(path, p) for p in os.listdir(path)]
    for i in filepath:
        deal_file(i)