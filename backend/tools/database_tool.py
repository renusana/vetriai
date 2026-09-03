class DatabaseTool:
    """
    Controlled tool for accessing business database information.
    """

    name = "database_tool"
    description = "Provides controlled access to business database information."

    def execute(self, action, user=None):
        """
        Execute an approved database action.
        """

        # -----------------------------------------
        # Own User Profile
        # -----------------------------------------
        if action == "get_own_profile":

            if user is None:
                return {
                    "status": "error",
                    "message": "User information is required.",
                }

            # Determine application role
            if user.is_superuser:
                role = "admin"
            elif user.is_staff:
                role = "manager"
            else:
                role = "employee"

            profile = {
                "username": user.username,
                "email": user.email,
                "role": role,
                "status": "Active" if user.is_active else "Inactive",
            }

            return {
                "status": "success",
                "data": {
                    "profile": profile,
                },
            }

        # -----------------------------------------
        # Business Summary
        # -----------------------------------------
        if action == "get_business_summary":

            return {
                "status": "success",
                "data": {
                    "total_customers": 125,
                    "total_orders": 48,
                    "pending_orders": 7,
                },
            }

        # -----------------------------------------
        # Employees
        # -----------------------------------------
        if action == "get_employees":

            return {
                "status": "success",
                "data": {
                    "employees": [
                        {
                            "name": "Arun",
                            "department": "Development",
                            "role": "Python Developer",
                            "status": "Active",
                        },
                        {
                            "name": "Priya",
                            "department": "HR",
                            "role": "HR Executive",
                            "status": "On Leave",
                        },
                        {
                            "name": "Karthik",
                            "department": "Sales",
                            "role": "Sales Executive",
                            "status": "Active",
                        },
                        {
                            "name": "Divya",
                            "department": "Development",
                            "role": "React Developer",
                            "status": "On Leave",
                        },
                        {
                            "name": "Suresh",
                            "department": "Management",
                            "role": "Project Manager",
                            "status": "Active",
                        },
                    ],
                    "total_employees": 5,
                },
            }

        # -----------------------------------------
        # Employees Currently on Leave
        # -----------------------------------------
        if action == "get_employees_on_leave":

            return {
                "status": "success",
                "data": {
                    "employees_on_leave": [
                        {
                            "name": "Priya",
                            "department": "HR",
                            "leave_type": "Casual Leave",
                            "date": "2026-09-02",
                        },
                        {
                            "name": "Divya",
                            "department": "Development",
                            "leave_type": "Sick Leave",
                            "date": "2026-09-02",
                        },
                    ],
                    "total_on_leave": 2,
                },
            }

        # -----------------------------------------
        # Attendance
        # -----------------------------------------
        if action == "get_attendance":

            return {
                "status": "success",
                "data": {
                    "date": "2026-09-01",
                    "total_employees": 5,
                    "present": 3,
                    "absent": 0,
                    "on_leave": 2,
                },
            }

        # -----------------------------------------
        # Leave Information
        # -----------------------------------------
        if action == "get_leave_information":

            return {
                "status": "success",
                "data": {
                    "total_on_leave": 2,
                    "employees": [
                        {
                            "name": "Priya",
                            "leave_type": "Casual Leave",
                            "date": "2026-09-02",
                        },
                        {
                            "name": "Divya",
                            "leave_type": "Sick Leave",
                            "date": "2026-09-02",
                        },
                    ],
                },
            }

        # -----------------------------------------
        # Employee Salary
        # -----------------------------------------
        if action == "get_employee_salary":

            return {
                "status": "success",
                "data": {
                    "salary_information": [
                        {
                            "name": "Arun",
                            "monthly_salary": 45000,
                        },
                        {
                            "name": "Priya",
                            "monthly_salary": 40000,
                        },
                        {
                            "name": "Karthik",
                            "monthly_salary": 42000,
                        },
                        {
                            "name": "Divya",
                            "monthly_salary": 45000,
                        },
                        {
                            "name": "Suresh",
                            "monthly_salary": 65000,
                        },
                    ]
                },
            }

        # -----------------------------------------
        # Unsupported Action
        # -----------------------------------------
        return {
            "status": "error",
            "message": "Database action not supported.",
        }
