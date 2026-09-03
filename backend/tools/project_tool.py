class ProjectTool:
    """
    Controlled tool for project management operations.
    """

    name = "project_tool"
    description = "Provides controlled access to project information."

    def execute(self, action, user=None):

        # -------------------------------------------------
        # Employee-specific project data
        # -------------------------------------------------
        #
        # employee_test is currently our test employee.
        # These are the projects/tasks assigned to that user.
        #
        employee_projects = [
            {
                "name": "Vetri E-Commerce",
                "status": "Delayed",
                "progress": 75,
            }
        ]

        employee_tasks = [
            {
                "project": "Vetri E-Commerce",
                "task": "Payment Integration",
                "status": "Pending",
            }
        ]

        # -----------------------------------------
        # All Projects
        # -----------------------------------------
        if action == "get_projects":

            # Employee receives only their own projects.
            if user and not user.is_staff and not user.is_superuser:
                return {
                    "status": "success",
                    "data": {
                        "projects": employee_projects,
                        "total_projects": len(employee_projects),
                    },
                }

            # Manager/Admin can see broader project data.
            return {
                "status": "success",
                "data": {
                    "projects": [
                        {
                            "name": "Vetri E-Commerce",
                            "status": "Delayed",
                            "progress": 75,
                        },
                        {
                            "name": "AI Dashboard",
                            "status": "Delayed",
                            "progress": 80,
                        },
                        {
                            "name": "CRM System",
                            "status": "Active",
                            "progress": 60,
                        },
                        {
                            "name": "HR Management System",
                            "status": "Completed",
                            "progress": 100,
                        },
                    ],
                    "total_projects": 4,
                },
            }

        # -----------------------------------------
        # Delayed Projects
        # -----------------------------------------
        if action == "get_delayed_projects":

            return {
                "status": "success",
                "data": {
                    "delayed_projects": [
                        {
                            "name": "Vetri E-Commerce",
                            "delay_days": 3,
                        },
                        {
                            "name": "AI Dashboard",
                            "delay_days": 2,
                        },
                    ],
                    "total_delayed": 2,
                },
            }

        # -----------------------------------------
        # Project Status
        # -----------------------------------------
        if action == "get_project_status":

            return {
                "status": "success",
                "data": {
                    "active_projects": 8,
                    "completed_projects": 15,
                    "delayed_projects": 2,
                },
            }

        # -----------------------------------------
        # Project Deadlines
        # -----------------------------------------
        if action == "get_project_deadlines":

            return {
                "status": "success",
                "data": {
                    "deadlines": [
                        {
                            "project": "Vetri E-Commerce",
                            "deadline": "2026-09-05",
                        },
                        {
                            "project": "AI Dashboard",
                            "deadline": "2026-09-08",
                        },
                        {
                            "project": "CRM System",
                            "deadline": "2026-09-15",
                        },
                    ]
                },
            }

        # -----------------------------------------
        # Project Tasks
        # -----------------------------------------
        if action == "get_project_tasks":

            # Employee receives only their own tasks.
            if user and not user.is_staff and not user.is_superuser:
                return {
                    "status": "success",
                    "data": {
                        "tasks": employee_tasks,
                    },
                }

            # Manager/Admin can see broader task data.
            return {
                "status": "success",
                "data": {
                    "tasks": [
                        {
                            "project": "Vetri E-Commerce",
                            "task": "Payment Integration",
                            "status": "Pending",
                        },
                        {
                            "project": "AI Dashboard",
                            "task": "Dashboard UI",
                            "status": "In Progress",
                        },
                        {
                            "project": "CRM System",
                            "task": "Customer Module",
                            "status": "Completed",
                        },
                    ]
                },
            }

        # -----------------------------------------
        # Unsupported Action
        # -----------------------------------------
        return {
            "status": "error",
            "message": "Project action not supported.",
        }
