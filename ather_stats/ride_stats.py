import pandas as pd
import pywebio
from pywebio.output import put_text, put_markdown, put_row, put_html, put_table
import datetime as dt
import humanize
import plotly.express as px

from ather_stats.constants import RIDES_FILE

def ride_stats():
    rides_df = pd.read_csv(RIDES_FILE)
    
    total_number_of_rides = len(rides_df)
    