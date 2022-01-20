import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import base64
import datetime
import io
from os import listdir



# function for file formating
def Edge_dataformating(edge_df):
    if 'from' not in  edge_df.columns or 'to' not in  edge_df.columns:
        raise Exception("Edge dataframe missing 'from' or 'to' column.")
    nodes_list = list(set(list(edge_df['from'].unique()) + list(edge_df['to'].unique())))
    
    
    edge_df['id'] = edge_df['from'].str.cat(edge_df['to'], sep ="---")    
    edge_df['arrows'] = edge_df['id'].apply(lambda x : 'to')
    return edge_df , nodes_list



def Node_dataformating(edgesdf):
    if 'from' not in  edgesdf.columns or 'to' not in  edgesdf.columns:
        raise Exception("Edge dataframe missing 'from' or 'to' column.")
        
    temp1 = edgesdf.groupby(['from'], as_index=False).sum()
    temp2 = edgesdf.groupby(['to'], as_index=False).sum()
    temp2.rename(columns = {'to':'from'}, inplace = True)
    temp3 = temp1.append(temp2)
    if 'Edge_weight' in edgesdf.columns:
        temp3.rename(columns = {'from':'id', 'Edge_weight':'Node_weight' }, inplace = True)
    else:
        temp3.rename(columns = {'from':'id'}, inplace = True)
    temp3['label']= temp3['id'].apply(lambda x : x + '_label')
    
    node_df =   temp3.groupby(['id','label'], as_index=False).sum() 
    node_df['shape'] = node_df['id'].apply(lambda x : 'dot')
    return node_df
        
        
       
# input file format 
def Data_foramting(edge_df, node_df=None):
    edge_data , nodes_list = Edge_dataformating(edge_df)
    
    edges = edge_data.to_dict('records')
    if node_df is None:
        nodes_data = Node_dataformating(edge_df)
        nodes = nodes_data.to_dict('records')
    if node_df is not None:
        nodes = node_df.to_dict('records')
    dict_data  = {'node': nodes, 'edges': edges}
    return  dict_data, nodes_list

    

# function to find initial nodes
def initial_nodes(edges_df):
    # find unique nodes
    nodes_list = list(set(list(edges_df['from'].unique()) + list(edges_df['to'].unique())))
    # Build your graph
    G=nx.from_pandas_edgelist(edges_df, 'from', 'to')
 
    # Plot it to test 
    #nx.draw(G, with_labels=True)
    #plt.show()
    
    #find  sub graphs 
    connection_list = []
    for i in nodes_list:
        nodes = nx.shortest_path(G,i).keys()
        connection= list(nodes)
        connection_list.append(connection)  
    # sort the connetions by length
    connection_list.sort(key = len)
    
    initial_nodes = []
    sub_graph = []
    a= 0
    for connect in connection_list:
        if a != len(connect):
            a = len(connect)
            sub_graph.append(connect)
            initial_nodes.append(connect[0])
    return initial_nodes , sub_graph



# nodes and edges for coloring 
def Color_egdesnodes(edgesdf, nodedf=None):
    edge_columns = []
    rejectlist = ['id', 'from', 'to', 'arrows']
    edge_columns = edgesdf.columns
    

    edge_color = []
    for i in edge_columns:
        if edgesdf.dtypes[i] ==  object and i not in rejectlist:
            edge_color.append(i)
    
    if len(edge_color) ==0:
        edge_color = [None]
    
    
    node_color = []
    if nodedf is  None:
        return edge_color , node_color
    
    if nodedf is not None:
        node_columns = []
        rejectlist = ['id', 'label', 'from', 'to', 'shape']
        node_columns = nodedf.columns
        node_color = []
        for i in node_columns:
            if nodedf.dtypes[i] ==  object and i not in rejectlist:
                node_color.append(i)
    
         
        if len(node_color) ==0:
            node_color =None #

    return edge_color , node_color

 


# organize uploaded file 
def filefinding(contents , filename):
    
    if (len(contents)) ==2:
        if (filename.index('Edges.csv')) == 0:
            content_type, content_string = contents[0].split(',')
            decoded = base64.b64decode(content_string)
            edgesdf = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            
            content_type, content_string = contents[1].split(',')
            decoded = base64.b64decode(content_string)
            nodedf = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return edgesdf, nodedf
        
        if (filename.index('Edges.csv')) == 1:
            content_type, content_string = contents[1].split(',')
            decoded = base64.b64decode(content_string)
            edgesdf = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            
            content_type, content_string = contents[0].split(',')
            decoded = base64.b64decode(content_string)
            nodedf = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return edgesdf, nodedf
        
    
    if (len(contents)) ==1:
        filename[0] =='Edges.csv'
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)
        edgesdf = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        nodedf = None
        return edgesdf , nodedf
    else :
        edgesdf = None
        nodedf = None
               
slectedNode_list = []
def networkgraph(edgesdf, nodedf, ip_Node):
        
    mydata1, nodes_list = Data_foramting(edgesdf, nodedf)
    edges_color , nodes_color  = Color_egdesnodes(edgesdf, nodedf)
    
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
        #mydata ={'nodes':[ mydata1['node'][0], mydata1['node'][5], mydata1['node'][6] ],
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
