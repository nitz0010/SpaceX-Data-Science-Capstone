import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import io

# --- PART 1: DATA LOADING (AUTO-DOWNLOAD) ---
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
try:
    s = requests.get(url).content
    spacex_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    # The dataset uses 'Class' for success (1) and failure (0)
    # We create a 'Launch Site' column if it's named differently in the CSV
    if 'Launch Site' not in spacex_df.columns and 'LaunchSite' in spacex_df.columns:
        spacex_df.rename(columns={'LaunchSite': 'Launch Site'}, inplace=True)
except Exception as e:
    print(f"Error loading data: {e}")

max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

# --- PART 2: DASH APP LAYOUT ---
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown for Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Pie chart for success counts
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # TASK 4: Scatter chart for Payload vs. Success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# --- PART 3: CALLBACK FUNCTIONS ---
@app.callback(
    [Output(component_id='success-pie-chart', component_property='figure'),
     Output(component_id='success-payload-scatter-chart', component_property='figure')],
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_graphs(entered_site, payload_range):
    low, high = payload_range
    # Filter data by payload
    df_filtered = spacex_df[(spacex_df['PayloadMass'] >= low) & (spacex_df['PayloadMass'] <= high)]
    
    if entered_site == 'ALL':
        # Pie Chart for ALL sites
        fig1 = px.pie(spacex_df, values='Class', 
                      names='Launch Site', 
                      title='Total Success Launches By Site')
        # Scatter Chart for ALL sites
        fig2 = px.scatter(df_filtered, x="PayloadMass", y="Class", 
                          color="BoosterVersion",
                          title='Correlation between Payload and Success for all Sites')
    else:
        # Pie Chart for SPECIFIC site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Calculate success vs failure counts
        success_counts = site_df['Class'].value_counts().reset_index()
        success_counts.columns = ['Class', 'count']
        fig1 = px.pie(success_counts, values='count', 
                      names='Class', 
                      title=f'Total Success Launches for site {entered_site}')
        
        # Scatter Chart for SPECIFIC site
        site_scatter_df = df_filtered[df_filtered['Launch Site'] == entered_site]
        fig2 = px.scatter(site_scatter_df, x="PayloadMass", y="Class", 
                          color="BoosterVersion",
                          title=f'Correlation between Payload and Success for {entered_site}')
    
    return fig1, fig2

# --- PART 4: RUN APP ---
if __name__ == '__main__':
    # 'run_server' is now just 'run' in newer Dash versions
    app.run(debug=True)