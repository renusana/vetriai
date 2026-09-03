import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import AIChat from "./pages/AIChat";
import UserRoles from "./pages/UserRoles";
import Permissions from "./pages/Permissions";
import AgentOrchestrator from "./pages/AgentOrchestrator";
import Notifications from "./pages/Notifications";
import Approvals from "./pages/Approvals";
import ProtectedRoute from "./components/ProtectedRoute";

import DashboardLayout from "./layouts/DashboardLayout";

function App() {
  return (
    <Routes>

      {/* Public */}
      <Route
        path="/"
        element={<Navigate to="/login" />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      {/* Application */}
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/ai-chat"
            element={<AIChat />}
          />

          <Route
            path="/user-roles"
            element={<UserRoles />}
          />

          <Route
            path="/permissions"
            element={<Permissions />}
          />

          <Route
            path="/agent-orchestrator"
            element={<AgentOrchestrator />}
          />

          <Route
            path="/approvals"
            element={<Approvals />}
          />

          <Route
            path="/notifications"
            element={<Notifications />}
          />

        </Route>
      </Route>



    </Routes>
  );
}

export default App;

