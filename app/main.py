from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.engine import create_graph, run_graph, get_run

app = FastAPI()


# Data models
class GraphCreate(BaseModel):
    nodes: list
    edges: Dict[str, Optional[str]]
    start_node: str


class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


# Endpoint for creating ids and making graphs.
@app.post("/graph/create")
def create_new_graph(payload: GraphCreate):
    try:
        graph_def = {
            "nodes": payload.nodes,
            "edges": payload.edges,
            "start_node": payload.start_node
        }
        graph_id = create_graph(graph_def)
        return {"graph_id": graph_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for running existing graphs.
@app.post("/graph/run")
def run_existing_graph(payload: RunRequest):
    try:
        result = run_graph(payload.graph_id, payload.initial_state)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail="Graph not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint for retrieving run state by run id.
@app.get("/graph/state/{run_id}")
def get_run_state(run_id: str):
    result = get_run(run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")
    return result