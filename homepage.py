import pywebio
from pywebio.input import *
from pywebio.output import (
    put_button, 
    put_buttons, 
    put_image, 
    put_markdown, 
    put_row,
    put_text,
)

from ather_stats.charging_input import func
from ather_stats.charging_stats import charging_stats
from ather_stats.constants import ATHER_450X_IMAGE_FILE
from ather_stats.odometer import odometer_entry, odometer_graph
from ather_stats.range_calculation import predict_range


def index():
    put_markdown(f'# My Ather')

    with open(ATHER_450X_IMAGE_FILE, 'rb') as f:
        put_image(f.read(), width='75%').style('margin-left: auto; margin-right: auto; display: block')
    
    put_buttons(
        ['Add charging log', 'Charging Statistics'],
        onclick=[func, charging_stats]
    )

    # put_button(
    #     label='Add charging log',
    #     onclick=func,
    #     color='primary'
    # )

    # put_button(
    #     label='Charging Statistics',
    #     onclick=charging_stats,
    #     color='primary'
    # )

    charging_stats()

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
