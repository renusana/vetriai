# Vetri AI Multi-Agent

## Known Issues

**Project:** Vetri AI Multi-Agent Business Operations Assistant

---

# 1. Introduction

This document records known limitations, configuration issues, and areas that may require additional work in the Vetri AI Multi-Agent application.

---

# 2. Google Calendar OAuth Configuration

Google Calendar integration requires correct OAuth configuration.

A redirect URI mismatch can occur when the callback URL configured in Google Cloud does not exactly match the application's callback URL.

**Callback endpoint:**

```text
/api/calendar/oauth2callback/
```

Administrators should ensure that the production callback URL is correctly registered in Google Cloud.

---

# 3. Google OAuth Testing Mode

When the Google OAuth application is configured for testing, only configured test users may be able to authorize the application.

If an unauthorized account attempts to connect, Google may return an access-denied error.

---

# 4. Email Tool Validation

Email actions require the necessary parameters, including a valid recipient.

If the recipient is missing, the email execution fails with an error similar to:

```json
{
    "status": "error",
    "message": "Recipient is required."
}
```

The approval workflow records the execution result so the failure can be investigated.

---

# 5. Audit Log API Authentication

The current Audit Log API view does not explicitly enforce `IsAuthenticated`.

**Endpoint:**

```http
GET /api/audit-logs/
```

This should be reviewed before production hardening because audit records may contain sensitive operational information.

---

# 6. Calendar Endpoint Authentication

The current Google Calendar login, OAuth callback, and Calendar Test views do not explicitly enforce DRF `IsAuthenticated`.

The endpoints are:

```http
GET /api/calendar/login/
GET /api/calendar/oauth2callback/
GET /api/calendar/test/
```

The OAuth flow depends on session-based Google Calendar credentials.

---

# 7. AI / LLM Dependency

Some advanced AI functionality may depend on external LLM configuration and API availability.

If the required API credentials, quota, or billing configuration are unavailable, LLM-generated responses may not work as expected.

The application should continue to use the available agent and business-tool functionality where supported.

---

# 8. External Integration Dependency

External integrations can fail independently of the Vetri AI application.

Possible causes include:

* API downtime
* Invalid credentials
* Expired OAuth credentials
* Network problems
* Incorrect configuration
* Service quota limits
* Permission restrictions

External integration failures should be checked through application logs and the relevant service configuration.

---

# 9. Automation Data Dependency

Automated reminders and intelligent alerts depend on the availability and quality of business information.

If there are no matching conditions or relevant business records, the automation endpoint may generate zero reminders or alerts.

Example:

```json
{
    "status": "success",
    "total_reminders": 0,
    "message": "0 new automated reminders generated."
}
```

A zero result does not necessarily indicate an application failure.

---

# 10. Multi-Agent Routing Limitations

The AI Orchestrator determines which specialized agent should process a request.

Ambiguous or incomplete user requests may result in less accurate routing.

Users should provide clear business requests when possible.

Example:

```text
Show my finance summary
```

is more specific than:

```text
Show my summary
```

---

# 11. Tool Execution Failures

An agent may successfully identify a tool or action while the actual tool execution fails.

Possible causes include:

* Missing parameters
* Invalid data
* External service failure
* Permission restrictions
* Authentication failure
* Configuration problems

Tool execution results should be reviewed when an operation fails.

---

# 12. Deployment Configuration

Production deployment depends on correct configuration of:

* Environment variables
* CORS
* Allowed hosts
* Database settings
* Gunicorn
* External service credentials
* OAuth configuration

A configuration error can cause the application to work locally but fail after deployment.

---

# 13. Database Dependency

The Django application depends on a correctly configured database.

Database connectivity or migration problems may affect:

* User data
* Conversations
* Notifications
* Approvals
* Audit records
* Business information

Database migrations should be run after database-related model changes.

---

# 14. Browser and Network Dependency

The React frontend requires network access to communicate with the Django backend.

API requests may fail when:

* The backend is unavailable
* The production API URL is incorrect
* CORS is incorrectly configured
* The user's network is unavailable
* An external service cannot be reached

---

# 15. Security Hardening

Some areas require additional security hardening before a production-scale deployment.

These include:

* Restricting audit-log access
* Reviewing OAuth endpoint protection
* Reviewing production CORS configuration
* Protecting all secrets
* Reviewing role and permission policies
* Performing unauthorized-access testing
* Performing integration-failure testing

---

# 16. Testing Limitations

The major application functionality has been tested, including:

* Authentication
* AI Chat
* Finance Agent
* Project Agent
* Reporting Agent
* Calendar integration
* Approval workflow
* Notifications
* Audit logging
* Automation

Additional comprehensive security testing, AI evaluation, and failure-condition testing may be required for future releases.

---

# 17. Known Issue Tracking

Known issues should be reviewed and updated whenever:

* A new limitation is discovered
* An integration changes
* A deployment issue is identified
* A security concern is discovered
* A previously known issue is resolved

Resolved issues should be removed from this document or moved to a project change log when appropriate.

---

# 18. Summary

The Vetri AI Multi-Agent application is functional across its major business workflows, but several areas depend on external services, production configuration, and additional security hardening.

The most important areas to monitor are:

* Google Calendar OAuth
* Email parameter validation
* Audit-log access control
* External API availability
* LLM configuration
* Automation data
* Deployment configuration
* Database availability
* Security testing

These limitations should be considered during deployment, testing, and future development.
