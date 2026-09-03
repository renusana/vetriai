import { useEffect, useState } from "react";
import { getUserRoles } from "../services/api";

function UserRoles() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        loadUsers();
    }, []);

    async function loadUsers() {
        try {
            setLoading(true);
            setError("");

            const data = await getUserRoles();

            console.log(
                "USER ROLES API RESPONSE:",
                JSON.stringify(data, null, 2)
            );

            setUsers(Array.isArray(data.users) ? data.users : []);
        } catch (err) {
            console.error("USER ROLES ERROR:", err);
            setError(err.message || "Failed to load users.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="container-fluid mt-4">

            {/* Page Header */}
            <div className="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2 className="fw-bold mb-1">
                        User Roles
                    </h2>

                    <p className="text-muted mb-0">
                        Manage users and their assigned roles.
                    </p>
                </div>

                <button
                    className="btn btn-primary"
                    onClick={loadUsers}
                >
                    <i className="bi bi-arrow-clockwise me-2"></i>
                    Refresh
                </button>
            </div>

            {/* Loading */}
            {loading && (
                <div className="alert alert-info">
                    <i className="bi bi-hourglass-split me-2"></i>
                    Loading users...
                </div>
            )}

            {/* Error */}
            {error && (
                <div className="alert alert-danger">
                    <i className="bi bi-exclamation-triangle me-2"></i>
                    {error}
                </div>
            )}

            {/* No users */}
            {!loading && !error && users.length === 0 && (
                <div className="alert alert-warning">
                    <i className="bi bi-people me-2"></i>
                    No users found.
                </div>
            )}

            {/* Users */}
            {!loading && !error && users.length > 0 && (
                <div className="card shadow-sm">

                    <div className="card-header bg-white">
                        <h5 className="mb-0">
                            <i className="bi bi-people-fill me-2"></i>
                            Registered Users
                            <span className="badge bg-secondary ms-2">
                                {users.length}
                            </span>
                        </h5>
                    </div>

                    <div className="table-responsive">

                        <table className="table table-hover align-middle mb-0">

                            <thead className="table-light">
                                <tr>
                                    <th>#</th>
                                    <th>User</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Permissions</th>
                                </tr>
                            </thead>

                            <tbody>

                                {users.map((user, index) => (

                                    <tr key={user.id || index}>

                                        {/* ID */}
                                        <td>
                                            {index + 1}
                                        </td>

                                        {/* Username */}
                                        <td>
                                            <div className="d-flex align-items-center">

                                                <div
                                                    className="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center me-2"
                                                    style={{
                                                        width: "40px",
                                                        height: "40px"
                                                    }}
                                                >
                                                    {user.username
                                                        ? user.username
                                                            .charAt(0)
                                                            .toUpperCase()
                                                        : "U"}
                                                </div>

                                                <strong>
                                                    {user.username || "Unknown"}
                                                </strong>

                                            </div>
                                        </td>

                                        {/* Name */}
                                        <td>
                                            {user.name || "-"}
                                        </td>

                                        {/* Email */}
                                        <td>
                                            {user.email || "-"}
                                        </td>

                                        {/* Role */}
                                        <td>
                                            <span className="badge bg-primary">
                                                {user.role
                                                    ? user.role
                                                        .charAt(0)
                                                        .toUpperCase() +
                                                    user.role.slice(1)
                                                    : "Employee"}
                                            </span>
                                        </td>

                                        {/* Permissions */}
                                        <td>
                                            <button
                                                className="btn btn-sm btn-outline-primary"
                                                disabled
                                                title="Permission management will be implemented next"
                                            >
                                                <i className="bi bi-shield-check me-1"></i>
                                                View Permissions
                                            </button>
                                        </td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    </div>

                </div>
            )}

        </div>
    );
}

export default UserRoles;