import { useEffect, useState } from "react";
import { getAgents } from "../services/api";

import {
  createApprovalPreview,
  approveAction,
  editApproval,
  cancelAction,
} from "../services/approvalService";

import "./AgentOrchestrator.css";

function AgentOrchestrator() {
  const [agents, setAgents] = useState([]);
  const [agentsLoading, setAgentsLoading] = useState(true);
  const [agentsError, setAgentsError] = useState("");

  const [agentName, setAgentName] = useState("Sales Agent");
  const [toolName, setToolName] = useState("email_tool");
  const [action, setAction] = useState("send_email");

  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  const [pendingAction, setPendingAction] = useState(null);

  const [loading, setLoading] = useState(false);
  const [messageText, setMessageText] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadAgents() {
      try {
        setAgentsLoading(true);
        setAgentsError("");

        const data = await getAgents();

        console.log("AVAILABLE AGENTS:", data);

        setAgents(data.agents || []);
      } catch (err) {
        console.error("AGENTS API ERROR:", err);
        setAgentsError(err.message);
      } finally {
        setAgentsLoading(false);
      }
    }

    loadAgents();
  }, []);

  async function handleRequestApproval(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessageText("");

      const result = await createApprovalPreview({
        agent_name: agentName,
        tool_name: toolName,
        action: action,
        parameters: {
          to,
          subject,
          message,
        },
      });

      if (result.status === "pending") {
        setPendingAction(result);

        setMessageText(
          `Approval requested successfully. Action ID: ${result.action_id}`
        );
      } else {
        setMessageText(
          result.message || "Action processed successfully."
        );
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleApprove() {
    if (!pendingAction) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessageText("");

      const result = await approveAction(
        pendingAction.action_id
      );

      setPendingAction(null);

      if (result.execution) {
        setMessageText(
          "Action approved and executed successfully."
        );
      } else {
        setMessageText(
          "Action approved successfully."
        );
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleEdit() {
    if (!pendingAction) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessageText("");

      const result = await editApproval(
        pendingAction.action_id,
        {
          to,
          subject,
          message,
        }
      );

      if (result.action) {
        setPendingAction(result.action);
      }

      setMessageText(
        "Approval action updated successfully."
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCancel() {
    if (!pendingAction) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessageText("");

      await cancelAction(
        pendingAction.action_id
      );

      setPendingAction(null);

      setMessageText(
        "Approval action cancelled."
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="agent-orchestrator-page">
      <div className="container-fluid agent-orchestrator-container">

        {/* PAGE HEADER */}
        <div className="ao-page-header">
          <div>
            <div className="ao-title-row">
              <div className="ao-title-icon">
                <i className="bi bi-diagram-3"></i>
              </div>

              <div>
                <h2 className="ao-page-title">
                  Agent Orchestrator
                </h2>

                <p className="ao-page-subtitle">
                  Central AI agent routing and approval management.
                </p>
              </div>
            </div>
          </div>

          <div className="ao-system-status">
            <span className="ao-status-dot"></span>
            Orchestrator Active
          </div>
        </div>

        {/* ERROR */}
        {error && (
          <div className="alert alert-danger ao-alert">
            <i className="bi bi-exclamation-triangle me-2"></i>
            <span>{error}</span>
          </div>
        )}

        {/* SUCCESS */}
        {messageText && (
          <div className="alert alert-success ao-alert">
            <i className="bi bi-check-circle me-2"></i>
            <span>{messageText}</span>
          </div>
        )}

        {/* AVAILABLE AGENTS */}
        <div className="card ao-card mb-4">

          <div className="card-header ao-card-header">
            <div className="ao-section-heading">
              <div className="ao-section-icon">
                <i className="bi bi-robot"></i>
              </div>

              <div>
                <h5 className="mb-0">
                  Available AI Agents
                </h5>

                <small>
                  Registered agents available for orchestration
                </small>
              </div>
            </div>

            {!agentsLoading && !agentsError && (
              <span className="badge text-bg-primary ao-agent-count">
                {agents.length} Agents
              </span>
            )}
          </div>

          <div className="card-body ao-card-body">

            {/* LOADING */}
            {agentsLoading && (
              <div className="ao-empty-state">

                <div
                  className="spinner-border text-primary mb-3"
                  role="status"
                >
                  <span className="visually-hidden">
                    Loading...
                  </span>
                </div>

                <p className="text-muted mb-0">
                  Loading available AI agents...
                </p>

              </div>
            )}

            {/* ERROR */}
            {agentsError && (
              <div className="alert alert-danger mb-0">
                <i className="bi bi-exclamation-triangle me-2"></i>
                {agentsError}
              </div>
            )}

            {/* AGENTS */}
            {!agentsLoading &&
              !agentsError &&
              agents.length > 0 && (
                <div className="row g-3">

                  {agents.map((agent) => (
                    <div
                      className="col-12 col-sm-6 col-xl-4"
                      key={agent.name}
                    >
                      <div className="ao-agent-card">

                        <div className="ao-agent-main">

                          <div className="ao-agent-icon">
                            <i className="bi bi-robot"></i>
                          </div>

                          <div className="ao-agent-content">
                            <h6 className="ao-agent-name">
                              {agent.name}
                            </h6>

                            <p className="ao-agent-description">
                              {agent.description}
                            </p>
                          </div>

                        </div>

                        <div className="ao-agent-footer">
                          <span className="badge text-bg-success">
                            <i className="bi bi-check-circle me-1"></i>
                            Available
                          </span>
                        </div>

                      </div>
                    </div>
                  ))}

                </div>
              )}

            {/* NO AGENTS */}
            {!agentsLoading &&
              !agentsError &&
              agents.length === 0 && (
                <div className="ao-empty-state">

                  <div className="ao-empty-icon">
                    <i className="bi bi-robot"></i>
                  </div>

                  <h6>
                    No AI agents available
                  </h6>

                  <p className="text-muted mb-0">
                    No AI agents are currently available.
                  </p>

                </div>
              )}

          </div>
        </div>

        {/* ORCHESTRATION FLOW */}
        <div className="card ao-card mb-4">

          <div className="card-header ao-card-header">

            <div className="ao-section-heading">
              <div className="ao-section-icon">
                <i className="bi bi-arrow-repeat"></i>
              </div>

              <div>
                <h5 className="mb-0">
                  Orchestration Flow
                </h5>

                <small>
                  How Vetri AI processes business requests
                </small>
              </div>
            </div>

          </div>

          <div className="card-body ao-card-body">

            <div className="row g-3">

              <div className="col-12 col-md-6 col-xl-3">
                <div className="ao-flow-step">

                  <div className="ao-flow-number">
                    01
                  </div>

                  <div className="ao-flow-icon">
                    <i className="bi bi-chat-dots"></i>
                  </div>

                  <h6>User Request</h6>

                  <small>
                    Request received from the user
                  </small>

                </div>
              </div>

              <div className="col-12 col-md-6 col-xl-3">
                <div className="ao-flow-step">

                  <div className="ao-flow-number">
                    02
                  </div>

                  <div className="ao-flow-icon">
                    <i className="bi bi-search"></i>
                  </div>

                  <h6>Intent Detection</h6>

                  <small>
                    Registry identifies the appropriate agent
                  </small>

                </div>
              </div>

              <div className="col-12 col-md-6 col-xl-3">
                <div className="ao-flow-step">

                  <div className="ao-flow-number">
                    03
                  </div>

                  <div className="ao-flow-icon">
                    <i className="bi bi-shield-check"></i>
                  </div>

                  <h6>Permission Check</h6>

                  <small>
                    Role permissions are verified
                  </small>

                </div>
              </div>

              <div className="col-12 col-md-6 col-xl-3">
                <div className="ao-flow-step">

                  <div className="ao-flow-number">
                    04
                  </div>

                  <div className="ao-flow-icon">
                    <i className="bi bi-cpu"></i>
                  </div>

                  <h6>Agent Processing</h6>

                  <small>
                    Selected agent processes the request
                  </small>

                </div>
              </div>

            </div>

          </div>
        </div>

        {/* REQUEST ACTION APPROVAL */}
        <div className="card ao-card mb-4">

          <div className="card-header ao-card-header">

            <div className="ao-section-heading">
              <div className="ao-section-icon">
                <i className="bi bi-shield-lock"></i>
              </div>

              <div>
                <h5 className="mb-0">
                  Request Action Approval
                </h5>

                <small>
                  Submit an action for approval before execution
                </small>
              </div>
            </div>

          </div>

          <div className="card-body ao-card-body">

            <form onSubmit={handleRequestApproval}>

              <div className="row g-3">

                {/* AGENT */}
                <div className="col-12 col-md-6 col-xl-4">

                  <label
                    htmlFor="agentName"
                    className="form-label ao-form-label"
                  >
                    Agent
                  </label>

                  <select
                    id="agentName"
                    name="agentName"
                    className="form-select ao-form-control"
                    value={agentName}
                    onChange={(event) =>
                      setAgentName(event.target.value)
                    }
                  >
                    <option>Sales Agent</option>
                    <option>HR Agent</option>
                    <option>Project Agent</option>
                    <option>Reporting Agent</option>
                    <option>Calendar Agent</option>
                  </select>

                </div>

                {/* TOOL */}
                <div className="col-12 col-md-6 col-xl-4">

                  <label
                    htmlFor="toolName"
                    className="form-label ao-form-label"
                  >
                    Tool
                  </label>

                  <select
                    id="toolName"
                    name="toolName"
                    className="form-select ao-form-control"
                    value={toolName}
                    onChange={(event) =>
                      setToolName(event.target.value)
                    }
                  >
                    <option>email_tool</option>
                    <option>calendar_tool</option>
                    <option>crm_tool</option>
                    <option>project_tool</option>
                    <option>reporting_tool</option>
                  </select>

                </div>

                {/* ACTION */}
                <div className="col-12 col-md-12 col-xl-4">

                  <label
                    htmlFor="action"
                    className="form-label ao-form-label"
                  >
                    Action
                  </label>

                  <select
                    id="action"
                    name="action"
                    className="form-select ao-form-control"
                    value={action}
                    onChange={(event) =>
                      setAction(event.target.value)
                    }
                  >
                    <option>send_email</option>
                    <option>send_bulk_message</option>
                    <option>approve_leave</option>
                    <option>financial_change</option>
                    <option>deploy</option>
                    <option>delete_data</option>
                  </select>

                </div>

              </div>

              {/* EMAIL PARAMETERS */}
              {action === "send_email" && (
                <div className="ao-email-section">

                  <div className="ao-email-heading">
                    <div className="ao-email-icon">
                      <i className="bi bi-envelope"></i>
                    </div>

                    <div>
                      <h6 className="mb-0">
                        Email Parameters
                      </h6>

                      <small>
                        Enter the details for the email action
                      </small>
                    </div>
                  </div>

                  <div className="row g-3">

                    <div className="col-12">

                      <label
                        htmlFor="recipient"
                        className="form-label ao-form-label"
                      >
                        Recipient
                      </label>

                      <input
                        id="recipient"
                        name="recipient"
                        type="email"
                        className="form-control ao-form-control"
                        placeholder="customer@example.com"
                        value={to}
                        onChange={(event) =>
                          setTo(event.target.value)
                        }
                        required
                      />

                    </div>

                    <div className="col-12">

                      <label
                        htmlFor="subject"
                        className="form-label ao-form-label"
                      >
                        Subject
                      </label>

                      <input
                        id="subject"
                        name="subject"
                        type="text"
                        className="form-control ao-form-control"
                        placeholder="Email subject"
                        value={subject}
                        onChange={(event) =>
                          setSubject(event.target.value)
                        }
                        required
                      />

                    </div>

                    <div className="col-12">

                      <label
                        htmlFor="message"
                        className="form-label ao-form-label"
                      >
                        Message
                      </label>

                      <textarea
                        id="message"
                        name="message"
                        className="form-control ao-form-control"
                        rows="5"
                        placeholder="Enter email message"
                        value={message}
                        onChange={(event) =>
                          setMessage(event.target.value)
                        }
                        required
                      ></textarea>

                    </div>

                  </div>

                </div>
              )}

              <div className="ao-form-actions">

                <button
                  type="submit"
                  className="btn btn-primary ao-primary-button"
                  disabled={loading}
                >

                  {loading ? (
                    <>
                      <span
                        className="spinner-border spinner-border-sm me-2"
                        role="status"
                      ></span>

                      Processing...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-shield-check me-1"></i>
                      Request Approval
                    </>
                  )}

                </button>

              </div>

            </form>

          </div>
        </div>

        {/* PENDING APPROVAL */}
        {pendingAction && (
          <div className="card ao-card ao-pending-card mb-4">

            <div className="card-header ao-pending-header">

              <div className="ao-section-heading">

                <div className="ao-section-icon ao-warning-icon">
                  <i className="bi bi-exclamation-circle"></i>
                </div>

                <div>
                  <h5 className="mb-0">
                    Pending Approval
                  </h5>

                  <small>
                    This action requires approval before execution
                  </small>
                </div>

              </div>

              <span className="badge text-bg-warning">
                {pendingAction.status}
              </span>

            </div>

            <div className="card-body ao-card-body">

              <div className="row g-3 mb-4">

                <div className="col-12 col-md-6">
                  <div className="ao-detail-box">

                    <span className="ao-detail-label">
                      Action ID
                    </span>

                    <strong className="ao-action-id">
                      {pendingAction.action_id}
                    </strong>

                  </div>
                </div>

                <div className="col-12 col-md-6">
                  <div className="ao-detail-box">

                    <span className="ao-detail-label">
                      Status
                    </span>

                    <span>
                      <span className="badge text-bg-warning">
                        {pendingAction.status}
                      </span>
                    </span>

                  </div>
                </div>

              </div>

              <div className="row g-3 mb-4">

                <div className="col-12 col-md-4">
                  <div className="ao-detail-box">

                    <span className="ao-detail-label">
                      Agent
                    </span>

                    <strong>
                      {pendingAction.agent}
                    </strong>

                  </div>
                </div>

                <div className="col-12 col-md-4">
                  <div className="ao-detail-box">

                    <span className="ao-detail-label">
                      Tool
                    </span>

                    <strong>
                      {pendingAction.tool}
                    </strong>

                  </div>
                </div>

                <div className="col-12 col-md-4">
                  <div className="ao-detail-box">

                    <span className="ao-detail-label">
                      Action
                    </span>

                    <strong>
                      {pendingAction.action}
                    </strong>

                  </div>
                </div>

              </div>

              <div className="ao-parameters-section">

                <div className="ao-parameters-heading">
                  <i className="bi bi-braces me-2"></i>
                  Parameters
                </div>

                <pre className="ao-parameters">
                  {JSON.stringify(
                    pendingAction.parameters,
                    null,
                    2
                  )}
                </pre>

              </div>

              <div className="ao-pending-actions">

                <button
                  type="button"
                  className="btn btn-success"
                  onClick={handleApprove}
                  disabled={loading}
                >
                  <i className="bi bi-check-lg me-1"></i>
                  Approve
                </button>

                <button
                  type="button"
                  className="btn btn-warning"
                  onClick={handleEdit}
                  disabled={loading}
                >
                  <i className="bi bi-pencil me-1"></i>
                  Save Edit
                </button>

                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={handleCancel}
                  disabled={loading}
                >
                  <i className="bi bi-x-lg me-1"></i>
                  Cancel
                </button>

              </div>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default AgentOrchestrator;