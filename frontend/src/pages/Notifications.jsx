import { useEffect, useState } from "react";

import {
    getNotifications,
    markNotificationRead,
} from "../services/notificationService";

import { sendNotificationEmail } from "../services/emailService";

function Notifications() {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function sendEmailForNotification(notification) {
        // Only send emails for email-channel notifications
        if (notification.channel !== "email") {
            return;
        }

        // Prevent duplicate emails
        const sentKey = `notification_email_sent_${notification.id} `;

        if (localStorage.getItem(sentKey)) {
            return;
        }

        try {
            const result = await sendNotificationEmail({
                to_name: notification.username,
                to_email: notification.email,
                message: notification.message,
                notification_type: notification.notification_type,
                notification_time: new Date(
                    notification.created_at
                ).toLocaleString(),
            });

            if (result.success) {
                localStorage.setItem(sentKey, "true");

                console.log(
                    `Email sent successfully for notification ${notification.id}`
                );
            } else {
                console.error(
                    `Email failed for notification ${notification.id}`
                );
            }
        } catch (err) {
            console.error(
                `EmailJS error for notification ${notification.id}: `,
                err
            );
        }
    }

    async function loadNotifications() {
        try {
            setLoading(true);
            setError("");

            const accessToken = localStorage.getItem("access_token");

            if (!accessToken) {
                throw new Error("You are not logged in.");
            }

            const data = await getNotifications(accessToken);

            setNotifications(data);

            // Send EmailJS emails only for email-channel notifications
            for (const notification of data) {
                await sendEmailForNotification(notification);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadNotifications();
    }, []);

    async function handleMarkAsRead(notificationId) {
        try {
            const accessToken = localStorage.getItem("access_token");

            if (!accessToken) {
                throw new Error("You are not logged in.");
            }

            const updatedNotification = await markNotificationRead(
                notificationId,
                accessToken
            );

            setNotifications((currentNotifications) =>
                currentNotifications.map((notification) =>
                    notification.id === updatedNotification.id
                        ? updatedNotification
                        : notification
                )
            );
        } catch (err) {
            setError(err.message);
        }
    }

    function getPriorityClass(priority) {
        switch (priority) {
            case "critical":
                return "danger";

            case "high":
                return "warning";

            case "medium":
                return "primary";

            default:
                return "secondary";
        }
    }

    return (
        <>
            <div className="container py-4">

                <div className="d-flex justify-content-between align-items-center mb-4">
                    <h2 className="mb-0">
                        Notifications
                    </h2>

                    <button
                        type="button"
                        className="btn btn-outline-primary"
                        onClick={loadNotifications}
                    >
                        <i className="bi bi-arrow-clockwise me-1"></i>
                        Refresh
                    </button>
                </div>

                {error && (
                    <div className="alert alert-danger">
                        {error}
                    </div>
                )}

                {loading ? (
                    <div className="text-center py-5">

                        <div
                            className="spinner-border text-primary"
                            role="status"
                        >
                            <span className="visually-hidden">
                                Loading...
                            </span>
                        </div>

                        <p className="mt-3 mb-0">
                            Loading notifications...
                        </p>

                    </div>
                ) : notifications.length === 0 ? (

                    <div className="alert alert-info">
                        <i className="bi bi-info-circle me-2"></i>
                        No notifications found.
                    </div>

                ) : (

                    <div className="row g-3">

                        {notifications.map((notification) => (

                            <div
                                className="col-12"
                                key={notification.id}
                            >

                                <div
                                    className={`card shadow - sm ${notification.is_read
                                        ? ""
                                        : "border-primary"
                                        } `}
                                >

                                    <div className="card-body">

                                        <div className="d-flex justify-content-between align-items-start gap-3">

                                            <div>
                                                <h5 className="card-title mb-2">
                                                    {notification.title}
                                                </h5>

                                                <p className="card-text mb-2">
                                                    {notification.message}
                                                </p>
                                            </div>

                                            <span
                                                className={`badge text - bg - ${getPriorityClass(
                                                    notification.priority
                                                )
                                                    } `}
                                            >
                                                {notification.priority}
                                            </span>

                                        </div>

                                        <div className="small text-muted mb-3">

                                            <span className="me-3">
                                                Type:{" "}
                                                {notification.notification_type}
                                            </span>

                                            <span className="me-3">
                                                Channel:{" "}
                                                {notification.channel}
                                            </span>

                                            <span>
                                                {new Date(
                                                    notification.created_at
                                                ).toLocaleString()}
                                            </span>

                                        </div>

                                        {!notification.is_read ? (

                                            <button
                                                type="button"
                                                className="btn btn-sm btn-primary"
                                                onClick={() =>
                                                    handleMarkAsRead(
                                                        notification.id
                                                    )
                                                }
                                            >
                                                <i className="bi bi-check2 me-1"></i>
                                                Mark as Read
                                            </button>

                                        ) : (

                                            <span className="badge text-bg-success">
                                                <i className="bi bi-check-circle me-1"></i>
                                                Read
                                            </span>

                                        )}

                                    </div>

                                </div>

                            </div>

                        ))}

                    </div>

                )}

            </div>
        </>
    );
}

export default Notifications;

