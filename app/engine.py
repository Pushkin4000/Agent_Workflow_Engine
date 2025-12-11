import uuid
from typing import Dict, Any, Optional
from app.workflows import NODE_REGISTRY

# In-memory stores
GRAPHS: Dict[str, Dict] = {}
RUNS: Dict[str, Dict] = {}


def create_graph(graph_def: Dict) -> str: #this will store and create uuid for a graph.
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = graph_def
    return graph_id


def get_graph(graph_id: str) -> Optional[Dict]: #will retrieve a graph by id.
    return GRAPHS.get(graph_id)

# will do exactly as the name suggests runs a graph and return final state, logs and status.
def run_graph(graph_id: str, initial_state: Dict[str, Any], max_steps: int = 100) -> Dict:
    graph = GRAPHS.get(graph_id)
    if graph is None:
        raise KeyError(f"Graph {graph_id} not found, please recheck the graph ID and try again.")
    
    run_id = str(uuid.uuid4())
    state = dict(initial_state)   
    logs = []
    current_node = graph["start_node"]
    step = 0
    status = "running"
    
    # Execute nodes
    while current_node is not None and step < max_steps:
        step += 1
        node_function = NODE_REGISTRY.get(current_node)
        
        if node_function is None:
            logs.append(f"Step {step}: ERROR, Node '{current_node}' not found")
            status = "failed"
            break
        
        try:
            state = node_function(state)
            logs.append(f"Step {step}: Executed '{current_node}'")
        except Exception as e:
            logs.append(f"Step {step}: ERROR in '{current_node}' - {str(e)}")
            status = "failed"
            break
        
        # Determining the next node. Either by _next in state or predefined edge.
        next_node = state.pop("_next", None)
        if next_node is None:
            next_node = graph["edges"].get(current_node)
        current_node = next_node
    
    #final status check
    if current_node is None:
        status = "finished"
        logs.append(f"Workflow completed in {step} steps.")
    elif step >= max_steps:
        status = "failed"
        logs.append(f"ERROR: Workflow stopped after {max_steps} steps (possible infinite loop or some internal error).")
    
    # Saveing the runs.
    RUNS[run_id] = {
        "graph_id": graph_id,
        "final_state": state,
        "logs": logs,
        "status": status
    }
    
    return {
        "run_id": run_id,
        "final_state": state,
        "logs": logs,
        "status": status
    }

# retrieve a run by its id.
def get_run(run_id: str) -> Optional[Dict]:
    return RUNS.get(run_id)