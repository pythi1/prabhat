# from fastapi import FastAPI, Form

# app = FastAPI()

# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}

# @app.get('/pipelines/parse')
# def parse_pipeline(pipeline: str = Form(...)):
#     return {'status': 'parsed'}

from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import networkx as nx
import json

app = FastAPI()

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: str = Form(...)):
    try:
        # Convert the pipeline string to a dictionary
        pipeline_data = json.loads(pipeline)
        nodes = pipeline_data.get("nodes", [])
        edges = pipeline_data.get("edges", [])
        
        # Calculate number of nodes and edges
        num_nodes = len(nodes)
        num_edges = len(edges)
        
        # Create directed graph and add nodes and edges
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        # Check if the graph is a DAG
        is_dag = nx.is_directed_acyclic_graph(G)
        
        return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid pipeline format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
