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

from google.adk.tools import ToolContext
from typing import Callable


class UserTools:
    """A class that provides tools for managing user context."""

    def get_current_user_id(self, tool_context: ToolContext) -> dict[str, str]:
        """
        Gets the user ID for the current session. Use this to confirm the user's identity if needed.

        Args:
            tool_context: The context of the tool invocation.

        Returns:
            A dictionary containing the user ID or an error if not found.
        """
        user_id = tool_context.state.get("user_id") or "1"
        return {"user_id": user_id}

    def set_user_id(self, new_user_id: str, tool_context: ToolContext) -> str:
        """
        Sets or updates the user ID for the current session. Use this when a user wants to switch context.

        Args:
            new_user_id: The new user ID to set for the session.
            tool_context: The context of the tool invocation.
        """
        tool_context.state["user_id"] = new_user_id
        return f"User ID for this session has been updated to '{new_user_id}'."

    def get_tools(self) -> list[Callable]:
        """Returns a list of all tool methods."""
        return [
            self.get_current_user_id,
            self.set_user_id,
        ]