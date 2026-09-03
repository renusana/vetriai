import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import DashboardNavbar from "../components/DashboardNavbar";

function DashboardLayout() {
    return (
        <div className="app-layout">

            <Sidebar />

            <div className="main-area">

                <DashboardNavbar />

                <main className="page-content">
                    <Outlet />
                </main>

            </div>

        </div>
    );
}

export default DashboardLayout;

