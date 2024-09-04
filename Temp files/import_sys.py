import sys
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

# Load your dataset
dataset_path = r'D:\RC Ld\Dataset\UPDATED DATA.csv'
df = pd.read_csv(dataset_path)

# Convert the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')  # Adjusted format

def run_dash():
    app = Dash(__name__)

    app.layout = html.Div(children=[
        html.H1(children='Run Hours vs Power Consumption', style={'text-align': 'center', 'margin-bottom': '20px', 'font-weight': 'bold'}),

        # Main container for all inputs
        html.Div([
            # Mill Dropdown
            html.Div([
                html.Label('Mill:', style={'font-weight': 'bold', 'display': 'block', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='mill-dropdown',
                    options=[
                        {'label': 'RawMill-1', 'value': 'RawMill-1'},
                        {'label': 'CoalMill-1', 'value': 'CoalMill-1'},
                        {'label': 'KILNMill-1', 'value': 'KILNMill-1'},
                        {'label': 'CementMill-1', 'value': 'CementMill-1'},
                    ],
                    placeholder="Select a Mill",
                    clearable=False,
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block', 'margin-right': '20px'}),

            # Trend Selection Dropdown
            html.Div([
                html.Label('Trend Selection:', style={'font-weight': 'bold', 'display': 'block', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='trend-dropdown',
                    options=[
                        {'label': 'Specific Date', 'value': 'Specific Date'},
                        {'label': 'Range of Dates', 'value': 'Range of Dates'},
                    ],
                    placeholder="Select a Trend",
                    clearable=False,
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block', 'margin-right': '20px'}),

            # Options Dropdown (initially hidden)
            html.Div(id='options-container', style={'display': 'inline-block', 'margin-right': '20px'}),

        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'gap': '20px'}),

        # Date Range Picker (initially hidden, shown below the Trend Selection dropdown)
        html.Div(id='date-range-container', style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}),

        # Container for the dynamic graph
        html.Div(id='graph-container', style={'margin-top': '20px'})
    ])

    # Callback to show Options Dropdown based on Trend Selection
    @app.callback(
        Output('options-container', 'children'),
        Input('trend-dropdown', 'value')
    )
    def show_options(selected_trend):
        if selected_trend == 'Range of Dates':
            return html.Div([
                html.Label('Options:', style={'font-weight': 'bold', 'display': 'block', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='sub-dropdown',
                    options=[],
                    placeholder="Select an Option",
                    clearable=False,
                    style={'width': '200px'}
                )
            ])
        return None

    # Callback to show Date Range Picker based on Options Dropdown selection
    @app.callback(
        Output('date-range-container', 'children'),
        Input('sub-dropdown', 'value')
    )
    def show_date_range(selected_option):
        if selected_option:
            return html.Div([
                html.Label('Date Range:', style={'font-weight': 'bold', 'margin-right': '10px', 'align-self': 'center'}),
                dcc.DatePickerRange(
                    id='range-date-picker',
                    start_date_placeholder_text='Start Date',
                    end_date_placeholder_text='End Date',
                    display_format='DD-MM-YYYY',
                    style={'width': '400px'}
                )
            ], style={'display': 'flex', 'align-items': 'center'})
        return None

    # Callback to update Options Dropdown based on Mill Selection
    @app.callback(
        Output('sub-dropdown', 'options'),
        Input('mill-dropdown', 'value')
    )
    def update_options(selected_mill):
        options = []
        if selected_mill == 'RawMill-1':
            options = [
                {'label': 'RM', 'value': 'RM'},
                {'label': 'RMF', 'value': 'RMF'},
                {'label': 'Sec. cla fan', 'value': 'Sec. cla fan'},
                {'label': 'Raw mill-Aux', 'value': 'Raw mill-Aux'},
            ]
        elif selected_mill == 'CoalMill-1':
            options = [
                {'label': 'CM', 'value': 'CM'},
                {'label': 'CMF', 'value': 'CMF'},
                {'label': 'Coal mill-Aux', 'value': 'Coal mill-Aux'},
            ]
        elif selected_mill == 'KILNMill-1':
            options = [
                {'label': 'IDF', 'value': 'IDF'},
                {'label': 'BHF', 'value': 'BHF'},
                {'label': 'MD', 'value': 'MD'},
                {'label': 'Cooler fans Clinker Tr.', 'value': 'Cooler fans Clinker Tr.'},
                {'label': 'Kiln-1-Aux', 'value': 'Kiln-1-Aux'},
            ]
        elif selected_mill == 'CementMill-1':
            options = [
                {'label': 'ZM', 'value': 'ZM'},
                {'label': 'ZMF', 'value': 'ZMF'},
                {'label': 'Cement Mill-1-Aux', 'value': 'Cement Mill-1-Aux'},
            ]
        return options

    # Callback to update graph based on option selection and date range
    @app.callback(
        Output('graph-container', 'children'),
        [Input('sub-dropdown', 'value'),
         Input('range-date-picker', 'start_date'),
         Input('range-date-picker', 'end_date')]
    )
    def update_graph(selected_option, start_date, end_date):
        if selected_option and start_date and end_date:
            filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
            if selected_option in filtered_df.columns:
                y_values = filtered_df[selected_option]
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Scatter(
                                x=filtered_df['Date'],
                                y=y_values,
                                mode='lines+markers',
                                name=selected_option,
                                line=dict(width=2)
                            )
                        ],
                        'layout': go.Layout(
                            title=f'{selected_option} Over Time',
                            xaxis={
                                'title': 'Date',
                                'tickformat': '%b %Y'  # Format to show month and year
                            },
                            yaxis={'title': selected_option},
                            hovermode='closest'
                        )
                    }
                )
        return None

    # Run the server on localhost
    app.run_server(host='127.0.0.1', port=8050, debug=True, use_reloader=False)

if __name__ == '__main__':
    run_dash()
