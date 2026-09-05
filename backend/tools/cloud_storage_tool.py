class CloudStorageTool:
    """
    Controlled tool for cloud storage operations.
    """

    name = "cloud_storage_tool"
    description = "Provides controlled access to cloud storage information."

    def execute(self, action, user=None, credentials=None):

        # -----------------------------------------
        # Storage Summary
        # -----------------------------------------
        if action == "get_storage_summary":

            return {
                "status": "success",
                "data": {
                    "total_files": 128,
                    "total_folders": 24,
                    "storage_used": "6.8 GB",
                    "storage_limit": "15 GB",
                },
            }

        # -----------------------------------------
        # Files
        # -----------------------------------------
        if action == "get_files":

            return {
                "status": "success",
                "data": {
                    "files": [
                        {
                            "name": "Project_Report.pdf",
                            "type": "PDF",
                            "size": "2.4 MB",
                        },
                        {
                            "name": "Sales_Data.xlsx",
                            "type": "Excel",
                            "size": "1.8 MB",
                        },
                        {
                            "name": "Employee_Data.xlsx",
                            "type": "Excel",
                            "size": "1.2 MB",
                        },
                    ],
                    "total_files": 128,
                },
            }

        # -----------------------------------------
        # Folders
        # -----------------------------------------
        if action == "get_folders":

            return {
                "status": "success",
                "data": {
                    "folders": [
                        {
                            "name": "Projects",
                            "files": 35,
                        },
                        {
                            "name": "Sales",
                            "files": 28,
                        },
                        {
                            "name": "HR",
                            "files": 22,
                        },
                        {
                            "name": "Reports",
                            "files": 18,
                        },
                    ],
                    "total_folders": 24,
                },
            }

        # -----------------------------------------
        # Recent Files
        # -----------------------------------------
        if action == "get_recent_files":

            return {
                "status": "success",
                "data": {
                    "recent_files": [
                        {
                            "name": "Project_Report.pdf",
                            "updated": "2026-09-05",
                        },
                        {
                            "name": "Sales_Data.xlsx",
                            "updated": "2026-09-04",
                        },
                        {
                            "name": "Employee_Data.xlsx",
                            "updated": "2026-09-03",
                        },
                    ]
                },
            }

        # -----------------------------------------
        # Unsupported Action
        # -----------------------------------------
        return {
            "status": "error",
            "message": "Cloud storage action not supported.",
        }
