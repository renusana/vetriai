function StatCard({ title, value, icon, description }) {
    return (
        <div className="col-12 col-sm-6 col-xl-3 mb-4">
            <div className="card dashboard-stat-card shadow-sm h-100">

                <div className="card-body">

                    <div className="d-flex justify-content-between align-items-start">

                        <div>
                            <p className="dashboard-stat-title mb-2">
                                {title}
                            </p>

                            <h3 className="dashboard-stat-value mb-1">
                                {value}
                            </h3>

                            <small className="dashboard-stat-description">
                                {description}
                            </small>
                        </div>

                        <div className="dashboard-stat-icon">
                            <i className={`bi ${icon}`}></i>
                        </div>

                    </div>

                </div>

            </div>
        </div>
    );
}

export default StatCard;