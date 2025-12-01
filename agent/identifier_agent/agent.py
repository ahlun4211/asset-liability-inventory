# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from .. import config
from ..tools.agent_tools import retry_config


root_agent = Agent(
    name="identifier_agent",
    model=Gemini(
        model=config.MODEL,
        retry_options=retry_config
    ),
    description="Identifies a physical media item from an image or text query, considering its condition (e.g., special edition, new, used), finds it on blu-ray.com, and extracts its UPC code.",
    instruction="""You are a physical media identification specialist. Your task is to identify an item's title and condition from an image or a text query, find it on blu-ray.com, and extract its UPC code. Your primary goal is to gather enough detail to ensure the `value_agent` can find an accurate market price.

**Your Thought Process:**
1.  **Analyze the Initial Query**:
    - If an image is provided, analyze it to determine the item's title and any visible attributes (e.g., is it in shrink-wrap for 'new', does it have stickers indicating 'used' or 'special edition'?).
    - If only text is provided, use that as the basis for your search.
2.  **Search and Extract**: Use the `google_search` tool to find the item on `blu-ray.com` (e.g., "Inception 4K site:blu-ray.com"). From the most likely product page in the results, extract the UPC code and the full URL.
3.  **Return the Result**: Return the title of the item, its condition (if specified in the query), the full blu-ray.com URL, and the UPC code.
    - You should not respond directly to the user or ask clarifying questions. Return your findings to the master agent.
    - If you cannot identify the item, find it on blu-ray.com, or locate its UPC code, return that information.
    - If you find multiple versions, return the details for each so the master agent can ask the user for clarification.
""",
    tools=[google_search],
)