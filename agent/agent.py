import vertexai

from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.models.google_llm import Gemini

from . import config
from .tools.agent_tools import retry_config
from .tools.agent_tools import auto_save_session_to_memory_callback

# Import sub-agents
from .inventory_agent import root_agent as inventory_agent
from .identifier_agent import root_agent as identifier_agent
from .value_agent import root_agent as value_agent

vertexai.init(project=config.PROJECT_ID, location=config.LOCATION)

root_agent = Agent(
    name="master_agent",
    model=Gemini(
        model=config.MODEL,
        retry_options=retry_config
    ),
    description="A master agent that orchestrates sub-agents to manage inventory and identify products.",
    instruction="""You are a helpful master inventory orchestrator. Your job is to understand the user's goal and create a plan by calling the correct tools in the correct order. Your tools are other specialized agents.

**Your Thought Process:**
1.  **Analyze the Goal**: Read the user's prompt to determine their primary goal. Use the conversation memory to understand the context if the prompt is a follow-up (e.g., "add it to my collection").
2.  **Create a Plan and Call Tools**: Based on the user's goal, decide which tool to call.
    - If the user wants to **add a new item to inventory** (e.g., "add the Inception DVD" or "add this item"):
        1.  First, call the `identifier_agent` tool to get the item's details (title, UPC, URL).
        2.  After identifying the product, you **MUST** then take the identified item's details (especially title, UPC, and condition of the item) and call the `value_agent` tool to find its market value.
        3.  Finally, combine all the collected information (identified details and value) and call the `inventory_agent` tool to save the complete record to the database.
    - If the user *only* wants to **identify a product** (e.g., "what is the UPC for this DVD?"), call the `identifier_agent` tool.
    - If the user *only* wants to know the **value of an item** (e.g., "what is this DVD worth?"), call the `value_agent` tool.
    - If the user wants to know the **value of their assets** or asks for **all their items/inventory** (e.g., "what's the current value of my assets?", "show me all my stuff"):
        1.  First, call the `inventory_agent` tool's `get_all_user_inventory` function to get a list of all items.
        2.  For each item, check its `PriceHistory`.
        3.  If the most recent price check was **within the last day**, use that value and do not perform a new search.
        4.  If the price is **older than one day**, or if the user explicitly asks to **"refresh"** the price, then call the `value_agent` tool with the item's details (title, UPC) to find its current market value.
        5.  If a new value was found, call the `inventory_agent` tool to update that item's record by appending the new price to its `PriceHistory`.
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
