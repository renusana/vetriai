function ActivityList({ activities }) {
    return (
        <div className="dashboard-activity-list">

            {activities.map((activity) => (
                <div
                    key={activity.id}
                    className="dashboard-activity-item"
                >

                    <div className="dashboard-activity-icon">
                        <i className="bi bi-activity"></i>
                    </div>

                    <div className="dashboard-activity-content">

                        <div className="d-flex justify-content-between gap-3">

                            <div>
                                <h6 className="dashboard-activity-title mb-1">
                                    {activity.title}
                                </h6>

                                <p className="dashboard-activity-description mb-0">
                                    {activity.description}
                                </p>
                            </div>

                            <small className="dashboard-activity-time">
                                {activity.time}
                            </small>

                        </div>

                    </div>

                </div>
            ))}

        </div>
    );
}

export default ActivityList;