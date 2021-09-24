import os

import xlrd

import config
from src.db import session_maker
from src.sensors import Sensor


def check_sensors_data_in_db(street, sensor_num):
    with session_maker() as session:
        return session.query(Sensor).filter(Sensor.street == street, Sensor.sensor_num == sensor_num).first()


def init_sensors():
    files = os.listdir(config.sensors_data_path)

    example = ['Дата измерения', 'Температура', 'Влажность', 'СО2', 'ЛОС', 'Пыль pm 1.0', 'Пыль pm 2.5', 'Пыль pm 10',
               'Давление', 'AQI', 'Формальдегид']

    for file in files:
        workbook = xlrd.open_workbook(f'{config.sensors_data_path}/{file}', ignore_workbook_corruption=True)
        sheet = workbook.sheet_by_index(0)

        rows = [sheet.cell_value(0, col) for col in range(sheet.ncols)]
        if rows != example:
            print(f'Rows is not ok! Rows is {rows}, need to be like {example}')
            continue
        i = 1
        for row in range(1, sheet.nrows):
            elem = {}
            for col in range(sheet.ncols):
                value = sheet.cell_value(row, col)
                if not value:
                    elem = None
                    break
                elem[col] = value
            if not elem:
                continue

            street = file.replace('.xls', '').split('_')[0]
            sensor_num = file.replace('.xls', '').split('_')[-1]

            if i == 1:
                if check_sensors_data_in_db(street, sensor_num):
                    continue
                i += 1

            sensor = Sensor(
                street=street,
                sensor_num=int(sensor_num),
                coords={},
                measurement_datetime=elem[0],
                temperature=round(elem[1], 3),
                humidity=round(elem[2], 3),
                co2=round(elem[3], 3),
                los=round(elem[4], 3),
                pm1=round(elem[5], 3),
                pm2_5=round(elem[6], 3),
                pm10=round(elem[7], 3),
                pressure=round(elem[8], 3),
                aqi=round(elem[9], 3),
                formaldehyde=round(elem[10], 3),
            )
            with session_maker() as session:
                session.add(sensor)
                session.commit()
