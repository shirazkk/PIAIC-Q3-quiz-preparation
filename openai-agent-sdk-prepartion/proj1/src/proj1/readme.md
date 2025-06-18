# Project 2: Task Manager with Tool Forcing and Hooks

## Description:
Create a task management system where an agent processes user requests to add tasks, check due dates, or mark tasks as complete. Use a single agent with multiple tools, force tool use for specific actions, and add lifecycle hooks to log events. Process results to display structured outputs and handle errors.

## Requirements:

### Agents:
- Create a TaskAgent with tools: add_task, check_due_date, and mark_complete.
- Use a Pydantic model (e.g., TaskResponse) for structured outputs (fields: task_id, action, details).
- Force tool use with ModelSettings.tool_choice for specific inputs (e.g., “add” forces add_task).
- Add a custom AgentHooks class to log when the agent starts and when tools are called.

### Running Agents:
- Use Runner.run_sync() for simplicity.
- Set a run_config with max_turns=3 and a custom workflow_name.

### Results:
- Access final_output to display the structured task response.
- Log raw_responses to inspect LLM outputs.
- Handle exceptions like ModelBehaviorError for invalid outputs.
- Use last_agent to confirm the agent (should always be TaskAgent since no handoffs).

## Expected Output:

### Input: 
“Add a task: Finish report by tomorrow.”

### Output:
```json
{
  "task_id": "T001",
  "action": "add",
  "details": "Task 'Finish report' added, due tomorrow."
}
```

## Log:
Shows hook events (e.g., “Agent started”, “Tool add_task called”) and raw LLM responses.

## Error handling:
Catches and displays any ModelBehaviorError.

## Tasks for You:
- Define the Pydantic model and tools.
- Implement the hooks to log events.
- Write the main logic to run the agent, process results, and handle exceptions.
- Test with inputs like “Check due date for T001” and verify structured outputs.
