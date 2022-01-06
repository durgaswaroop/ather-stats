import pywebio
from pywebio.input import *
from pywebio.output import put_text, put_markdown, put_row
from datetime import date, datetime
import time
import os
import csv


CHARGE_STATS_FILE = 'ather_charging.csv'


COLUMNS = [
    'Start Date',
    'Start Time',
    'Start SoC %',
    'End Date',
    'End Time',
    'End Soc %',
    'Charged %',
    'Time taken'
]

def func():
    put_markdown(f'# Ather Charging Log')
    put_markdown(f'## Date: {date.today()}')
    put_markdown(f'## Charging Start')

    today_date = date.today()
    now_time = time.strftime('%H:%M')

    # Start
    inputs = input_group('Charging Times', [
        # Start
        input('Starting Date', name='start_date', type=DATE, value=str(today_date)),
        input('Starting Time', name='start_time', type=TIME, value=str(now_time)),
        slider('Starting Battery', name='start_soc', type=NUMBER, value=50),

        # End
        input('Ending Date', name='end_date', type=DATE, value=str(today_date)),
        input('Ending Time', name='end_time', type=TIME, value=str(now_time)),
        slider('Ending Battery', name='end_soc', type=NUMBER, value=50),
    ])

    actions(buttons=["Continue"])

    start_date = inputs['start_date']
    start_time = inputs['start_time']
    start_soc = inputs['start_soc']

    end_date = inputs['end_date']
    end_time = inputs['end_time']
    end_soc = inputs['end_soc']

    # '2022-01-04' + ' ' + '13:35' => '2022-01-04 13:35'
    start = datetime.fromisoformat(start_date + ' ' + start_time)
    end = datetime.fromisoformat(end_date + ' ' + end_time)

    charged_percent = end_soc - start_soc
    time_taken_mins = (end - start).seconds//60

    with open(CHARGE_STATS_FILE, 'a') as f:
        # If the file is empty, add columns
        if os.stat(CHARGE_STATS_FILE).st_size == 0:
            f.write(','.join(COLUMNS) + '\n')
        
        writer = csv.writer(f)
        writer.writerow([start_date, start_time, start_soc, end_date, end_time, end_soc, charged_percent, time_taken_mins])
        


if __name__ == '__main__':
    pywebio.start_server(func, port=8888)
