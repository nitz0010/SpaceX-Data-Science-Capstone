import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import io

# --- PART 1: DATA LOADING & CLEANING ---
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
try:
    s = requests.get(url).content
    spacex_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    
    # Standardizing Launch Site Names to match Dropdown options
    # This ensures "KSC LC-39A" matches regardless of CSV formatting
    if 'Launch Site' not in spacex_df.columns:
        spacex_df.rename(columns={'LaunchSite': 'Launch Site'}, inplace=True)
    
    # Cleaning site names to ensure they match our dropdown exactly
    spacex_df['Launch Site'] = spacex_df['Launch Site'].str.replace('  ', ' ').str.strip()
    
except Exception as e:
    print(f"Error loading data: {e}")

max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

# --- PART 2: DASH APP LAYOUT ---
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown
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

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Range Slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # TASK 4: Scatter chart
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
    # Filter dataset by payload slider range
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
        # Filter data for specific site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # Pie Chart: Success (1) vs Failure (0)
        # We use names='Class' to show the split for that specific site
        fig1 = px.pie(site_df, names='Class', 
                      title=f'Success (1) vs Failure (0) for site {entered_site}')
        
        # Scatter Chart: Filtered by site AND payload range
        site_scatter_df = df_filtered[df_filtered['Launch Site'] == entered_site]
        fig2 = px.scatter(site_scatter_df, x="PayloadMass", y="Class", 
                          color="BoosterVersion",
                          title=f'Payload vs. Outcome for site {entered_site}')
    
    return fig1, fig2

# --- PART 4: RUN APP ---
if __name__ == '__main__':
    # Use app.run() for newer versions of Dash/Python
    app.run(debug=True)
