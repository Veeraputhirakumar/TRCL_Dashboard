import sys
from dash import Dash, dcc, html
import plotly.graph_objs as go
import pandas as pd

# Load your dataset
dataset_path = r'D:\RC Ld\oly.csv'
df = pd.read_csv(dataset_path)

def run_dash():
    app = Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children='Country vs Gold and Total'),
        html.Div(children=[
            dcc.Graph(
                id='country-gold-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=df['Country'],
                            y=df['Gold'],
                            name='Gold'
                        ),
                        go.Scatter(
                            x=df['Country'],
                            y=[24] * len(df),  # Baseline value
                            mode='lines',
                            name='Baseline',
                            line=dict(color='red', width=2, dash='dash')
                        )
                    ],
                    'layout': go.Layout(
                        title='Gold Medals by Country',
                        xaxis={'title': 'Country'},
                        yaxis={'title': 'Gold'},
                        hovermode='closest'
                    )
                }
            ),
            dcc.Graph(
                id='country-total-graph',
                figure={
                    'data': [
                        go.Scatter(
                            x=df['Country'],
                            y=df['Total'],  # Assuming 'Total' column exists in the dataset
                            mode='lines+markers',
                            name='Total',
                            line=dict(color='blue', width=2)
                        )
                    ],
                    'layout': go.Layout(
                        title='Total by Country',
                        xaxis={'title': 'Country'},
                        yaxis={'title': 'Total'},
                        hovermode='closest'
                    )
                }
            )
        ], style={'display': 'flex', 'flex-direction': 'row'})
    ])
    app.run_server(host='', port=8050, debug=True, use_reloader=False)

if __name__ == '__main__':
    run_dash()
