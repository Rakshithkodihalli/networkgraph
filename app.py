# Application buiding using dash #
import dash
from dash.dependencies import Input, Output, State
from  preprocess import  initial_nodes, Data_foramting ,  filefinding
import numpy as np
import sys
import os
import pandas as pd
from layout  import *




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server = app.server
app.layout = get_app_layout




slectedNode_list = []
def networkgraph(edgesdf, nodedf, ip_Node):
        
    mydata1, nodes_list = Data_foramting(edgesdf, nodedf)
    #edges_color , nodes_color  = Color_egdesnodes(edgesdf, nodedf)

    # calling initial node list 
    first_clusternodes , sub_graph= initial_nodes(edgesdf)
    
    # calling initial node dict object 
    initial_nodeDict = []
    for i in mydata1['node']:
        if (i['id']) in first_clusternodes:
            initial_nodeDict.append(i)
         
        
    op_node = 'Selected nodes : '
    # Display initial clusters [Before any node selection]
    if len(ip_Node['nodes']) ==0:
        mydata ={'nodes':initial_nodeDict, 'edges':[]}        
        return [ mydata ] 
   
   
        # Display nodes and edges on user choose [ Atlest one node selection]
    if len(ip_Node['nodes']) > 0 :
        #print("start")
        op_node += str(ip_Node['nodes'][0])  
        node_selected = op_node.split(":")[1].replace(" ", "")
        slectedNode_list.append(node_selected)
        
        
      
        
        if ip_Node['nodes'][0] == node_selected:
                unique_groupNode = np.unique(slectedNode_list)
                # edge filtering
                z = []
                edges = []
                for i in mydata1['edges']:
                    if (i['from']) in unique_groupNode  or (i['to'] in unique_groupNode):
                        x = i['from']
                        y = i['to']
                        z.append(x)
                        z.append(y)
                        edges.append(i)
                node_list = list(set(z))
                # cluster_nodes contains all nodes   selected nodes  +  free suspended nodes 
                node_list.extend(first_clusternodes)
                
                #node filtering
                node = []
                for i in mydata1['node']:
                    if (i['id']) in node_list:
                        node.append(i)
        
                # parsing new nodes and edges to display network graph     
                mydata ={ 'nodes':node,'edges':edges }
               
                   # parse  unexplored nodes            
                if node_selected in nodes_list:
                    nodes_list.remove(node_selected)
                unclicked = [i   for i in nodes_list]
                unexplorednodes = "Unselected Node: " + str(unclicked)
                #print("end") 
                #return [op_node, mydata,unexplorednodes ]             
                #return [op_node, mydata]
        return [ mydata]








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
    app.run_server(debug=False)
    #app.run_server(debug=True)
    
    
    
    


