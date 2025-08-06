import React, { useState } from "react";
import { MessageCircle, Plus, Search, Clock, CheckCircle, AlertTriangle, ChevronRight, Ticket, UserCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ComplaintChatbot } from "./ComplaintChatbot";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

interface Complaint {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: "Low" | "Medium" | "High" | "Critical";
  status: "Open" | "In Progress" | "Resolved" | "Closed";
  createdAt: Date;
  updatedAt: Date;
}

interface Activity {
  id: number;
  type: "new_ticket" | "status_change" | "new_message";
  details: string;
  timestamp: string;
  icon: React.ReactNode;
}

export const UserDashboard = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([
    {
      id: "TICKET-001",
      title: "Login Issues",
      description: "Unable to login to my account",
      category: "Technical",
      priority: "High",
      status: "In Progress",
      createdAt: new Date("2024-01-15"),
      updatedAt: new Date("2024-01-16"),
    },
    {
      id: "TICKET-002",
      title: "Billing Discrepancy",
      description: "Incorrect charges on my account",
      category: "Billing",
      priority: "Medium",
      status: "Open",
      createdAt: new Date("2024-01-14"),
      updatedAt: new Date("2024-01-14"),
    },
    {
      id: "TICKET-004",
      title: "Slow Service",
      description: "The service has been very slow lately.",
      category: "Service",
      priority: "Low",
      status: "Open",
      createdAt: new Date("2024-01-18"),
      updatedAt: new Date("2024-01-18"),
    },
  ]);
  
  const [recentActivity] = useState<Activity[]>([
    { id: 1, type: 'new_ticket', details: 'You created a new ticket #TICKET-004.', timestamp: '2 hours ago', icon: <Ticket className="h-5 w-5 text-blue-500" /> },
    { id: 2, type: 'status_change', details: 'Your ticket #TICKET-001 is now In Progress.', timestamp: '3 hours ago', icon: <UserCheck className="h-5 w-5 text-green-500" /> },
    { id: 3, type: 'new_message', details: 'You received a new message on #TICKET-001.', timestamp: '5 hours ago', icon: <MessageCircle className="h-5 w-5 text-yellow-500" /> },
  ]);

  const [searchQuery, setSearchQuery] = useState("");
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "Critical": return "destructive";
      case "High": return "destructive";
      case "Medium": return "secondary";
      case "Low": return "outline";
      default: return "outline";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "Open": return <Clock className="h-4 w-4 text-yellow-500" />;
      case "In Progress": return <AlertTriangle className="h-4 w-4 text-blue-500" />;
      case "Resolved": return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "Closed": return <CheckCircle className="h-4 w-4 text-gray-500" />;
      default: return <Clock className="h-4 w-4" />;
    }
  };

  const handleComplaintGenerated = (newComplaint: any) => {
    const complaint: Complaint = {
      ...newComplaint,
      title: newComplaint.description.slice(0, 50) + "...",
      updatedAt: new Date(),
    };
    setComplaints(prev => [complaint, ...prev]);
    setIsChatbotOpen(false);
  };

  const filteredComplaints = complaints.filter(complaint =>
    complaint.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    complaint.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    complaint.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const statsData = [
    {
      title: "Total Complaints",
      value: complaints.length,
      description: "All time submissions",
    },
    {
      title: "Open Issues",
      value: complaints.filter(c => c.status === "Open" || c.status === "In Progress").length,
      description: "Awaiting resolution",
    },
    {
      title: "Resolved",
      value: complaints.filter(c => c.status === "Resolved" || c.status === "Closed").length,
      description: "Successfully handled",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50/50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Welcome Back!</h1>
            <p className="text-muted-foreground">Here's a summary of your support requests.</p>
          </div>
          <Button onClick={() => setIsChatbotOpen(true)} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            New Complaint
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {statsData.map((stat, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-300">
              <CardHeader className="pb-3">
                <CardDescription>{stat.title}</CardDescription>
                <CardTitle className="text-3xl font-bold">{stat.value}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{stat.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            {/* Complaints Table */}
            <Card>
              <CardHeader>
                <CardTitle>My Complaints</CardTitle>
                <div className="relative mt-2">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search complaints..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Status</TableHead>
                      <TableHead>Ticket ID</TableHead>
                      <TableHead>Title</TableHead>
                      <TableHead>Priority</TableHead>
                      <TableHead>Last Updated</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredComplaints.length > 0 ? (
                      filteredComplaints.map((complaint) => (
                        <TableRow key={complaint.id} className="hover:bg-gray-50">
                          <TableCell>
                            <div className="flex items-center gap-2">
                              {getStatusIcon(complaint.status)}
                              <span>{complaint.status}</span>
                            </div>
                          </TableCell>
                          <TableCell className="font-medium">{complaint.id}</TableCell>
                          <TableCell>{complaint.title}</TableCell>
                          <TableCell>
                            <Badge variant={getPriorityColor(complaint.priority)}>
                              {complaint.priority}
                            </Badge>
                          </TableCell>
                          <TableCell>{complaint.updatedAt.toLocaleDateString()}</TableCell>
                          <TableCell>
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button variant="outline" size="sm">View</Button>
                              </DialogTrigger>
                              <DialogContent>
                                <DialogHeader>
                                  <DialogTitle>Complaint Details</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                  <p><strong>ID:</strong> {complaint.id}</p>
                                  <p><strong>Title:</strong> {complaint.title}</p>
                                  <p><strong>Description:</strong> {complaint.description}</p>
                                  <p><strong>Category:</strong> {complaint.category}</p>
                                  <p><strong>Priority:</strong> {complaint.priority}</p>
                                  <p><strong>Status:</strong> {complaint.status}</p>
                                </div>
                              </DialogContent>
                            </Dialog>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={7} className="h-24 text-center">
                          No complaints found.
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
          
          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivity.map(activity => (
                  <div key={activity.id} className="flex items-start gap-4">
                    <div className="bg-gray-100 p-2 rounded-full">
                      {activity.icon}
                    </div>
                    <div>
                      <p className="text-sm">{activity.details}</p>
                      <p className="text-xs text-muted-foreground">{activity.timestamp}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <ComplaintChatbot
        isOpen={isChatbotOpen}
        onClose={() => setIsChatbotOpen(false)}
        onComplaintGenerated={handleComplaintGenerated}
      />
    </div>
  );
}
