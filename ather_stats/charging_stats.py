import pandas as pd
import pywebio
from pywebio.output import put_text, put_markdown, put_row, put_html, put_table
import datetime as dt
import humanize
import plotly.express as px

from ather_stats.constants import CHARGE_STATS_FILE, BATTERY_KWH


def charging_stats():
    put_markdown('## Charging Statistics')
    df = pd.read_csv(CHARGE_STATS_FILE)

    # No. of times charged
    num_times_charged = len(df)

    # Total time charged
    total_time_charged_mins = df['Time taken'].sum()
    total_time_charged = dt.timedelta(minutes=int(total_time_charged_mins))

    # Average percentage charge each time
    avg_percentage_charge = df['Charged %'].mean()

    # Identify Fast charging
    df['Charge Per Minute'] = df['Charged %']/df['Time taken']
    df['Is Fast Charging'] = df['Charge Per Minute'] > 0.75
    num_fast_charging = len(df[df['Is Fast Charging'] == True])

    # Average charge gain in one hour
    slow_charged_df = df[df['Is Fast Charging'] == False]
    avg_slow_charge_per_min = 60 * sum(slow_charged_df['Charged %'])/sum(slow_charged_df['Time taken'])
    fast_charged_df = df[df['Is Fast Charging'] == True]
    avg_fast_charge_per_min = 60 * sum(fast_charged_df['Charged %'])/sum(fast_charged_df['Time taken'])

    total_slow_charged_time = dt.timedelta(minutes=int(slow_charged_df['Time taken'].sum()))
    total_fast_charged_time = dt.timedelta(minutes=int(fast_charged_df['Time taken'].sum()))

    avg_slow_charged_time = dt.timedelta(minutes=int(slow_charged_df['Time taken'].mean()))
    avg_fast_charged_time = dt.timedelta(minutes=int(fast_charged_df['Time taken'].mean()))

    # KWH charged so far
    total_slow_charged_percentage = slow_charged_df['Charged %'].sum()
    total_fast_charged_percentage = fast_charged_df['Charged %'].sum()
    total_slow_charged_kwh = total_slow_charged_percentage * BATTERY_KWH / 100
    total_fast_charged_kwh = total_fast_charged_percentage * BATTERY_KWH / 100

    put_table([
        ['', 'Regular charge', 'Fast Charge'],
        ['No. of times charged',num_times_charged - num_fast_charging,  num_fast_charging],
        ['Time charged', humanize.naturaldelta(total_slow_charged_time), humanize.naturaldelta(total_fast_charged_time)],
        ['Avg. charge gain in one hour', f'{avg_slow_charge_per_min: .1f}%', f'{avg_fast_charge_per_min :.1f}%'],
        ['Electricity Consumed', f'{total_slow_charged_kwh: .1f} units', f'{total_fast_charged_kwh: .1f} units'],
        ['Avg. Charge duration', humanize.naturaldelta(avg_slow_charged_time), humanize.naturaldelta(avg_fast_charged_time)]
    ])

    # Aggregate on total charge time per day
    day_grouped_by_charging_time = df.groupby('Start Date').sum()['Time taken']
    fig = px.bar(day_grouped_by_charging_time, title='Charging time in mins by day')
    html = fig.to_html(include_plotlyjs="require", full_html=False)
    put_html(html)


if __name__ == '__main__':
    pywebio.start_server(charging_stats, port=8888)
