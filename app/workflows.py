from typing import TypedDict
from tools import TOOL_REGISTRY

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
    code = state["code"]
    funcs = [line.strip() for line in code.split("\n") if line.strip().startswith("def ")]
    state["functions"] = funcs
    return state

# Node 2- Complexity checking
def check_complexity(state: Code_Review_State) -> Code_Review_State:
    funcs = state["functions"]
    if not funcs:
        state["avg_complexity"] = 0.0
        return state
    
    # Check out tools.py for this function's working-
    TOOL_REGISTRY["complexity_checker_tool"](funcs, state)
    return state

# Node 3- Detecting Issues
def detect_issues(state: Code_Review_State) -> Code_Review_State:
    code = state["code"]
    issues = code.count("TODO") + code.count("FIXME") + code.count("HACK") + code.count("BUG") + code.count("XXX") 
    state["issues"] = issues
    return state

# Node 4- Suggests Improvements
def suggest_improvements(state: Code_Review_State) -> Code_Review_State:
    suggestions = []
    
    #Check out the tools.py for it's working.
    TOOL_REGISTRY["quality_scorer_tool"](state)  
    
    #the if conditions to give suggestions.
    if state["issues"] > 0:
        suggestions.append(f"Remove and fix {state['issues']} TODO/FIXME comments present in code.")
    
    if state["avg_complexity"] > 10:
        suggestions.append(f"Reduce function complexity (current func avg: {state['avg_complexity']:.1f}). Keeping simple works.")
    
    if not state["functions"]:
        suggestions.append("No functions found, add functions/modularize code.")
    
    if state["quality_score"] < state["threshold"]:
        suggestions.append(f"Quality score {state['quality_score']:.1f} is below threshold {state['threshold']}, use some help from the web and write better functions to improve this score.")
    # above used state['quality_score'] instead of q coz q is out of scope here.
    
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




# At the bottom of your workflow.py file, add:

if __name__ == "__main__":
    # Test state
    test_state = {
        "code": """
def hello():
    pass

def complex_function():
    # TODO: optimize this
    # FIXME: bug here
    if True:afdggggggggggggggggggggg
    gas
    f
    gsadf
    gs
    dfhg
    sdf
    h
    sdgfh
    rety34w56y325
    46
        for i in range(10):
            print(i)
""",
        "functions": [],
        "avg_complexity": 0.0,
        "issues": 0,
        "quality_score": 0.0,
        "threshold": 80,
        "suggestions": []
    }
    
    print("Initial State:")
    print(f"Code length: {len(test_state['code'])} chars")
    print(f"Issues: {test_state['issues']}")
    print()
    
    # Run the workflow
    final_state = run_graph("extract_functions", edges, test_state)
    
    print("Final State:")
    print(f"Functions found: {len(final_state['functions'])}")
    print(f"Functions: {final_state['functions']}")
    print(f"Average complexity: {final_state['avg_complexity']:.2f}")
    print(f"Issues found: {final_state['issues']}")
    print(f"Quality score: {final_state['quality_score']:.2f}")
    print(f"Threshold: {final_state['threshold']}")
    print(f"\nSuggestions:")
    for suggestion in final_state['suggestions']:
        print(f"  - {suggestion}")