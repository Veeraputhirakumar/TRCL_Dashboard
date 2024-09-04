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

            # Trend Selection Dropdown and Options Dropdown (aligned)
            html.Div([
                html.Div([
                    html.Label('Trend Selection:', style={
                               'font-weight': 'bold'}),
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

                html.Div(id='options-container',
                         style={'display': 'none', 'margin-top': '20px'})
            ], style={'display': 'flex', 'align-items': 'center', 'gap': '20px'}),

        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'gap': '20px'}),

        # Date Input Fields (initially hidden)
        html.Div(id='date-input-container',
                 style={'display': 'none', 'margin-top': '20px'}),

        # Date Range Input Fields (initially hidden)
        html.Div(id='date-range-container',
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

    # Callback to show the "Options" dropdown when "Range of Dates" is selected
    @app.callback(
        Output('options-container', 'style'),
        [Input('mill-dropdown', 'value'),
         Input('trend-dropdown', 'value')]
    )
    def show_options_dropdown(selected_mill, selected_trend):
        if selected_trend == 'Range of Dates' and selected_mill:
            return {'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
        return {'display': 'none'}

    # Callback to populate the "Options" dropdown based on the selected mill
    @app.callback(
        Output('options-container', 'children'),
        Input('mill-dropdown', 'value')
    )
    def populate_options(selected_mill):
        options = []
        if selected_mill == 'RawMill-1':
            options = [{'label': 'RM', 'value': 'RM'},
                       {'label': 'RMF', 'value': 'RMF'},
                       {'label': 'Sec. cla fan', 'value': 'Sec. cla fan'},
                       {'label': 'Raw mill-Aux', 'value': 'Raw mill-Aux'}]
        elif selected_mill == 'CoalMill-1':
            options = [{'label': 'CM', 'value': 'CM'},
                       {'label': 'CMF', 'value': 'CMF'},
                       {'label': 'Coal mill-Aux', 'value': 'Coal mill-Aux'}]
        elif selected_mill == 'KILNMill-1':
            options = [{'label': 'IDF', 'value': 'IDF'},
                       {'label': 'BHF', 'value': 'BHF'},
                       {'label': 'MD', 'value': 'MD'},
                       {'label': 'Cooler fans Clinker Tr.',
                           'value': 'Cooler fans Clinker Tr.'},
                       {'label': 'Kiln-1-Aux', 'value': 'Kiln-1-Aux'}]
        elif selected_mill == 'CementMill-1':
            options = [{'label': 'ZM', 'value': 'ZM'},
                       {'label': 'ZMF', 'value': 'ZMF'},
                       {'label': 'Cement Mill-1-Aux', 'value': 'Cement Mill-1-Aux'}]

        return html.Div([
            html.Label('Options:', style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='options-dropdown',
                options=options,
                placeholder="Select an Option",
                clearable=False,
                style={'width': '200px'}
            )
        ], style={'display': 'inline-block'})

    # Callback to hide or show Date Range input fields based on Trend Selection
    @app.callback(
        Output('date-range-container', 'style'),
        Input('trend-dropdown', 'value')
    )
    def show_date_range(selected_trend):
        if selected_trend == 'Range of Dates':
            return {'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
        return {'display': 'none'}

    # Callback to display Date Range input fields
    @app.callback(
        Output('date-range-container', 'children'),
        Input('trend-dropdown', 'value')
    )
    def display_date_range(selected_trend):
        if selected_trend == 'Range of Dates':
            return html.Div([
                html.Label('Date Range:', style={'font-weight': 'bold'}),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    start_date=None,  # No default start date
                    end_date=None,    # No default end date
                    display_format='YYYY-MM-DD',
                    style={'margin-right': '20px'}
                )
            ], style={'display': 'flex', 'align-items': 'center'})
        return None

    # Callback to update the graph based on the selected date range or specific date
    @app.callback(
        Output('graph-container', 'children'),
        [Input('date-range-picker', 'start_date'),
         Input('date-range-picker', 'end_date'),
         Input('day-input', 'value'),
         Input('month-input', 'value'),
         Input('year-input', 'value'),
         Input('mill-dropdown', 'value'),
         Input('options-dropdown', 'value'),
         Input('trend-dropdown', 'value')]
    )
    def update_graph(start_date, end_date, day, month, year, selected_mill, selected_option, trend_type):
        if not selected_mill or not selected_option:
            return html.Div("Please select a mill and an option.")

        # Process specific date
        if trend_type == 'Specific Date' and day and month and year:
            try:
                specific_date = pd.to_datetime(
                    f'{year}-{month:02d}-{day:02d}', format='%Y-%m-%d')
            except ValueError:
                return html.Div("Invalid date. Please check day, month, and year.")

            filtered_df = df[df['Date'] == specific_date]

            if not filtered_df.empty:
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Bar(
                                x=[opt for opt in df.columns if opt in [
                                    'RM', 'RMF', 'Sec. cla fan', 'Raw mill-Aux']],
                                y=[filtered_df[opt].sum() for opt in [
                                    'RM', 'RMF', 'Sec. cla fan', 'Raw mill-Aux']],
                                marker_color='blue'
                            )
                        ],
                        'layout': go.Layout(
                            title=f'Power Consumption on {specific_date.strftime("%d-%m-%Y")}',
                            xaxis={'title': 'Parameter'},
                            yaxis={'title': 'Power Consumption (kW)'},
                            hovermode='closest'
                        )
                    }
                )
            else:
                return html.Div(f'No data available for {specific_date.strftime("%d-%m-%Y")}')

        # Process date range
        elif trend_type == 'Range of Dates' and start_date and end_date:
            try:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
            except ValueError:
                return html.Div("Invalid date range. Please check start and end dates.")

            filtered_df = df[(df['Date'] >= start_date)
                             & (df['Date'] <= end_date)]

            if not filtered_df.empty:
                return dcc.Graph(
                    id='mill-graph',
                    figure={
                        'data': [
                            go.Scatter(
                                x=filtered_df['Date'],
                                y=filtered_df[selected_option],
                                mode='lines+markers',
                                line=dict(color='blue'),
                                name=selected_option
                            )
                        ],
                        'layout': go.Layout(
                            title=f'Power Consumption from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}',
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Power Consumption (kW)'},
                            hovermode='closest'
                        )
                    }
                )
            else:
                return html.Div(f'No data available from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}')

        return None

    # Run the app
    if __name__ == '__main__':
        # app.run_server(host='0.0.0.0', port=9000,debug=True, use_reloader=False)
        app.run_server(debug=False)


# Call the function to run the Dash app
run_dash()
