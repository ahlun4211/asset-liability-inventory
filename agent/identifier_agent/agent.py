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
from google.genai import types
from google.adk.tools import google_search

# import vertexai
# import os

# We are using custom PROJECT_ID instead of GOOGLE_CLOUD_PROJECT because 
# this values defaults to the PROJECT NUMBER in Vertex Agent Engine and
# causes issues with finding the database.
# PROJECT_ID = os.environ["PROJECT_ID"]
# LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]

# vertexai.init(project=PROJECT_ID, location=LOCATION)

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

root_agent = Agent(
    name="identifier_agent",
    model=Gemini(
        model="gemini-2.5-pro",
        retry_options=retry_config),
    description="Identifies a physical media item from an image or text query, considering its condition (e.g., special edition, new, used), finds it on blu-ray.com, and extracts its UPC code.",
    instruction="""You are a physical media identification specialist. Your task is to identify an item's title and condition from an image or a text query, find it on blu-ray.com, and extract its UPC code.

**Your Thought Process:**
1.  **Determine the Item's Title and Condition**:
    - If an image is provided, analyze it to determine the item's title and assess its visual condition (e.g., is it in shrink-wrap for 'new', does it have stickers indicating 'used' or 'special edition'?).
    - If only text is provided, use the text as the title.
2.  **Search and Extract**: Use the `google_search` tool to find the item on `blu-ray.com` (e.g., "Inception 4K site:blu-ray.com"). From the most likely product page in the results, extract the UPC code and the full URL.
3.  **Return the Result**: Respond with the title of the item, its condition (if specified), the full blu-ray.com URL, and the UPC code.
    - If you cannot identify the item, find it on blu-ray.com, or locate its UPC code, state that clearly.
    - If you find multiple versions, provide details for each (like UPC, image, or other identifiers) to help the user verify the correct one.
""",
    tools=[google_search],
)