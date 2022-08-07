import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

DATA_DIR = 'data/data.parquet'
df = pd.read_parquet(DATA_DIR, engine='auto')
df['departure_date']= pd.to_datetime(df['departure_date'], format="%Y-%m-%d")
df['sale_date']= pd.to_datetime(df['sale_date'], format="%Y-%m-%d")
df["total_sale"] = df["price"]*df["demand"]
df["route"] = df['destination_station_name']+"-"+df['origin_station_name']

def get_df_ab(df, key1, key2):
    return df[df['origin_station_name'].isin(key1) & df['destination_station_name'].isin(key2)]

def make_ts_table(df, f=None):
    df2 = df.groupby(by=['sale_date'])[["demand","total_sale"]].sum().reindex(pd.date_range(min(df["sale_date"]).date(), max(df["departure_date"]).date()), fill_value=f)
    df2["dynamic_avg_price"] = df2["total_sale"]/df2["demand"]
    df2 = df2.rename_axis(index='Time')
    total = df2.rename(columns={"total_sale": "dynamic_total_sale","demand":"dynamic_demand"})
    
    df3 = df.groupby(by=['departure_date'])[["demand","total_sale"]].sum().reindex(pd.date_range(min(df["sale_date"]).date(), max(df["departure_date"]).date()), fill_value=f)
    total["demand"] = df3["demand"]
    total["total_sale"] = df3["total_sale"]
    total["avg_price"] = total["total_sale"]/total["demand"]
    return total

def make_total_ts(df, f=None):
    total=make_ts_table(df,f)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=total.index, y=total.dynamic_demand, name="Ticket sold on date"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=total.index, y=total.demand, name="Demand on date"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=total.index, y=total.dynamic_avg_price, name="Dynamic average price on date"),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(x=total.index, y=total.avg_price, name="Average price on date"),
        secondary_y=True,
    )
    fig.update_layout(
        title="Time Series of ticket demand",
        xaxis_title="Time window",
        yaxis_title="Ticket Sold",
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_yaxes(title_text="<b>Number of ticket sold</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Price</b>", secondary_y=True)
    return fig

app = dash.Dash()
app.layout = html.Div([
    html.Div([
        "Departure: ",
        dcc.Input(id='Departure', value='bb', type='text')
    ]),
    html.Div([
        "Destination: ",
        dcc.Input(id='Destination', value='rb', type='text')
    ]),
    html.H2("Time series on given Departure and Destination"),
    dcc.Graph(
        id='TS',
    )
])

@app.callback(
    Output('TS', 'figure'),
    Input('Departure', 'value'),
    Input('Destination', 'value'))
def make_fig(Departure, Destination):
    key1 = [str(Departure)]
    key2 = [str(Destination)]
    data = get_df_ab(df, key1, key2)
    fig = make_total_ts(data)
    return fig

app.run_server(debug=True, use_reloader=False)