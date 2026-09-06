import { useEffect, useState } from 'react';
import StatCard from '../components/StatCard';
import DashboardCard from '../components/DashboardCard';
import ActivityList from '../components/ActivityList';
import { getDashboard } from '../services/api';

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError('');

      const data = await getDashboard();

      setDashboard(data.dashboard);
    } catch (err) {
      console.error('Dashboard error:', err);
      setError(err.message || 'Failed to load dashboard.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="container-fluid px-4 py-4">
        <div className="text-center py-5">
          <div
            className="spinner-border text-primary"
            role="status"
          >
            <span className="visually-hidden">
              Loading...
            </span>
          </div>

          <p className="text-muted mt-3">
            Loading dashboard...
          </p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="container-fluid px-4 py-4">
        <div className="alert alert-danger" role="alert">
          <i className="bi bi-exclamation-triangle me-2"></i>
          {error}
        </div>

        <button
          className="btn btn-primary"
          onClick={loadDashboard}
        >
          <i className="bi bi-arrow-clockwise me-2"></i>
          Try Again
        </button>
      </main>
    );
  }

  if (!dashboard) {
    return null;
  }

  const finance = dashboard.finance || {};
  const sales = dashboard.sales || {};
  const customers = dashboard.customers || {};
  const followups = dashboard.followups || {};
  const projects = dashboard.projects || {};
  const projectStatus = dashboard.project_status || {};
  const delayedProjects = dashboard.delayed_projects || {};
  const deadlines = dashboard.deadlines || {};
  const tasks = dashboard.tasks || {};
  const employees = dashboard.employees || {};
  const employeesOnLeave = dashboard.employees_on_leave || {};
  const attendance = dashboard.attendance || {};
  const leave = dashboard.leave || {};
  const orders = dashboard.orders || {};
  const pendingOrders = dashboard.pending_orders || {};

  const totalEmployees = employees.total_employees || 0;
  const totalOnLeave = employeesOnLeave.total_on_leave || 0;
  const activeEmployees = totalEmployees - totalOnLeave;

  const taskList = tasks.tasks || [];

  const pendingTaskList = taskList.filter(
    (task) => task.status !== 'Completed'
  );

  const pendingTaskCount = pendingTaskList.length;

  /*
   * Create activity information from actual backend data.
   * The backend currently doesn't provide timestamps, so we
   * don't create fake "10 min ago" / "1 hour ago" values.
   */
  const activities = [];

  const leadCount = sales.new_leads || 0;

  if (leadCount > 0) {
    activities.push({
      id: 'leads',
      title: 'New leads',
      description: `${leadCount} new leads are currently available.`,
      time: 'Current data',
    });
  }

  if ((delayedProjects.total_delayed || 0) > 0) {
    const delayedProject =
      delayedProjects.delayed_projects?.[0];

    activities.push({
      id: 'delayed-project',
      title: 'Delayed project',
      description: delayedProject
        ? `${delayedProject.name} is delayed by ${delayedProject.delay_days} days.`
        : `${delayedProjects.total_delayed} projects are delayed.`,
      time: 'Current data',
    });
  }

  if (pendingTaskCount > 0) {
    const pendingTask = pendingTaskList[0];

    activities.push({
      id: 'pending-task',
      title: 'Pending task',
      description: pendingTask
        ? `${pendingTask.task} is ${pendingTask.status}.`
        : `${pendingTaskCount} tasks require attention.`,
      time: 'Current data',
    });
  }

  if ((pendingOrders.pending_orders || 0) > 0) {
    activities.push({
      id: 'pending-orders',
      title: 'Pending orders',
      description: `${pendingOrders.pending_orders} orders are awaiting action.`,
      time: 'Current data',
    });
  }

  /*
   * Build risks from actual backend information.
   */
  const risks = [];

  if ((delayedProjects.total_delayed || 0) > 0) {
    risks.push({
      name: `${delayedProjects.total_delayed} delayed project(s)`,
      level: 'High',
    });
  }

  if ((followups.pending_followups || []).length > 0) {
    risks.push({
      name: `${followups.pending_followups.length} pending customer follow-up(s)`,
      level: 'Medium',
    });
  }

  if ((pendingOrders.pending_orders || 0) > 0) {
    risks.push({
      name: `${pendingOrders.pending_orders} pending order(s)`,
      level: 'Medium',
    });
  }

  /*
   * Format Indian currency.
   */
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(value || 0);
  };

  /*
   * Format project deadline dates.
   */
  const formatDate = (dateString) => {
    if (!dateString) {
      return '-';
    }

    const date = new Date(`${dateString}T00:00:00`);

    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
    });
  };

  return (
    <main className="container-fluid px-4 py-4">

      {/* Header */}
      <div className="mb-4">
        <h2 className="fw-bold">
          Welcome, Renuka
        </h2>

        <p className="text-muted mb-0">
          Here's an overview of your business operations.
        </p>
      </div>

      {/* Main Statistics */}
      <div className="row">

        <StatCard
          title="Revenue"
          value={formatCurrency(finance.total_revenue)}
          icon="bi-currency-rupee"
          description={`Expenses: ${formatCurrency(finance.total_expenses)}`}
        />

        <StatCard
          title="Leads"
          value={sales.total_leads || 0}
          icon="bi-person-plus"
          description={`${sales.new_leads || 0} new leads`}
        />

        <StatCard
          title="Projects"
          value={projects.total_projects || 0}
          icon="bi-kanban"
          description={`${projectStatus.active_projects || 0} active projects`}
        />

        <StatCard
          title="Customers"
          value={customers.total_customers || 0}
          icon="bi-people"
          description="Active customers"
        />

      </div>

      {/* Employee / Operations Statistics */}
      <div className="row">

        <StatCard
          title="Employees"
          value={totalEmployees}
          icon="bi-person-badge"
          description={`${activeEmployees} currently active`}
        />

        <StatCard
          title="Leave"
          value={totalOnLeave}
          icon="bi-calendar-check"
          description="Employees on leave"
        />

        <StatCard
          title="Workload"
          value="—"
          icon="bi-bar-chart"
          description="Workload data not available"
        />

        <StatCard
          title="Pending Tasks"
          value={pendingTaskCount}
          icon="bi-list-task"
          description="Tasks awaiting action"
        />

      </div>

      {/* Recent Business Activity */}
      <div className="row g-4 mb-4">

        <div className="col-12 col-lg-8">
          <DashboardCard title="Business Activity">

            {activities.length > 0 ? (
              <ActivityList
                activities={activities}
              />
            ) : (
              <p className="text-muted mb-0">
                No current business activity available.
              </p>
            )}

          </DashboardCard>
        </div>

        {/* Pending Tasks */}
        <div className="col-12 col-lg-4">
          <DashboardCard title="Pending Tasks">

            {pendingTaskList.length > 0 ? (
              <ul className="list-group list-group-flush">

                {pendingTaskList.map(
                  (task, index) => (
                    <li
                      key={index}
                      className="list-group-item px-0"
                    >
                      <i className="bi bi-check2-square text-primary me-2"></i>

                      <strong>
                        {task.task}
                      </strong>

                      <div className="small text-muted ms-4">
                        {task.project} · {task.status}
                      </div>
                    </li>
                  )
                )}

              </ul>
            ) : (
              <p className="text-muted mb-0">
                No pending tasks.
              </p>
            )}

          </DashboardCard>
        </div>

      </div>

      {/* Risks + Deadlines */}
      <div className="row g-4">

        {/* Risks */}
        <div className="col-12 col-lg-6">
          <DashboardCard title="Risks">

            {risks.length > 0 ? (
              <div className="list-group list-group-flush">

                {risks.map(
                  (risk, index) => (
                    <div
                      key={index}
                      className="list-group-item px-0 d-flex justify-content-between"
                    >
                      <span>
                        {risk.name}
                      </span>

                      <span
                        className={`badge ${risk.level === 'High'
                            ? 'bg-danger'
                            : risk.level === 'Medium'
                              ? 'bg-warning text-dark'
                              : 'bg-success'
                          }`}
                      >
                        {risk.level}
                      </span>
                    </div>
                  )
                )}

              </div>
            ) : (
              <p className="text-muted mb-0">
                No current risks identified.
              </p>
            )}

          </DashboardCard>
        </div>

        {/* Upcoming Deadlines */}
        <div className="col-12 col-lg-6">
          <DashboardCard title="Project Deadlines">

            {deadlines.deadlines?.length > 0 ? (
              <div className="list-group list-group-flush">

                {deadlines.deadlines.map(
                  (deadline, index) => (
                    <div
                      key={index}
                      className="list-group-item px-0 d-flex justify-content-between"
                    >
                      <span>
                        {deadline.project}
                      </span>

                      <strong>
                        {formatDate(
                          deadline.deadline
                        )}
                      </strong>
                    </div>
                  )
                )}

              </div>
            ) : (
              <p className="text-muted mb-0">
                No project deadlines available.
              </p>
            )}

          </DashboardCard>
        </div>

      </div>

    </main>
  );
}

export default Dashboard;