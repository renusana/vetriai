# Vetri AI Multi-Agent

## User Guide

**Project:** Vetri AI Multi-Agent Business Operations Assistant
**Frontend:** React
**Backend:** Django REST Framework
**Authentication:** JWT

---

# 1. Introduction

Vetri AI Multi-Agent is an AI-powered business operations assistant designed to help users access business information and perform supported business operations through specialized AI agents.

The system provides a single AI Chat interface through which users can interact with different business agents.

The platform includes functionality for:

* Business information
* Finance
* Sales
* Projects
* Reporting
* HR
* Calendar
* Marketing
* Developer operations
* QA
* Operations
* GitHub
* Notifications
* Approvals
* Automation
* Intelligent alerts

---

# 2. Getting Started

To use Vetri AI Multi-Agent:

1. Open the deployed application.
2. Log in with your username and password.
3. After successful authentication, the Dashboard is displayed.
4. Use the navigation menu to access available features.
5. Use AI Chat to communicate with the business agents.

---

# 3. Login

The Login page is used to authenticate users.

Enter:

* Username
* Password

Then select **Login**.

After successful authentication, the application receives a JWT access token and refresh token.

The access token is used to access protected application APIs.

---

# 4. Dashboard

The Dashboard provides an overview of business operations.

Depending on the available business data, the Dashboard can display:

* Revenue
* Sales leads
* Customers
* Follow-ups
* Orders
* Pending orders
* Employees
* Employees on leave
* Attendance
* Leave information
* Projects
* Project status
* Delayed projects
* Deadlines
* Tasks

The Dashboard provides a quick overview before performing detailed operations through AI Chat.

---

# 5. AI Chat

AI Chat is the main interface for interacting with Vetri AI.

Users can enter natural-language business questions or requests.

Example:

```text
Show my finance summary
```

The request is sent to the Django backend and processed by the AI Orchestrator.

The Orchestrator identifies the appropriate specialized agent and returns the result.

---

# 6. Example AI Chat Requests

Users can ask questions such as:

### Finance

```text
Show my finance summary
```

### Sales

```text
Show my sales leads
```

### Projects

```text
Show my project status
```

### Reporting

```text
Show the latest business report
```

### Calendar

```text
Show my calendar events
```

### Multiple Business Areas

```text
Show my sales leads and finance summary
```

The system can route different parts of a request to the appropriate business functionality.

---

# 7. AI Agents

Vetri AI uses specialized agents for different business functions.

Current registered agents include:

* Calendar Agent
* HR Agent
* Sales Agent
* Project Agent
* Finance Agent
* Marketing Agent
* Developer Agent
* QA Agent
* Operations Agent
* Reporting Agent
* GitHub Agent

Each agent is responsible for handling requests related to its business domain.

---

# 8. Conversation History

The application provides conversation management for authenticated users.

Users can:

* Create conversations
* Continue existing conversations
* View previous messages
* Maintain separate conversation histories

Conversation records are associated with the authenticated user.

A user can access only their own conversation records.

---

# 9. User Roles

The User Roles functionality provides information about application users and their assigned roles.

Roles are used as part of the application's access-control system.

User permissions determine which operations can be performed.

---

# 10. Permissions

The Permissions section provides permission information from the application's Permission Engine.

The Permission Engine helps control access to business operations.

Before performing restricted operations, the system can verify whether the user has the required permission.

---

# 11. Google Calendar

Vetri AI supports Google Calendar integration using OAuth.

## Connecting Google Calendar

The Calendar integration process is:

```text
Open Calendar Login
       ↓
Google Authentication
       ↓
Grant Calendar Permission
       ↓
OAuth Callback
       ↓
Calendar Credentials Stored
       ↓
Calendar API Available
```

After successful authentication, the application can use the Google Calendar integration for supported calendar operations.

---

# 12. Notifications

The Notifications section displays important events and system messages.

Notifications can be generated for:

* Approval requests
* Approved actions
* Executed actions
* Project risks
* High-priority leads
* Overdue payments
* Customer issues
* Deadlines
* Intelligent business alerts

Notifications are associated with the authenticated user.

---

# 13. Approval Workflow

Some operations are considered sensitive and require user approval before execution.

Examples include:

* Sending emails
* Sending bulk messages
* Approving leave
* Financial changes
* Deployment
* Data deletion

The workflow is:

