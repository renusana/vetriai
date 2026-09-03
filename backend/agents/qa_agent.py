from .base_agent import BaseAgent


class QAAgent(BaseAgent):

    name = "QA Agent"

    description = (
        "Handles testing, quality assurance, test results, bugs, and quality metrics"
    )

    def can_handle(self, request):

        qa_keywords = [
            "qa",
            "quality assurance",
            "testing",
            "test results",
            "test cases",
            "test case",
            "test execution",
            "quality",
            "regression testing",
            "regression",
            "bug testing",
            "defects",
            "defect",
            "test coverage",
        ]

        request_lower = request.lower()

        return any(keyword in request_lower for keyword in qa_keywords)

    def get_required_permission(self, request):
        return "view_qa"

    def process(self, request, user, credentials=None):

        request_lower = request.lower()

        if any(
            keyword in request_lower
            for keyword in [
                "qa",
                "quality assurance",
                "testing",
                "test results",
                "test cases",
                "test case",
                "test execution",
                "quality",
                "regression testing",
                "regression",
                "bug testing",
                "defects",
                "defect",
                "test coverage",
            ]
        ):

            data = {
                "total_test_cases": 120,
                "passed_tests": 108,
                "failed_tests": 12,
                "test_coverage": "90%",
            }

            message = (
                "QA Summary:\n"
                f"Total Test Cases: {data['total_test_cases']}\n"
                f"Passed Tests: {data['passed_tests']}\n"
                f"Failed Tests: {data['failed_tests']}\n"
                f"Test Coverage: {data['test_coverage']}"
            )

            return {
                "agent": self.name,
                "status": "success",
                "data": data,
                "message": message,
            }

        return {
            "agent": self.name,
            "status": "error",
            "data": {},
            "message": "The requested QA information is not currently supported.",
        }
