from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
import vertexai
import os

# Import sub-agents
from .inventory_agent import root_agent as inventory_agent
from .identifier_agent import root_agent as identifier_agent
from .value_agent import root_agent as value_agent


PROJECT_ID = os.environ.get("PROJECT_ID", "")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "")

vertexai.init(project=PROJECT_ID, location=LOCATION)

async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)

root_agent = Agent(
    name="master_agent",
    model="gemini-2.5-pro",
    description="A master agent that orchestrates sub-agents to manage inventory and identify products.",
    instruction="""You are a helpful master inventory orchestrator. Your job is to understand the user's goal and create a plan by calling the correct tools in the correct order. Your tools are other specialized agents.

**Your Thought Process:**
1.  **Analyze the Goal**: Read the user's prompt to determine their primary goal. Use the conversation memory to understand the context if the prompt is a follow-up (e.g., "add it to my collection").
2.  **Create a Plan and Call Tools**: Based on the user's goal, decide which tool to call.
    - If the user wants to **add a new item to inventory** (e.g., "add the Inception DVD" or "add this item"):
        1.  First, call the `identifier_agent` tool to get the item's details (title, UPC, URL).
        2.  Next, take the identified item's details (especially title and UPC) and call the `value_agent` tool to find its market value.
        3.  Finally, combine all the collected information (identified details and value) and call the `inventory_agent` tool to save the complete record to the database.
    - If the user *only* wants to **identify a product** (e.g., "what is the UPC for this DVD?"), call the `identifier_agent` tool.
    - If the user *only* wants to know the **value of an item** (e.g., "what is this DVD worth?"), call the `value_agent` tool.
    - If the user wants to **update the value of all their assets** (e.g., "what's the current value of my assets?"):
        1.  First, call the `inventory_agent` tool to get a list of all items in the user's inventory.
        2.  Then, for each item returned, call the `value_agent` tool with its details (title, UPC) to find its current market value.
        3.  After finding the value for an item, call the `inventory_agent` tool to update that item's record, appending the new price to its `PriceHistory`.
    - For all other database tasks like **querying, updating, or deleting inventory**, call the `inventory_agent` tool.
3.  **Be Helpful**: Your primary role is to call your tools to accomplish the user's task. Do not try to answer questions directly, but use your understanding of the conversation to guide the user if their request is unclear.

""",
    tools=[
        AgentTool(agent=inventory_agent), 
        AgentTool(agent=identifier_agent), 
        AgentTool(agent=value_agent),
        PreloadMemoryTool()],
    after_agent_callback=auto_save_session_to_memory_callback,
)
