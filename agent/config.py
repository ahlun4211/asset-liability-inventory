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

import os

# We are using custom PROJECT_ID instead of GOOGLE_CLOUD_PROJECT because 
# this values defaults to the PROJECT NUMBER in Vertex Agent Engine and
# causes issues with finding the database.
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]

MODEL = "gemini-2.5-pro"

# Define your Firestore database name
FIRESTORE_DATABASE = "inventory"
