import csv


def read_series(path):
    f = open(path)
    csv_f = csv.reader(f)
    series = []
    for s in csv_f:
        series.append(map(float, s))
    return series
