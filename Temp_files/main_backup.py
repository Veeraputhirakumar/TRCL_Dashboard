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
        html.H1(children='Energy Consumption', style={
                'text-align': 'center', 'margin-bottom': '20px', 'font-weight': 'bold'}),

        # Main container for all inputs
        html.Div([
            # Container for Trend Selection, Mill Dropdown, and Options Dropdown
            html.Div([
                # Trend Selection Dropdown
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

                # Mill Dropdown
                html.Div([
                    html.Label('Mill:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='mill-dropdown',
                        options=[
                            {'label': 'RawMill-1', 'value': 'RawMill-1'},
                            {'label': 'CoalMill-1', 'value': 'CoalMill-1'},
                            {'label': 'KILN-1', 'value': 'KILN-1'},
                            {'label': 'CementMill-1', 'value': 'CementMill-1'},
                        ],
                        placeholder="Select a Mill",
                        clearable=False,
                        style={'width': '200px'}
                    )
                ], style={'display': 'inline-block', 'margin-right': '20px'}),

                # Options Dropdown
                html.Div(id='options-container',
                         style={'display': 'none', 'margin-top': '20px', 'display': 'inline-block'}),

            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'gap': '20px'}),

            # Date Input Fields (initially hidden)
            html.Div(id='date-input-container',
                     style={'display': 'none', 'margin-top': '20px'}),

            # Date Range Input Fields (initially hidden)
            html.Div(id='date-range-container',
                     style={'display': 'none', 'margin-top': '20px'}),

        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),

        # Container for the dynamic graph
        html.Div(id='graph-container', style={'margin-top': '20px'})
    ])

    # Callback to show/hide the "Options" dropdown based on the trend selection
    @app.callback(
        Output('options-container', 'style'),
        Input('trend-dropdown', 'value')
    )
    def show_options_dropdown(selected_trend):
        if selected_trend == 'Range of Dates':
            return {'display': 'inline-block', 'margin-top': '20px'}
        return {'display': 'none'}

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
                html.Label('Select Date:', style={
                           'font-weight': 'bold', 'margin-right': '10px'}),
                dcc.DatePickerSingle(
                    id='date-picker-single',
                    date=None,  # No default date
                    display_format='YYYY-MM-DD',
                    style={'margin-right': '20px'}
                )
            ], style={'display': 'flex', 'align-items': 'center'})
        return None

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
        elif selected_mill == 'KILN-1':
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
         Input('date-picker-single', 'date'),
         Input('mill-dropdown', 'value'),
         Input('options-dropdown', 'value'),
         Input('trend-dropdown', 'value')]
    )
    def update_graph(start_date, end_date, specific_date, selected_mill, selected_option, trend_type):
        # Debug: Check the input values
        print(f"Trend Type: {trend_type}")
        print(f"Specific Date: {specific_date}")
        print(f"Selected Mill: {selected_mill}")

        # Handle Specific Date selection
        if trend_type == 'Specific Date' and specific_date and selected_mill:
            try:
                # Convert selected date to pandas datetime
                selected_date = pd.to_datetime(specific_date)
                # Debug: Confirm date conversion
                print(f"Converted Specific Date: {selected_date}")
            except ValueError:
                # Debug: Log error in date format
                print("Invalid date format encountered.")
                return html.Div("Invalid date format. Please check the selected date.")

            # Filter the data for the specific date
            filtered_df = df[df['Date'] == selected_date]
            # Debug: Show filtered data
            print(f"Filtered Data for {selected_date}: {filtered_df}")

            # Check if the filtered data is empty
            if filtered_df.empty:
                # Debug: No data
                print(
                    f"No data available for {selected_date.strftime('%d-%m-%Y')}")
                return html.Div(f'No data available for {selected_date.strftime("%d-%m-%Y")}')

            # Check mill type and plot the corresponding graph
            if selected_mill == 'RawMill-1':
                # Debug: Indicate graph generation for RawMill-1
                print("Generating graph for RawMill-1")
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
            elif selected_mill == 'CoalMill-1':
                # Debug: Indicate graph generation for CoalMill-1
                print("Generating graph for CoalMill-1")
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
            elif selected_mill == 'KILN-1':
                # Debug: Indicate graph generation for KILN-1
                print("Generating graph for KILN-1")
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
            elif selected_mill == 'CementMill-1':
                # Debug: Indicate graph generation for CementMill-1
                print("Generating graph for CementMill-1")
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

        # Handle Range of Dates selection
        elif trend_type == 'Range of Dates' and start_date and end_date:
            try:
                # Convert start and end dates to pandas datetime
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                # Debug: Show date range
                print(f"Date Range: {start_date} to {end_date}")
            except ValueError:
                # Debug: Log error in date range
                print("Invalid date range encountered.")
                return html.Div("Invalid date range. Please check the start and end dates.")

            # Filter the data for the date range
            filtered_df = df[(df['Date'] >= start_date)
                             & (df['Date'] <= end_date)]

            # Check if filtered data is empty
            if filtered_df.empty:
                # Debug: No data
                print(
                    f"No data available from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
                return html.Div(f'No data available from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}')

            # Check if the selected option exists in the data columns
            if selected_option in filtered_df.columns:
                # Debug: Indicate graph generation
                print(
                    f"Generating graph for option {selected_option} over range.")
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

        # Default case: no data or incorrect inputs
        print("No valid data to display.")  # Debug: No valid inputs provided
        return None

    # Run the app
    if __name__ == '__main__':
        # app.run_server(host='0.0.0.0', port=9000,debug=True, use_reloader=False)
        app.run_server(debug=False)


# Call the function to run the Dash app
run_dash()
