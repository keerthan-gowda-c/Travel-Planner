import { Outlet } from "react-router-dom";
import "./MainLayout.css";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function MainLayout(){
    return(
        <div className="app-layout">
            <Sidebar/>
             <main className="main-content">
                <Navbar/>
                <section className="page-content">
                    <Outlet/>
                </section>
             </main>
        </div>
    )
}