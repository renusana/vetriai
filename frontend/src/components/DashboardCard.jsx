function DashboardCard({ title, children }) {
    return (
        <div className="card dashboard-section-card shadow-sm h-100">

            <div className="card-header">
                <h5 className="dashboard-section-title mb-0">
                    {title}
                </h5>
            </div>

            <div className="card-body">
                {children}
            </div>

        </div>
    );
}

export default DashboardCard;