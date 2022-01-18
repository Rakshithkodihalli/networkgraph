# Application buiding using dash #
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import visdcc
#from demos import dash_reusable_components as drc
from  preprocess import  initial_nodes, Data_foramting , Color_egdesnodes , networkgrapg, filefinding
import numpy as np
import sys
import os
import pandas as pd
from layout  import *


app = dash.Dash(__name__, )
server = app.server

app.layout = get_app_layout()


@app.callback([Output('net', 'data')],
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              Input('submit_', 'n_clicks'),
              Input('net', 'selection'))



def upload_data(contents, filename, date,  n_clicks, ip_Node):
    
    if (n_clicks ==0) or (contents is None and n_clicks >0):
        edgesdf= pd.read_csv('data/Edges1_.csv')
        nodedf = pd.read_csv('data/Node1_.csv')
        mydata = networkgrapg(edgesdf , nodedf, ip_Node)
        return(mydata)
            
    if (contents is not None and n_clicks >=1):
        edgesdf , nodedf = filefinding(contents, filename)
        mydata = networkgrapg(edgesdf , nodedf, ip_Node)
        return(mydata)
    
  
       
    
if __name__ == '__main__':   
    app.run_server(debug=True)
    


