import pandas as pd
import pywebio
from pywebio.output import put_text, put_markdown, put_row, put_html, put_table
import datetime as dt
import humanize
import plotly.express as px

from ather_stats.constants import CHARGE_STATS_FILE, ODOMETER_FILE, INITIAL_CHARGE_PERCENTAGE, USABLE_BATTERY_KWH, RIDES_FILE


def predict_range():

    charging_df = pd.read_csv(CHARGE_STATS_FILE)
    percentage_points_charged = charging_df['Charged %'].sum()
    total_charged_percentage = INITIAL_CHARGE_PERCENTAGE + percentage_points_charged

    odometer_df = pd.read_csv(ODOMETER_FILE)
    current_odometer_reading = float(odometer_df['Odometer'].iloc[-1])

    # x% charge gave the current Odometer value. How much would 100% give?
    predicted_range = 100 * current_odometer_reading / total_charged_percentage

    # Range from rides
    rides_df = pd.read_csv(RIDES_FILE)
    rides_df['energy_used_kwh'] = rides_df['Distance'] * rides_df['Efficiency'] / 1000

    print(rides_df.head())

    total_distance_ridden = rides_df['Distance'].sum()
    total_kwh_used = rides_df['energy_used_kwh'].sum()

    print(total_distance_ridden, total_kwh_used)

    predicted_range_from_rides = total_distance_ridden * USABLE_BATTERY_KWH / total_kwh_used
    

    put_table([
        ['Predicted Range based on Charging data',  f'{predicted_range :.2f} Kms'],
        ['Predicted Range based on Ride data',  f'{predicted_range_from_rides :.2f} Kms'],
    ], header=[])
