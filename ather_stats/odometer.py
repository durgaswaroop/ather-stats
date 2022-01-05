import datetime as dt

import humanize
import pandas as pd
import plotly.express as px
import pywebio
from pywebio.output import put_html, put_markdown, put_row, put_table, put_text

from ather_stats.constants import ODOMETER_FILE


def odometer_graph():

    pass

def odometer_entry():
    put_markdown(f'# Ather Odometer')
    odometer_df = pd.read_csv(ODOMETER_FILE)
    # breakpoint()
    # print(odometer_df.head())

    current_odometer_reading = float(odometer_df['Odometer'].iloc[-1])
    # print(current_odometer_reading)
    # print(type(current_odometer_reading))

    fig = px.line(odometer_df, x='Date', y='Odometer',title=f'Current Odometer = {current_odometer_reading} Kms')
    html = fig.to_html(include_plotlyjs="require", full_html=False)
    put_html(html)
