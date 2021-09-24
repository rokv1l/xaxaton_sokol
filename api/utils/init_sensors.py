import os

import xlrd

import config
from src.db import session_maker
from src.sensors import Sensor


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

        for row in range(1, sheet.nrows):
            elem = {}
            for col in range(sheet.ncols):
                elem[col] = sheet.cell_value(row, col)

            street = file.replace('.xls', '').split('_')[0]
            sensor_num = file.replace('.xls', '').split('_')[-1]

            sensor = Sensor(
                street=street,
                sensor_num=int(sensor_num),
                coords={},
                measurement_datetime=elem[0],
                temperature=elem[1],
                humidity=elem[2],
                co2=elem[3],
                los=elem[4],
                pm1=elem[5],
                pm2_5=elem[6],
                pm10=elem[7],
                pressure=elem[8],
                aqi=elem[9],
                formaldehyde=elem[10],
            )
            with session_maker() as session:
                session.add(sensor)
                session.commit()
