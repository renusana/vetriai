from .base_agent import BaseAgent
from tools.cloud_storage_tool import CloudStorageTool


class CloudStorageAgent(BaseAgent):

    name = "Cloud Storage Agent"

    description = (
        "Handles cloud storage, files, folders, storage usage, "
        "and cloud document questions"
    )

    def __init__(self):
        self.cloud_storage_tool = CloudStorageTool()

    def can_handle(self, request):

        cloud_storage_keywords = [
            "cloud storage",
            "cloud storage summary",
            "storage",
            "storage summary",
            "files",
            "file",
            "folders",
            "folder",
            "documents",
            "document",
            "cloud files",
            "cloud documents",
            "recent files",
            "storage usage",
            "storage used",
        ]

        request_lower = request.lower()

        return any(
            keyword in request_lower
            for keyword in cloud_storage_keywords
        )

    def get_required_permission(self, request):
        return "view_cloud_storage"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        # -----------------------------------------
        # Storage Summary
        # -----------------------------------------
        if (
            "storage summary" in request_lower
            or "storage usage" in request_lower
            or "storage used" in request_lower
            or "cloud storage" in request_lower
        ):

            result = self.cloud_storage_tool.execute(
                "get_storage_summary",
                user,
                credentials=credentials,
            )

            if result.get("status") == "success":

                data = result.get("data", {})

                message = (
                    "Cloud Storage Summary:\n"
                    f"Total Files: {data.get('total_files', 0)}\n"
                    f"Total Folders: {data.get('total_folders', 0)}\n"
                    f"Storage Used: {data.get('storage_used', '0 GB')}\n"
                    f"Storage Limit: {data.get('storage_limit', '0 GB')}"
                )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Recent Files
        # -----------------------------------------
        if "recent" in request_lower and "file" in request_lower:

            result = self.cloud_storage_tool.execute(
                "get_recent_files",
                user,
                credentials=credentials,
            )

            if result.get("status") == "success":

                data = result.get("data", {})
                files = data.get("recent_files", [])

                if files:
                    file_lines = [
                        f"{item['name']} - {item['updated']}"
                        for item in files
                    ]

                    message = (
                        "Recent Cloud Files:\n"
                        + "\n".join(file_lines)
                    )
                else:
                    message = "There are no recent cloud files."

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Folders
        # -----------------------------------------
        if "folder" in request_lower:

            result = self.cloud_storage_tool.execute(
                "get_folders",
                user,
                credentials=credentials,
            )

            if result.get("status") == "success":

                data = result.get("data", {})
                folders = data.get("folders", [])

                folder_names = [
                    folder["name"]
                    for folder in folders
                ]

                message = (
                    f"There are {len(folder_names)} "
                    "main cloud storage folders: "
                    + ", ".join(folder_names)
                    + "."
                )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Files
        # -----------------------------------------
        if "file" in request_lower or "document" in request_lower:

            result = self.cloud_storage_tool.execute(
                "get_files",
                user,
                credentials=credentials,
            )

            if result.get("status") == "success":

                data = result.get("data", {})
                files = data.get("files", [])

                file_names = [
                    file["name"]
                    for file in files
                ]

                message = (
                    f"There are {data.get('total_files', 0)} "
                    "files in cloud storage. "
                    "Recent examples: "
                    + ", ".join(file_names)
                    + "."
                )

                return {
                    "agent": self.name,
                    "status": "success",
                    "data": data,
                    "message": message,
                }

        # -----------------------------------------
        # Unsupported Request
        # -----------------------------------------
        return {
            "agent": self.name,
            "status": "error",
            "data": {},
            "message": (
                "The requested cloud storage information "
                "is not currently supported."
            ),
        }