```text
User Request
     ↓
AI Agent
     ↓
Sensitive Action
     ↓
Approval Required
     ↓
Notification
     ↓
User Reviews Request
     ↓
Approve / Edit / Cancel
     ↓
Tool Execution
     ↓
Execution Notification
```

---

# 14. Reviewing an Approval

When an approval request is generated:

1. Open the Notifications or approval-related section.
2. Identify the pending approval.
3. Review the requested action.
4. Check the parameters.
5. Choose the appropriate action.

Available approval operations include:

* Approve
* Edit
* Cancel

---

# 15. Approval Example

A sensitive email operation may generate an approval request containing:

```json
{
    "agent_name": "Sales Agent",
    "tool_name": "email_tool",
    "action": "send_email",
    "parameters": {
        "subject": "Test Email",
        "message": "Hello",
        "recipient": "example@example.com"
    }
}
```

The action is not executed until the required approval is completed.

---

# 16. Audit Logging

Important system operations are recorded through audit logging.

Audit records can contain:

* User
* Agent
* Request
* Data accessed
* Tool
* Action
* Approval status
* Result
* Timestamp

Audit logs provide traceability for important actions and approval workflows.

---

# 17. Automation

Vetri AI provides automation functionality for generating reminders and intelligent alerts.

## Reminders

Automated reminders can be generated from available business information.

Example types of reminders include:

* Upcoming deadlines
* Follow-ups
* Pending business tasks
* Other time-sensitive activities

## Intelligent Alerts

Intelligent alerts identify important business conditions such as:

* Project risks
* Approaching deadlines
* Important sales leads
* Overdue payments
* Customer issues
* Other business risks

---

# 18. How to Use AI Chat Effectively

For better results, users should provide clear requests.

### Good request

```text
Show my current project status
```

### More specific request

```text
Show delayed projects and upcoming deadlines
```

### Multiple-agent request

```text
Show my sales leads and finance summary
```

Clear requests help the AI Orchestrator route the request to the appropriate agent or agents.

---

# 19. Sensitive Actions

Users should carefully review sensitive actions before approving them.

Before approval, verify:

* Agent name
* Tool name
* Action
* Parameters
* Recipient information where applicable
* Expected result

Do not approve an action if the parameters are incorrect.

---

# 20. Error Messages

The application may display errors when:

* Required information is missing
* Authentication fails
* A requested resource does not exist
* A user does not have permission
* An external integration is unavailable
* A tool cannot execute an action

Example:

```json
{
    "status": "error",
    "message": "Recipient is required."
}
```

Users should correct the missing information and retry the operation where appropriate.

---

# 21. Logout

Users should log out when they have finished using the application, especially when accessing the application from a shared computer.

---

# 22. User Security Guidelines

Users should:

* Keep passwords private.
* Never share JWT tokens.
* Review sensitive approval requests carefully.
* Verify recipients before approving communication actions.
* Avoid approving unknown or unexpected operations.
* Log out from shared devices.
* Report unexpected system behavior to the administrator.

---

# 23. Typical User Workflow

A normal business workflow is:

```text
Login
  ↓
Dashboard
  ↓
AI Chat
  ↓
Ask Business Question
  ↓
AI Orchestrator
  ↓
Specialized Agent
  ↓
Business Data / Tool
  ↓
Response
```

For sensitive operations:

```text
Login
  ↓
AI Chat
  ↓
Sensitive Request
  ↓
Approval Request
  ↓
Notification
  ↓
User Approval
  ↓
Tool Execution
  ↓
Notification
  ↓
Audit Log
```

---

# 24. Best Practices

For effective use of Vetri AI:

1. Use clear natural-language requests.
2. Specify the business area when necessary.
3. Review AI responses before taking important decisions.
4. Carefully review approval requests.
5. Verify sensitive action parameters.
6. Monitor notifications regularly.
7. Use conversation history to continue related tasks.
8. Contact an administrator when an unexpected error occurs.

---

# 25. Summary

Vetri AI Multi-Agent provides a centralized interface for interacting with multiple business functions.

Users can:

* Log in securely
* View business information
* Ask questions through AI Chat
* Access specialized agents
* Manage conversations
* Review notifications
* Approve sensitive actions
* Use Google Calendar integration
* Receive automated reminders
* Receive intelligent business alerts

The system combines AI agents, business tools, permissions, approvals, notifications, and audit logging to support business operations through a single platform.
