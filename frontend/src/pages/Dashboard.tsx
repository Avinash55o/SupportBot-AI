import React, { useState, useEffect } from "react";
import { UserDashboard } from "@/components/UserDashboard";
import { AdminDashboard } from "@/components/AdminDashboard";
import { Button } from "@/components/ui/button";
import { Users, Shield, LogOut } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

export default function Dashboard() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const navigate = useNavigate();
  const [dashboardType, setDashboardType] = useState<"user" | "admin">("user");

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated, isLoading, navigate]);

  // Set dashboard type based on user role
  useEffect(() => {
    if (user) {
      const isAdmin = localStorage.getItem('isAdmin') === 'true' || user.is_admin;
      setDashboardType(isAdmin ? "admin" : "user");
    }
  }, [user]);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation Toggle */}
      <div className="bg-card border-b p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="text-xl font-bold no-underline text-foreground">
            Complaint Management System
          </Link>
          <div className="flex items-center gap-4">
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
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">
                Welcome, {user?.name}
              </span>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Dashboard Content */}
      {dashboardType === "user" ? <UserDashboard /> : <AdminDashboard />}
    </div>
  );
}