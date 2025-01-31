import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboards',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(
            id='site-dropdown',
             options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
             , {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
            value='ALL',
            placeholder='Select a Launch Site here',
            searchable = True
        ),
        # return the outcomes piechart for a selected site

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,  # Cambia según el intervalo que desees
    marks={
    0: '0 kg',
    2500:'2500 kg',
    5000: '5000 kg',
    7500: '7500 kg',
    10000: '10000 kg'
},  # Etiquetas
    value=[min_payload, max_payload]  # Valor inicial del rango
),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                     values='class',  # Cambia 'Class' si tienes otro nombre
                     names='Launch Site',  # Cambia 'Launch Site' según tu DataFrame
                     title='Total Success Launches for All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        grouped_data = filtered_df.groupby('class').size().reset_index(name='count')
        print(f'hola>=: {entered_site}')
       
        fig = px.pie(
            grouped_data,
            names = 'class', # Muestra éxito (1) vs fallo (0)
            values='count',
            title=f'Total Success Launches for {entered_site}'
        )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    # Filtrar los datos según el rango del slider
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    # Verificar si se selecciona un sitio específico
    if selected_site == 'ALL':
        # Gráfico para todos los sitios
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites',
            labels={'Class': 'Launch Success'},
            hover_data=['Launch Site']
            
        )
        print(f'hola>=: {selected_site}')
    else:
        print(f'hola>=: {selected_site}')
        # Filtrar datos para el sitio seleccionado
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Gráfico para un sitio específico\
        fig = px.scatter(
            site_filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for {selected_site}',
            labels={'Class': 'Launch Success'},
            hover_data=['Payload Mass (kg)']
        )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
