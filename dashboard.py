import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.plotting import figure
import seaborn as sns

# Load the tips dataset
df_tips = sns.load_dataset("tips")

# Create a Select widget for selecting the day of the week
select_day = Select(title='Day', options=['All'] + list(df_tips['day'].unique()))

# Create a Select widget for selecting the time of the day
select_time = Select(title='Time', options=['All'] + list(df_tips['time'].unique()))

# Create a figure for displaying the histogram
hist = figure(plot_width=500, plot_height=400, title='Tip Distribution')
hist.xaxis.axis_label = 'Tip Amount'
hist.yaxis.axis_label = 'Count'


# Define a callback function for the Select widgets
def update_histogram():
    # Filter the dataframe based on the selected day and time
    selected_day = select_day.value
    selected_time = select_time.value

    filtered_df = df_tips.copy()
    if selected_day != 'All':
        filtered_df = filtered_df[filtered_df['day'] == selected_day]
    if selected_time != 'All':
        filtered_df = filtered_df[filtered_df['time'] == selected_time]

    # Update the histogram based on the filtered dataframe
    hist.title.text = f'Tip Distribution ({selected_day}, {selected_time})'
    hist.quad(top=filtered_df['tip'], bottom=0, left=filtered_df.index - 0.5, right=filtered_df.index + 0.5,
              fill_color='dodgerblue', line_color='white')


# Attach the callback function to the Select widgets' value attributes
select_day.on_change('value', lambda attr, old, new: update_histogram())
select_time.on_change('value', lambda attr, old, new: update_histogram())

# Arrange the widgets and figure in a layout
controls = column(select_day, select_time)
layout = row(controls, hist)

# Update the histogram initially
update_histogram()

# Add the layout to the current document
curdoc().add_root(layout)
