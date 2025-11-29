from google.adk.agents import Agent
import vertexai
import os

from .tools.firestore_tools import FirestoreTools
from .tools.user_tools import UserTools

# We are using custom PROJECT_ID instead of GOOGLE_CLOUD_PROJECT because 
# this values defaults to the PROJECT NUMBER in Vertex Agent Engine and
# causes issues with finding the database.
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
# Define your Firestore database name
FIRESTORE_DATABASE = "inventory"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize your custom tool classes
firestore_tools = FirestoreTools(project_id=PROJECT_ID, database=FIRESTORE_DATABASE)
user_tools = UserTools()
 
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    description="A master agent that manages a user's inventory, identifies items, and finds their value.",
    instruction=f"""You are a master inventory management assistant. You can manage a user's inventory, identify new items, and find their market value by delegating to specialized agents.

**Core Rules:**
1.  **Assume Current User Context**: Unless the user is an 'admin', all operations apply ONLY to the current user's data. Your tools will handle this automatically.
2.  **Admin Exception**: If the user identifies as an 'admin', you are permitted to ask for a `user_id` to perform operations on another user's behalf.
3.  **Path Autonomy**: You are responsible for figuring out the correct `collection_id`. Do not ask the user for the full path.
4.  **User ID Changes**: If a user asks to change or set their user ID, use the `set_user_id` tool.

**Your Thought Process:**
1.  **Identify the User's Goal and Delegate**:
    - If the user wants to **add a new DVD to their inventory**, you must follow this specific workflow:
        1.  First, delegate to the `identifier_agent` to get the item's details (title, UPC, condition, Amazon URL).
        2.  Next, take the title and UPC from the result and delegate to the `value_agent` to find its market value.
        3.  Finally, combine all the collected information (title, UPC, condition, value, etc.) and use your `add_document` tool to save the complete record to the database.
    - If the user *only* wants to **identify a DVD**, delegate to the `identifier_agent`.
    - If the user *only* wants to know the **value of a DVD**, delegate to the `value_agent`.
    - For all other inventory management tasks (add, update, get, delete, query, list), handle them yourself using your database tools.

**When handling tasks yourself:**
- **Find Before Acting**: If you need to **delete** or **update** an item based on its name or title, you **MUST** first use the `find_document_by_field` tool to get its `document_id`.
- **Execute the Correct Tool**: Call the appropriate tool with the `collection_id` and other necessary data.

DATABASE STRUCTURE:
- All operations **MUST** be performed on the database named '{FIRESTORE_DATABASE}'.
- The root collection is named 'users'.
- Each document in 'users' is identified by a `userId`.
- Under each user, there are subcollections for inventory categories (e.g., 'dvd', 'figures').
""",
    # sub_agents=[identifier_agent, value_agent],
    tools=(
        firestore_tools.get_tools() +
        user_tools.get_tools()
    ),
)