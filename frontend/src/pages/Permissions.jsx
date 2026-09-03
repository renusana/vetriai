import { useEffect, useState } from "react";
import { getPermissions } from "../services/api";

function Permissions() {
  const [roles, setRoles] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadPermissions();
  }, []);

  async function loadPermissions() {
    try {
      setLoading(true);
      setError("");

      const data = await getPermissions();

      console.log(
        "PERMISSIONS API RESPONSE:",
        JSON.stringify(data, null, 2)
      );

      setRoles(data.roles || {});
    } catch (err) {
      console.error("PERMISSIONS ERROR:", err);
      setError(err.message || "Failed to load permissions.");
    } finally {
      setLoading(false);
    }
  }

  function formatRole(role) {
    return role
      .charAt(0)
      .toUpperCase() + role.slice(1);
  }

  function formatPermission(permission) {
    return permission
      .split("_")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  }

  return (
    <div className="container-fluid mt-4">

      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">
            Permissions
          </h2>

          <p className="text-muted mb-0">
            Manage user permissions and access controls.
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={loadPermissions}
        >
          <i className="bi bi-arrow-clockwise me-2"></i>
          Refresh
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="alert alert-info">
          <i className="bi bi-hourglass-split me-2"></i>
          Loading permissions...
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="alert alert-danger">
          <i className="bi bi-exclamation-triangle me-2"></i>
          {error}
        </div>
      )}

      {/* Permission Cards */}
      {!loading && !error && Object.keys(roles).length > 0 && (
        <div className="row">

          {Object.entries(roles).map(
            ([role, permissions]) => (

              <div
                className="col-md-6 col-xl-4 mb-4"
                key={role}
              >

                <div className="card h-100 shadow-sm">

                  <div className="card-header bg-white d-flex justify-content-between align-items-center">

                    <h5 className="mb-0 fw-bold">
                      <i className="bi bi-person-badge me-2"></i>
                      {formatRole(role)}
                    </h5>

                    <span className="badge bg-primary">
                      {permissions.length}
                    </span>

                  </div>

                  <div className="card-body">

                    {permissions.length > 0 ? (
                      <ul className="list-group list-group-flush">

                        {permissions.map(
                          permission => (

                            <li
                              className="list-group-item px-0"
                              key={permission}
                            >

                              <i className="bi bi-check-circle-fill text-success me-2"></i>

                              {formatPermission(
                                permission
                              )}

                            </li>

                          )
                        )}

                      </ul>
                    ) : (
                      <p className="text-muted mb-0">
                        No permissions assigned.
                      </p>
                    )}

                  </div>

                </div>

              </div>

            )
          )}

        </div>
      )}

      {/* No permissions */}
      {!loading &&
        !error &&
        Object.keys(roles).length === 0 && (
          <div className="alert alert-warning">
            No permission data found.
          </div>
        )}

    </div>
  );
}

export default Permissions;