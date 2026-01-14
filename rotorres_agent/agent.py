import os
from google.adk.agents import Agent
from google.adk.tools import google_search, AgentTool
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {os.environ.get('GIT_TOKEN')}",
        },
    ),
    tool_filter=[
        "list_repositories",
        "search_repositories",
        "search_issues",
        "list_issues",
        "get_issue",
        "list_pull_requests",
        "get_pull_request",
    ],
)

github_agent = Agent(
    name="github_specialist",
    model="gemini-2.5-flash",
    description="Specialist in GitHub information retrieval.",
    instruction="You are an expert at navigating GitHub. Use your tools to find repositories, code, issues, PR data or anything else related to github.",
    tools=[mcp_tools],
)

search_agent = Agent(
    name="web_search_specialist",
    model="gemini-2.5-flash",
    description="Specialist in searching the web for general information and documentation.",
    instruction="You are a research assistant. Use Google Search to find up-to-date information.",
    tools=[google_search],
)

agent_instruction = """
You are the lead engineer for QuantumRoast. 
Your goal is to triage issues by coordinating your team:
1. Use the 'web_search_specialist' for general technical documentation or external coffee machine specs.
2. Use the 'github_specialist' to look into our internal code, issues, and PRs.
Combine information from both to provide a final expert report.
"""

root_agent = Agent(
    name="rotorres_sample_agent",
    model="gemini-2.5-flash",
    description="Lead coordinator for QuantumRoast engineering tasks.",
    instruction=agent_instruction,
    # We pass the agents as TOOLS to the manager
    tools=[
        AgentTool(agent=github_agent),
        AgentTool(agent=search_agent)
    ],
)

from google.adk.apps.app import App
app = App(root_agent=root_agent, name="rotorres_sample_agent")