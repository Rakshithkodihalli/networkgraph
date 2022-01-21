# Application buiding using dash #
import dash
from dash.dependencies import Input, Output, State
from  preprocess import  initial_nodes, Data_foramting ,  filefinding, networkgraph ,slectedNode_list
import numpy as np
import sys
import os
import pandas as pd
from layout  import *




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server = app.server
app.layout = get_app_layout




@app.callback([Output('net', 'data')],
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              Input('submit_', 'n_clicks'),
              Input('net', 'selection'))


def upload_data(contents, filename, date,  n_clicks, ip_Node):
    if (n_clicks ==0) or (contents is None and n_clicks > 0):
        edgesdf= pd.read_csv('data/edgess.csv')
        nodedf = pd.read_csv('data/nodee.csv')
        mydata = networkgraph(edgesdf , nodedf, ip_Node)       
        return(mydata)
            
    if (contents is not None and n_clicks >=1):
        edgesdf , nodedf = filefinding(contents, filename)
        mydata = networkgraph(edgesdf , nodedf, ip_Node)
        #print(mydata)
        return(mydata)
    

@app.callback([Output('submit_','n_clicks'), Output('net', 'selection')],
             Input('reset_button','n_clicks'))

def update(reset):
    slectedNode_list.clear()
    return 0,  {'nodes': [], 'edges': []}
    
    
    
if __name__ == '__main__':   
    #app.run_server(debug=False)
    app.run_server(debug=True)
    
    
    
    


