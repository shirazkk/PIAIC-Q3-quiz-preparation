"""
Practice Problems for Tools:
1. WebSearchTool: Search for Information
Problem: Create an agent that uses the WebSearchTool to search for information about a specific topic. The agent should ask the user for a topic and then return the top 3 search results.

Task:

Use the WebSearchTool to fetch search results.

Extract and return the top 3 search results based on the search query from the user.

Display the titles and URLs of the search results.

2. FileSearchTool: Search in Files
Problem: Create an agent that uses the FileSearchTool to search for a specific keyword in a set of files stored in your OpenAI vector store.

Task:

Use FileSearchTool with a vector store ID to search for documents containing a given keyword.

Return a list of file names or document summaries that contain the keyword.

3. CodeInterpreterTool: Execute Code
Problem: Build an agent that uses the CodeInterpreterTool to execute a Python code snippet provided by the user. The code could perform a simple operation like calculating the square of a number.

Task:

The agent should take user input for a Python code snippet (e.g., x = 5; x**2).

Use CodeInterpreterTool to run the Python code.

Return the output of the code execution (e.g., 25).

4. ImageGenerationTool: Generate Images
Problem: Use the ImageGenerationTool to create an agent that can generate images based on user-provided descriptions.

Task:

Ask the user for a prompt (e.g., "A sunset over the ocean").

Use the ImageGenerationTool to generate the image from the prompt.

Return the URL of the generated image.

5. LocalShellTool: Run Shell Commands
Problem: Build an agent that uses the LocalShellTool to run simple shell commands (e.g., listing files in a directory).

Task:

Ask the user for a shell command to run (e.g., ls to list files).

Use LocalShellTool to run the command on your local machine.

Return the output of the command (e.g., list of files in the directory).

6. Agents as Tools: Use Agents as Tools
Problem: Create a central agent (e.g., Orchestrator Agent) that can use other agents as tools to perform specific tasks, like translating text into Spanish and French.

Task:

Create two separate agents: SpanishAgent and FrenchAgent, which translate text into Spanish and French, respectively.

The Orchestrator Agent should use these two agents as tools to translate a given input text into both languages.

The orchestrator should call the relevant agents based on the user's request for translations.

7. Custom Function Tool: Process Data
Problem: Create a function tool that processes a dictionary of user data. The tool should receive data like username and age and return a formatted string with the user's information.

Task:

Define a custom function tool called process_user_data that accepts a username (str) and age (int).

Format the data into a string like "username is age years old".

Implement the tool using Pydantic to validate the inputs.

8. Error Handling in Function Tools: Handle Errors Gracefully
Problem: Create a function tool that reads a file, but handles errors (e.g., file not found) gracefully by sending a helpful error message back to the user.

Task:

Define a function tool read_file() that attempts to open and read a file.

Implement error handling to catch potential errors (e.g., FileNotFoundError) and return a user-friendly error message.

Use the failure_error_function parameter to handle errors and provide a custom error response.

9. Custom Output Extraction in Agent Tools:
Problem: Create a tool-agent that fetches data (e.g., weather data) and extracts specific information (e.g., temperature) from the result before returning it.

Task:

Use an agent that fetches weather data (could be a mock function).

Implement a custom output extractor to extract only the temperature from the response and return it to the user.

Use custom_output_extractor when calling the tool to clean up the output before returning it.

10. Orchestrator Agent with Multiple Tools:
Problem: Build an orchestrator agent that coordinates multiple tools to fetch and display information. For example, the agent should search for a topic on the web, then fetch related documents, and summarize the information.

Task:

Use the WebSearchTool to fetch information based on a user query.

Use the FileSearchTool to find relevant documents.

Combine the results and return a summary of the information.

How to Approach These Problems:
For Hosted Tools:

Use built-in tools like WebSearchTool or ImageGenerationTool in your agent and experiment with how to extract and display data.

For Function Tools:

Focus on creating function tools by defining the function signature, using Pydantic for input validation, and implementing custom logic.

For Agents as Tools:

Work on orchestrating different agents, enabling them to call each other without a direct handoff, allowing you to chain their behavior together.

For Customizing Output:

Practice customizing the output of tools by implementing custom output extraction or error handling.

Resources to Help You:
OpenAI SDK Documentation: Refer to the official OpenAI SDK docs for examples and detailed information about each tool.

Pydantic: Use Pydantic to manage input validation for your tools.

By working through these practice problems, you'll gain a deeper understanding of tools in the OpenAI Agent SDK and how to integrate them into your agents.

"""