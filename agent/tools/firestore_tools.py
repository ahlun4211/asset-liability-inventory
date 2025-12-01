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

from google.cloud import firestore
from typing import Any, Callable, Optional
from google.adk.tools import ToolContext


class FirestoreTools:
    """A class that provides tools for interacting with a Firestore database."""

    def __init__(self, project_id: str, database: str):
        """
        Initializes the Firestore client.

        Args:
            project_id: The Google Cloud project ID.
            database: The name of the Firestore database.
        """
        self.db = firestore.Client(project=project_id, database=database)

    def get_document(
        self,
        collection_id: str,
        document_id: str,
        tool_context: ToolContext,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Fetches a document from a specified Firestore path.

        Args:
            collection_id: The ID of the inventory category (e.g., 'dvd', 'figures').
            document_id: The ID of the document to retrieve.
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        user_id = user_id or tool_context.state.get("user_id") or "1"
        document_path = f"users/{user_id}/{collection_id}/{document_id}"
        doc_ref = self.db.document(document_path)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else {"error": "Document not found."}

    def add_document(
        self,
        collection_id: str,
        data: dict[str, Any],
        tool_context: ToolContext,
        user_id: Optional[str] = None,
        document_id: Optional[str] = None,
    ) -> str:
        """
        Adds a new document to a Firestore collection. If no document_id is provided, one will be auto-generated.

        Args:
            collection_id: The ID of the inventory category (e.g., 'dvd', 'figures').
            data: A dictionary containing the data for the new document.
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            document_id: The ID for the new document. If omitted, a random ID will be generated.
            tool_context: The context of the tool invocation.
        """
        try:
            user_id = user_id or tool_context.state.get("user_id") or "1"
            collection_path = f"users/{user_id}/{collection_id}"
            doc_ref = self.db.collection(collection_path).document(document_id)
            doc_ref.set(data)
            return f"Successfully added document '{doc_ref.id}' to collection '{collection_path}'."
        except Exception as e:
            return f"An unexpected error occurred while adding the document: {e}"

    def update_document(
        self,
        collection_id: str,
        document_id: str,
        data: dict[str, Any],
        tool_context: ToolContext,
        user_id: Optional[str] = None,
    ) -> str:
        """
        Updates an existing document in Firestore, merging the new data.

        Args:
            collection_id: The ID of the inventory category (e.g., 'dvd', 'figures').
            document_id: The ID of the document to update.
            data: A dictionary containing the fields to update.
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        try:
            user_id = user_id or tool_context.state.get("user_id") or "1"
            document_path = f"users/{user_id}/{collection_id}/{document_id}"
            self.db.document(document_path).set(data, merge=True)
            return f"Successfully updated document at '{document_path}'."
        except Exception as e:
            return f"An unexpected error occurred while updating the document: {e}"

    def delete_document(
        self,
        collection_id: str,
        document_id: str,
        tool_context: ToolContext,
        user_id: Optional[str] = None,
    ) -> str:
        """
        Deletes a document from Firestore.

        Args:
            collection_id: The ID of the inventory category (e.g., 'dvd', 'figures').
            document_id: The ID of the document to delete.
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        try:
            user_id = user_id or tool_context.state.get("user_id") or "1"
            document_path = f"users/{user_id}/{collection_id}/{document_id}"
            doc_ref = self.db.document(document_path)
            if not doc_ref.get().exists:
                return f"Error: Document '{document_id}' not found."
            doc_ref.delete()
            return f"Successfully deleted document at '{document_path}'."
        except Exception as e:
            return f"An unexpected error occurred while deleting the document: {e}"

    def find_document_by_field(
        self,
        collection_id: str,
        field: str,
        value: Any,
        tool_context: ToolContext,
        user_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Finds documents in a collection by matching a field with a specific value.
        Use this to find the ID of a document when you only know its title or another property.

        Args:
            collection_id: The ID of the inventory category to search in (e.g., 'dvd', 'figures').
            field: The document field to search on (e.g., 'title', 'name').
            value: The value to match.
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        user_id = user_id or tool_context.state.get("user_id") or "1"
        collection_path = f"users/{user_id}/{collection_id}"
        query = self.db.collection(collection_path).where(field, "==", value)
        results = query.stream()
        return [{"id": doc.id, "data": doc.to_dict()} for doc in results]

    def query_collection(
        self,
        collection_id: str,
        field: str,
        operator: str,
        value: Any,
        tool_context: ToolContext,
        user_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Performs a simple query on a Firestore collection.

        Args:
            collection_id: The ID of the inventory category to query (e.g., 'dvd', 'figures').
            field: The document field to filter on.
            operator: The comparison operator (e.g., '==', '<', '>=').
            value: The value to compare against.
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        user_id = user_id or tool_context.state.get("user_id") or "1"
        collection_path = f"users/{user_id}/{collection_id}"
        query = self.db.collection(collection_path).where(field, operator, value)
        results = query.stream()
        return [doc.to_dict() for doc in results]

    def list_inventory_categories(
        self, tool_context: ToolContext, user_id: Optional[str] = None
    ) -> list[str]:
        """
        Lists all inventory categories (subcollections) for a given user.

        Args:
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        user_id = user_id or tool_context.state.get("user_id") or "1"
        user_doc_ref = self.db.collection("users").document(user_id)
        collections = user_doc_ref.collections()
        return [c.id for c in collections]

    def get_all_user_inventory(
        self, tool_context: ToolContext, user_id: Optional[str] = None
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Fetches all inventory items across all categories for a given user.
        Use this tool when the user asks for a summary of their items.

        Args:
            user_id: The ID of the user. If not provided, it will be inferred from the session.
            tool_context: The context of the tool invocation.
        """
        user_id = user_id or tool_context.state.get("user_id") or "1"

        user_doc_ref = self.db.collection("users").document(user_id)
        collections = user_doc_ref.collections()

        inventory: dict[str, list[dict[str, Any]]] = {}
        for collection in collections:
            category_id = collection.id
            docs = collection.stream()
            inventory[category_id] = [doc.to_dict() for doc in docs]

        return inventory if inventory else {"message": "No inventory found for this user."}

    def get_tools(self) -> list[Callable]:
        """Returns a list of all tool methods."""
        return [
            self.get_document,
            self.add_document,
            self.update_document,
            self.delete_document,
            self.query_collection,
            self.list_inventory_categories,
            self.get_all_user_inventory,
            self.find_document_by_field,
        ]
