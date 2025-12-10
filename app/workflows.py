from typing import TypedDict

# The state model 

class Code_Review_State(TypedDict):
    code: str
    functions: list
    avg_complexity: float
    issues: int
    quality_score: float
    threshold: int
    suggestions: list


# Node 1- Extracting functions  
def extract_functions(state: Code_Review_State) -> Code_Review_State:
    code = state.code
    funcs = [line.strip() for line in code.split("\n") if line.strip().startswith("def ")]
    state.functions = funcs
    return state

# Node 2- Complexity checking
def check_complexity(state: Code_Review_State) -> Code_Review_State:
    funcs = state.functions
    if not funcs:
        state["avg_complexity"] = 0.0
        return state
    
    scores = [len(f) / 10 for f in funcs]
    avg = sum(scores) / len(scores)
    state["avg_complexity"] = avg
    return state

# Node 3- Detecting Issues
def detect_issues(state: Code_Review_State) -> Code_Review_State:
    code = state.code
    issues = code.count("TODO") + code.count("FIXME") + code.count("HACK") + code.count("BUG") + code.count("XXX") 
    state.issues = issues
    return state

# Node 4- Suggests Improvements
def suggest_improvements(state: Code_Review_State) -> Code_Review_State:
    suggestions = []
    
    #quality score
    q = 100 - state["issues"]*10 - state["avg_complexity"]*5
    q = max(0, q) 
    state["quality_score"] = q
    
    
    if state["issues"] > 0:
        suggestions.append(f"Remove {state['issues']} TODO/FIXME comments")
    
    if state["avg_complexity"] > 10:
        suggestions.append(f"Reduce function complexity (current func avg: {state['avg_complexity']:.1f})")
    
    if not state["functions"]:
        suggestions.append("No functions found, add functions")
    
    if state["quality_score"] < state["threshold"]:
        suggestions.append(f"Quality score {q:.1f} is below threshold {state['threshold']}, use some help from the web.")
    
    state["suggestions"] = suggestions
    return state


NODE_REGISTRY = {
    "extract_functions": extract_functions,
    "check_complexity": check_complexity,
    "detect_issues": detect_issues,
    "suggest_improvements": suggest_improvements
}


edges = {
    "extract_functions": "check_complexity",
    "check_complexity": "detect_issues",
    "detect_issues": "suggest_improvements",
    "suggest_improvements": None
}


def run_graph(start_node: str, edges: dict, state: dict, max_steps: int = 100):
    current = start_node
    step = 0
    while current is not None and step < max_steps:
        step += 1
        fn = NODE_REGISTRY.get(current)
        if fn is None:
            raise RuntimeError(f"Node {current} not registered")
        state = fn(state)
        
        next_node = state.pop("_next", None)
        if next_node is None:
            next_node = edges.get(current)
        current = next_node
    return state

