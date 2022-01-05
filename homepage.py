import pywebio
from pywebio.input import *
from pywebio.output import put_text, put_markdown, put_row, put_button

from ather_stats.charging_input import func
from ather_stats.charging_stats import charging_stats
from ather_stats.odometer import odometer_entry, odometer_graph
from ather_stats.range_calculation import predict_range

def index():
    put_markdown(f'# Ather Monitoring Stats')

    put_button(
        label='Add charging log',
        onclick=func,
        color='primary'
    )

    put_button(
        label='Charging Statistics',
        onclick=charging_stats,
        color='primary'
    )

    put_button(
        label='Odometer',
        onclick=odometer_entry,
        color='primary'
    )

    put_button(
        label='Range Prediction',
        onclick=predict_range,
        color='primary'
    )



if __name__ == '__main__':
    pywebio.start_server(index, port=8888)
