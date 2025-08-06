import React, { useState } from "react";
import { UserDashboard } from "@/components/UserDashboard";
import { AdminDashboard } from "@/components/AdminDashboard";
import { Button } from "@/components/ui/button";
import { Users, Shield } from "lucide-react";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const [dashboardType, setDashboardType] = useState<"user" | "admin">("user");

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation Toggle */}
      <div className="bg-card border-b p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="text-xl font-bold no-underline text-foreground">
            Complaint Management System
          </Link>
          <div className="flex gap-2">
            <Button
              variant={dashboardType === "user" ? "default" : "outline"}
              onClick={() => setDashboardType("user")}
              className="flex items-center gap-2"
            >
              <Users className="h-4 w-4" />
              User View
            </Button>
            <Button
              variant={dashboardType === "admin" ? "default" : "outline"}
              onClick={() => setDashboardType("admin")}
              className="flex items-center gap-2"
            >
              <Shield className="h-4 w-4" />
              Admin View
            </Button>
          </div>
        </div>
      </div>

      {/* Dashboard Content */}
      {dashboardType === "user" ? <UserDashboard /> : <AdminDashboard />}
    </div>
  );
}
