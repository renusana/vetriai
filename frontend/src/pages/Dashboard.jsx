import StatCard from '../components/StatCard';
import DashboardCard from '../components/DashboardCard';
import ActivityList from '../components/ActivityList';

function Dashboard() {

  const activities = [
    {
      id: 1,
      title: 'New lead added',
      description: 'ABC Technologies was added as a new lead.',
      time: '10 min ago',
    },
    {
      id: 2,
      title: 'Project updated',
      description: 'Website Revamp project status changed.',
      time: '1 hour ago',
    },
    {
      id: 3,
      title: 'Task completed',
      description: 'Database integration task was completed.',
      time: '2 hours ago',
    },
    {
      id: 4,
      title: 'New customer',
      description: 'XYZ Solutions became a new customer.',
      time: 'Yesterday',
    },
  ];

  const pendingTasks = [
    'Review new customer requirements',
    'Complete dashboard UI',
    'Verify employee workload',
    'Prepare project report',
  ];

  const risks = [
    {
      name: 'Project deadline delay',
      level: 'High',
    },
    {
      name: 'Pending customer approval',
      level: 'Medium',
    },
    {
      name: 'Resource availability',
      level: 'Low',
    },
  ];

  return (
    <>

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
            value="₹8.45L"
            icon="bi-currency-rupee"
            description="This month"
          />

          <StatCard
            title="Leads"
            value="128"
            icon="bi-person-plus"
            description="24 new this week"
          />

          <StatCard
            title="Projects"
            value="18"
            icon="bi-kanban"
            description="6 active projects"
          />

          <StatCard
            title="Customers"
            value="86"
            icon="bi-people"
            description="8 new this month"
          />

        </div>


        {/* Secondary Statistics */}

        <div className="row">

          <StatCard
            title="Employees"
            value="42"
            icon="bi-person-badge"
            description="38 currently active"
          />

          <StatCard
            title="Leave"
            value="5"
            icon="bi-calendar-check"
            description="Employees on leave"
          />

          <StatCard
            title="Workload"
            value="78%"
            icon="bi-bar-chart"
            description="Average team workload"
          />

          <StatCard
            title="Pending Tasks"
            value="23"
            icon="bi-list-task"
            description="Tasks awaiting action"
          />

        </div>


        {/* Dashboard Sections */}

        <div className="row g-4 mb-4">

          {/* Recent Activity */}

          <div className="col-12 col-lg-8">

            <DashboardCard title="Recent Activity">

              <ActivityList
                activities={activities}
              />

            </DashboardCard>

          </div>


          {/* Pending Tasks */}

          <div className="col-12 col-lg-4">

            <DashboardCard title="Pending Tasks">

              <ul className="list-group list-group-flush">

                {pendingTasks.map((task, index) => (
                  <li
                    key={index}
                    className="list-group-item px-0"
                  >
                    <i className="bi bi-check2-square text-primary me-2"></i>

                    {task}
                  </li>
                ))}

              </ul>

            </DashboardCard>

          </div>

        </div>


        {/* Risks and Deadlines */}

        <div className="row g-4">

          {/* Risks */}

          <div className="col-12 col-lg-6">

            <DashboardCard title="Risks">

              <div className="list-group list-group-flush">

                {risks.map((risk, index) => (
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
                ))}

              </div>

            </DashboardCard>

          </div>


          {/* Deadlines */}

          <div className="col-12 col-lg-6">

            <DashboardCard title="Upcoming Deadlines">

              <div className="list-group list-group-flush">

                <div className="list-group-item px-0 d-flex justify-content-between">
                  <span>Website Revamp</span>
                  <strong>Sep 02</strong>
                </div>

                <div className="list-group-item px-0 d-flex justify-content-between">
                  <span>Mobile App Release</span>
                  <strong>Sep 05</strong>
                </div>

                <div className="list-group-item px-0 d-flex justify-content-between">
                  <span>Client Presentation</span>
                  <strong>Sep 08</strong>
                </div>

              </div>

            </DashboardCard>

          </div>

        </div>

      </main>
    </>
  );
}

export default Dashboard;