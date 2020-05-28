###############################################################################
# import required packages
import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime as dt

###############################################################################
# Step 1. Launch the application
app = dash.Dash()
server = app.server
###############################################################################
# Step 2. Import the dataset
path = 'https://raw.githubusercontent.com/ateetmaharjan/Dash_app/master/dailyload5zone.csv'
st = pd.read_csv(path)
st.head()

###############################################################################
# Step 3. Create a plotly figure

trace_1 = go.Scatter(x=st.datetime, y=st['zone_1'], name='zone_1',
                     line=dict(width=2, color='rgb(229, 151, 50)'))

layout = dict(
    title=dict(text="<b>Timeseries plot for daily demand of energy loads</b>",
               y=0.9, x=0.5, font_size=18),
    hovermode='x', hoverlabel=dict(font_color='white'),
    xaxis=dict(
        title="<b>Time</b>", linecolor='black', linewidth=1,
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1 month", step="month",
                     stepmode="backward"),
                dict(count=6, label="6 month", step="month",
                     stepmode="backward"),
                dict(count=1, label="1 year", step="year",
                     stepmode="backward"),
                dict(label='full data', step="all")
            ])
        )
    ),
    yaxis=dict(title="<b>Energy Load (in kW)</b>",
               linecolor='black', linewidth=1),
    font=dict(family="Helvetica", size=12, color="black"),
    paper_bgcolor="white",
    template="plotly",
)
fig = go.Figure(data=[trace_1], layout=layout)
###############################################################################

# dropdown options

# the options should be in the format of a dictionary
# options will be the columns only with the continuous variables

features = st.columns[1:]
# opts = [{'label': i, 'value': i} for i in features]
opts = [{'label': 'ZONE 1', 'value': 'zone_1'},
        {'label': 'ZONE 2', 'value': 'zone_2'},
        {'label': 'ZONE 3', 'value': 'zone_3'},
        {'label': 'ZONE 4', 'value': 'zone_4'},
        {'label': 'ZONE 5', 'value': 'zone_5'}]


# range slider options
st['datetime'] = pd.to_datetime(st.datetime)
dates = [
    '2004-01-01', '2004-05-01', '2004-09-01',
    '2005-01-01', '2005-05-01', '2005-09-01',
    '2006-01-01', '2006-05-01', '2006-09-01',
    '2007-01-01', '2007-05-01', '2007-09-01',
    '2008-01-01', '2008-05-01', '2008-06-22'
]
###############################################################################

# Step 4. Create a Dash layout
app.layout = html.Div([
    # a header and a paragraph
    html.Div([
        html.H1("Daily load demand for each zone"),
        html.P(
            "The timeseries plot shows daily load (in kW) measurements for 5 geographic sub-areas (e.g., residential and industrial zones) from January 2004 to June 2008.")
    ],
        style={'padding': '50px',
               'backgroundColor': 'yellow'}),

    # dropdown menu options
    html.P(
        [html.Label("Choose each zone to display energy load plot"),
         dcc.Dropdown(id='opt',
                      options=opts,
                      value='zone_1')],
        style={
            'width': '400px',
            'fontSize': '20px',
                        'padding-left': '100px',
                        'display': 'inline-block'}),

    # adding a plot
    dcc.Graph(id='plot', figure=fig),

    # add range slider
    html.P([
        html.Label("Time Period"),
        dcc.RangeSlider(id='slider',
                        marks={i: dates[i] for i in range(0, 15)},
                        min=0,
                        max=14,
                        value=[0, 14])
    ], style={'width': '80%',
              'fontSize': '20px',
              'padding-left': '100px',
                          'display': 'inline-block'})
])
###############################################################################

# Step 5. Add callback functions


@app.callback(
    Output('plot', 'figure'), [
        Input('opt', 'value'), Input('slider', 'value')
    ])
def update_figure(input1, input2):
    # filtering the data
    st2 = st[(st.datetime > dates[input2[0]]) &
             (st.datetime < dates[input2[1]])]

    # updating the plot
    trace_1 = go.Scatter(x=st2.datetime, y=st2[input1],
                         name=input1,
                         line=dict(width=2,
                                   color='rgb(106, 181, 135)'))
    fig = go.Figure(data=[trace_1], layout=layout)
    return fig


# # Step 5. Add callback functions
# @app.callback(
#     Output('plot', 'figure'),
#     [Input('opt', 'value'), Input('slider', 'value')])
# def update_figure(input1, input2):
#     # filtering the data
#     st2 = st[(st.datetime > dates[input2[0]]) &
#              (st.datetime < dates[input2[1]])]

#     # updating the plot
#     trace_1 = go.Scatter(x=st2.datetime, y=st2['zone_1'],
#                          name='zone_1',
#                          line=dict(width=2,
#                                    color='rgb(229, 151, 50)'))

#     trace_2 = go.Scatter(x=st2.datetime, y=st2[input1],
#                          name=input1,
#                          line=dict(width=2,
#                                    color='rgb(106, 181, 135)'))
#     fig = go.Figure(data=[trace_1, trace_2], layout=layout)
#     return fig

###############################################################################

# # Step 6. Add the server clause

# if __name__ == "__main__":
#     app.run_server()


if __name__ == '__main__':
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(port=8050,
                   host='0.0.0.0',
                   debug=True
                   )
