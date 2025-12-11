
def complexity_checker_tool(funcs, state):
    scores = [len(f) / 10 for f in funcs]
    avg = sum(scores) / len(scores)
    state["avg_complexity"] = avg
    

def quality_scorer_tool(state):
    q = 100 - state["issues"]*10 - state["avg_complexity"]*5
    q = max(0, q) 
    state["quality_score"] = q    



TOOL_REGISTRY = {
"complexity_checker_tool": complexity_checker_tool,
"quality_scorer_tool": quality_scorer_tool,
}    