import csv
import numpy as np
import datetime
from Stations import Stations

index={
    "date": 0,
    "temp": 1,
    "drew_pt": 2,
    "relat_hum": 3,
    "wind_dir": 4,
    "wind_speed": 5,
    "visibility": 6,
    "visib_indic": 7,
    "pressure": 8,
    "hmdx": 9,
    "wind_chill": 10,
    "weather": 11,
    "public_holy": 12,
    "station_code": 13,
    "withdrawals": 14,
    "volume": 15
}

geo_region = Stations("quartierssociologiques2014.json")

def get_OH_date(date):
    year, month, day = (int(x) for x in date.split('-'))
    data_day = datetime.date(year, month, day).weekday()
    return  [0 if i != data_day else 1 for i in range(7)]

def get_OH_hour(hour):
    hour_bornes = [6, 9, 11.30, 14, 16.30, 19, 21]
    hour_int = float(hour.replace(":", "."))
    hour_one_hot = [0 for _ in hour_bornes]
    if hour_int < hour_bornes[0] or hour_int > hour_bornes[-1]:
        hour_one_hot[0] = 1
    else:
        for i, _ in enumerate(hour_bornes):
            if hour_int > hour_bornes[i] and hour_int < hour_bornes[i + 1]:
                hour_one_hot[i] = 1
                break
    return hour_one_hot

def get_OH_wind_dir(wind_dir):
    index = int(wind_dir//4.5)
    return [1 if i == index else 0 for i in range(8)]

def get_OH_pressure(pressure):
    pressure_interval = [980, 1000, 1025, 1045]
    pressure_one_hot = [0 for _ in range(len(pressure_interval + 1))]
    if int(pressure) < pressure_interval[0]:
        pressure_one_hot[0] = 1
    elif int(pressure) > pressure_interval[-1]:
        pressure_one_hot[-1] = 1
    else:
        for i, _ in enumerate(pressure_interval):
            if pressure > pressure_interval[i] and pressure < pressure_interval[i + 1]:
                pressure_one_hot[i] = 1
                break
    return pressure_one_hot

def get_OH_region(station_code, geo_region_obj):
    for station in geo_region_obj.stations:
        if station_code == station["id"]:
            return [1 if station["quartier"]["id"] == index else 0 for index in range(len(geo_region_obj.region_ls))]


data = np.array(())

def count_total_line(filename):

    def _make_gen(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    return sum(buf.count(b'\n') for buf in f_gen)

def normalize(valeur, moy, ecart_type):
    return valeur

nb_lines = count_total_line("training.csv")
print("nb_line: " + str(nb_lines))
with open("training.csv", "r") as trainig_file:
    csv_reader = csv.reader(trainig_file)
    headers = next(csv_reader)
    for row in csv_reader:
        date, hour = row[index["date"]].split(' ')
        date_OH = get_OH_date(date)
        hour_OH = get_OH_hour(hour)
        wind_dir_OH = row[index["wind_dir"]]
        region_OH = get_OH_region(row[index["station_code"]], geo_region)
        ratio = float(csv_reader.line_num) / float(nb_lines)

        len_compt = 30
        print("\r [{}]{}% {} on {}".format("=" * (int(len_compt * ratio) - 1) + ">" + "-" * int(len_compt * (1-ratio)),
                                           int(ratio * 100),
                                           csv_reader.line_num, nb_lines), end="")
