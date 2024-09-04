from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

# Load your dataset
dataset_path = r'Dataset\\UPDATED_DATA.csv'


df = pd.read_csv(dataset_path)

# Convert the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')


def run_dash():
    app = Dash(__name__)

    app.layout = html.Div(children=[
        html.H1(children='Run Hours vs Power Consumption', style={
                'text-align': 'center', 'margin-bottom': '20px', 'font-weight': 'bold'}),

        # Main container for all inputs
        html.Div([
            # Mill Dropdown
            html.Div([
                html.Label('Mill:', style={'font-weight': 'bold'}),
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
                html.Label('Trend Selection:', style={'font-weight': 'bold'}),
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
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'gap': '20px'}),

        # Date Input Fields (initially hidden)
        html.Div(id='date-input-container',
                 style={'display': 'none', 'margin-top': '20px'}),

        # Container for the dynamic graph
        html.Div(id='graph-container', style={'margin-top': '20px'})
    ])

    # Callback to show Date Input Fields based on Trend Selection
    @app.callback(
        Output('date-input-container', 'style'),
        Input('trend-dropdown', 'value')
    )
    def show_date_inputs(selected_trend):
        if selected_trend == 'Specific Date':
            return {'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
        return {'display': 'none'}

    # Callback to display date input fields when "Specific Date" is selected
    @app.callback(
        Output('date-input-container', 'children'),
        Input('trend-dropdown', 'value')
    )
    def display_date_inputs(selected_trend):
        if selected_trend == 'Specific Date':
            return html.Div([
                html.Label('Day:', style={
                           'font-weight': 'bold', 'margin-right': '10px'}),
                dcc.Input(id='day-input', type='number', placeholder='DD',
                          min=1, max=31, style={'margin-right': '20px'}),
                html.Label('Month:', style={
                           'font-weight': 'bold', 'margin-right': '10px'}),
                dcc.Input(id='month-input', type='number', placeholder='MM',
                          min=1, max=12, style={'margin-right': '20px'}),
                html.Label('Year:', style={
                           'font-weight': 'bold', 'margin-right': '10px'}),
                dcc.Input(id='year-input', type='number', placeholder='YYYY', min=df['Date'].dt.year.min(
                ), max=df['Date'].dt.year.max(), style={'margin-right': '20px'}),
                html.Button('Submit', id='submit-date', n_clicks=0,
                            style={'margin-left': '20px'})
            ], style={'display': 'flex', 'align-items': 'center'})
        return None

    # Callback to update the graph based on the selected date and mill option
    @app.callback(
        Output('graph-container', 'children'),
        [Input('submit-date', 'n_clicks')],
        [Input('day-input', 'value'),
         Input('month-input', 'value'),
         Input('year-input', 'value'),
         Input('mill-dropdown', 'value')]
    )
    def update_graph(n_clicks, day, month, year, selected_mill):
        if n_clicks > 0 and selected_mill and day and month and year:
            selected_date = pd.Timestamp(year, month, day)
            filtered_df = df[df['Date'] == selected_date]

            if selected_mill == 'RawMill-1' and not filtered_df.empty:
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Bar(
                                x=['RM', 'RMF', 'Sec. cla fan', 'Raw mill-Aux'],
                                y=[
                                    filtered_df['RM'].values[0],
                                    filtered_df['RMF'].values[0],
                                    filtered_df['Sec. cla fan'].values[0],
                                    filtered_df['Raw mill-Aux'].values[0]
                                ],
                                marker_color=['blue', 'green', 'red', 'purple']
                            )
                        ],
                        'layout': go.Layout(
                            title=f'Power Consumption on {selected_date.strftime("%d-%m-%Y")}',
                            xaxis={'title': 'Components'},
                            yaxis={'title': 'Power Consumption (kW)'},
                            hovermode='closest'
                        )
                    }
                )
            elif selected_mill == 'CoalMill-1' and not filtered_df.empty:
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Bar(
                                x=['CM', 'CMF', 'Coal mill-Aux'],
                                y=[
                                    filtered_df['CM'].values[0],
                                    filtered_df['CMF'].values[0],
                                    filtered_df['Coal mill-Aux'].values[0]
                                ],
                                marker_color=['blue', 'green', 'red']
                            )
                        ],
                        'layout': go.Layout(
                            title=f'Power Consumption on {selected_date.strftime("%d-%m-%Y")}',
                            xaxis={'title': 'Components'},
                            yaxis={'title': 'Power Consumption (kW)'},
                            hovermode='closest'
                        )
                    }
                )
            elif selected_mill == 'KILNMill-1' and not filtered_df.empty:
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Bar(
                                x=['IDF', 'BHF', 'MD',
                                    'Cooler fans Clinker Tr.', 'Kiln-1-Aux'],
                                y=[
                                    filtered_df['IDF'].values[0],
                                    filtered_df['BHF'].values[0],
                                    filtered_df['MD'].values[0],
                                    filtered_df['Cooler fans Clinker Tr.'].values[0],
                                    filtered_df['Kiln-1-Aux'].values[0]
                                ],
                                marker_color=['blue', 'green',
                                              'red', 'purple', 'orange']
                            )
                        ],
                        'layout': go.Layout(
                            title=f'Power Consumption on {selected_date.strftime("%d-%m-%Y")}',
                            xaxis={'title': 'Components'},
                            yaxis={'title': 'Power Consumption (kW)'},
                            hovermode='closest'
                        )
                    }
                )
            elif selected_mill == 'CementMill-1' and not filtered_df.empty:
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Bar(
                                x=['ZM', 'ZMF', 'Cement Mill-1-Aux'],
                                y=[
                                    filtered_df['ZM'].values[0],
                                    filtered_df['ZMF'].values[0],
                                    filtered_df['Cement Mill-1-Aux'].values[0]
                                ],
                                marker_color=['blue', 'green', 'red']
                            )
                        ],
                        'layout': go.Layout(
                            title=f'Power Consumption on {selected_date.strftime("%d-%m-%Y")}',
                            xaxis={'title': 'Components'},
                            yaxis={'title': 'Power Consumption (kW)'},
                            hovermode='closest'
                        )
                    }
                )
        return None

    # Run the server on localhost
    app.run_server(host='127.0.0.1', port=8050, debug=True, use_reloader=False)


if __name__ == '__main__':
    run_dash()
