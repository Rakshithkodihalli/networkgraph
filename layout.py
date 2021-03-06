import os
import visdcc
import base64
import dash
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc






# Constants
# --------------
# default node and edge size
#DEFAULT_NODE_SIZE = 1
#DEFAULT_EDGE_SIZE = 1

# default node and egde color
#DEFAULT_COLOR = '#FFB300'


#colors = {
#    'background': '#817066',
#    'text': '#7FDBFF'
#}




# Taken from https://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors
KELLY_COLORS_HEX = [
    "#FFB300",  # Vivid Yellow
    "#803E75",  # Strong Purple
    "#FF6800",  # Vivid Orange
    "#A6BDD7",  # Very Light Blue
    "#C10020",  # Vivid Red
    "#CEA262",  # Grayish Yellow
    "#817066",  # Medium Gray
    # The following don't work well for people with defective color vision
    "#007D34",  # Vivid Green
    "#F6768E",  # Strong Purplish Pink
    "#00538A",  # Strong Blue
    "#FF7A5C",  # Strong Yellowish Pink
    "#53377A",  # Strong Violet
    "#FF8E00",  # Vivid Orange Yellow
    "#B32851",  # Strong Purplish Red
    "#F4C800",  # Vivid Greenish Yellow
    "#7F180D",  # Strong Reddish Brown
    "#93AA00",  # Vivid Yellowish Green
    "#593315",  # Deep Yellowish Brown
    "#F13A13",  # Vivid Reddish Orange
    "#232C16",  # Dark Olive Green
    ]


DEFAULT_OPTIONS = {
    'height': '600px',
    'width': '100%',
    'interaction':{'hover': True},
    'edges': {'scaling': {'min': 1, 'max': 5}},
    'physics':{'stabilization':{'iterations': 100}},       
}



def fetch_flex_row_style():
    return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'}


def create_row(children, style=fetch_flex_row_style()):
    return dbc.Row(children,
                   style=style,
                   className="column flex-display")
    
    
def get_options():
    opts = DEFAULT_OPTIONS.copy()
    return opts
    
    
    
    
def get_app_layout():
    nodes_color = ['A', 'B']
    encoded_image = base64.b64encode(open((os.path.join(os.path.dirname(__file__), 'assest/logo.PNG')), 'rb').read())
    return  html.Div([
            (html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width="45px")),
            dcc.Upload(id='upload-data',children=html.Div(['Drag and Drop or ',html.A('Select Files')]),
            style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px' },
        # Allow multiple files to be uploaded
        multiple=True ),
        html.Button('Submit', id='submit_', n_clicks=0),
        html.Button('Reset',id='reset_button', n_clicks=0),
        #html.Div(id='file loaded'),

        #create_row([dbc.Col([dbc.Form([html.H6("Color nodes/Edges")]),
        # color Node by feature  
        #dcc.Dropdown(
        #id='dropdown',
        #options=[{'label': i, 'value': i} for i in edges_color], value=None),
        #dcc.Dropdown(id='dropdown2',options=[{'label': i, 'value': i} for i in nodes_color],value=None),
        #html.Div(id = 'nodes'),
        #html.Div(id = 'unselectednodes')
                #]),
      #visdcc.Network(id = 'net',selection = {'nodes':[], 'edges':[]},  options = dict(height= '600px', width= '100%')),
      visdcc.Network(id = 'net',selection = {'nodes':[], 'edges':[]}, options = get_options())     
      ])




