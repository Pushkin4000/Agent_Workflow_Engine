# AGENT_WORKFLOW_ENGINE 

A minimal workflow engine for automated code review with looping and branching capabilities.

## How to Run

### 1. Install Dependencies
```bash
pip install -r .\requirements.txt
```

### 2. Start the Server
```bash
python -m uvicorn app.main:app --reload
```
Server will run at `http://localhost:8000`
add .doc at the end to test the api

### 3. Use the API (3 Steps)

#### **Step 1: Create Graph** 
`POST /graph/create`

```json
{
  "nodes": [
    "extract_functions",
    "check_complexity",
    "detect_issues",
    "suggest_improvements",
    "check_and_loop"
  ],
  "edges": {
    "extract_functions": "check_complexity",
    "check_complexity": "detect_issues",
    "detect_issues": "suggest_improvements",
    "suggest_improvements": "check_and_loop",  
    "check_and_loop": null
  },
  "start_node": "extract_functions"
}

```
**Response:** `{"graph_id": "abc-123-def"}` #example or use the Payload_1st_Endpoint copy that.
→ **Copy this `graph_id` for Step 2**

---

#### **Step 2: Run Graph**
`POST /graph/run`

```json
{
  "graph_id": "your-graph-id-from-step-1", 
  "initial_state": {
    "code": "def hello():\n    pass\n\ndef test():\n    # TODO: fix\n    pass",
    "functions": [],
    "avg_complexity": 0.0,
    "issues": 0,
    "quality_score": 0.0,
    "threshold": 80,
    "suggestions": [],
    "loop_count": 0
  }
}
```
**Response:** `{"run_id": "xyz-789-uvw", "final_state": {...}, "logs": [...], "status": "completed"}`  
→ **Copy this `run_id` for Step 3**

---

#### **Step 3: Get Results**
`GET /graph/state/{run_id}`

Example: `GET /graph/state/xyz-789-uvw`

**Response:** Returns complete execution results with final state, logs, and status.

---

## What the Workflow Engine Supports

### Core Features
- **Nodes**: Python functions that process shared state
- **State Management**: Dictionary flows through all nodes
- **Edges**: Define execution order between nodes
- **Branching**: Conditional routing based on state values (via `_next` in state)
- **Looping**: Workflow loops until quality threshold is met for (max 3 iterations)
- **Tool Registry**: Reusable functions (complexity checker, quality scorer)

### Code Review Workflow
1. **Extract Functions** - Finds all function definitions
2. **Check Complexity** - Calculates average function complexity
3. **Detect Issues** - Counts TODO/FIXME/HACK/BUG comments
4. **Suggest Improvements** - Generates actionable feedback
5. **Check & Loop** - Loops back if quality < threshold (max 3 times)

### API Endpoints
- `POST /graph/create` - Create new workflow graph
- `POST /graph/run` - Execute workflow with initial state
- `GET /graph/state/{run_id}` - Retrieve execution results

---

## What I Would Improve With More Time

### High Priority
1. **Persistent Storage** - Use PostgreSQL/SQLite instead of in-memory storage
2. **WebSocket Streaming** - Real-time log streaming during execution
3. **Async Execution** - Run long workflows as background tasks
4. **Better Error Handling** - Retry logic, detailed error messages

### Additional Features
5. **Parallel Node Execution** - Run independent nodes concurrently
6. **Dynamic Tool Registration** - API endpoint to add tools at runtime
7. **Workflow Visualization** - Generate diagrams of node execution


---

## Project Structure
```
app/
├── main.py          # FastAPI endpoints
├── engine.py        # Graph execution engine
├── workflows.py     # Node definitions (code review logic)
└── tools.py         # Reusable tools (complexity, quality scoring)
```

---

## Example Output

After running the workflow, you'll get:

```json
{
  "run_id": "xyz-789",
  "final_state": {
    "functions": ["def hello():", "def test():"],
    "avg_complexity": 3.5,
    "issues": 2,
    "quality_score": 82.5,
    "suggestions": ["✓ Quality threshold met!"],
    "loop_count": 1
  },
  "logs": [
    "Step 1: Executed 'extract_functions'",
    "Step 2: Executed 'check_complexity'",
    "Step 3: Executed 'detect_issues'",
    "Step 4: Executed 'suggest_improvements'",
    "Step 5: Executed 'check_and_loop'",
    "Workflow completed in 5 steps"
  ],
  "status": "completed"
}
```