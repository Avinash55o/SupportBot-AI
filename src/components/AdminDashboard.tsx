import React, { useState } from "react";
import { Users, Clock, TrendingUp, AlertTriangle, CheckCircle, Settings, Search, Ticket, MessageSquare, UserCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Bar, BarChart as RechartsBarChart, Pie, PieChart as RechartsPieChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Cell } from "recharts";

interface Ticket {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: "Low" | "Medium" | "High" | "Critical";
  status: "Open" | "In Progress" | "Resolved" | "Closed";
  assignedTo: string;
  customer: string;
  createdAt: Date;
  updatedAt: Date;
  aiSuggestion?: string;
}

interface Activity {
  id: number;
  type: "new_ticket" | "status_change" | "new_message";
  details: string;
  timestamp: string;
  icon: React.ReactNode;
}

export const AdminDashboard = () => {
  const [tickets, setTickets] = useState<Ticket[]>([
    {
      id: "TICKET-001",
      title: "Login Issues",
      description: "Unable to login to my account",
      category: "Technical",
      priority: "High",
      status: "In Progress",
      assignedTo: "Tech Team",
      customer: "John Doe",
      createdAt: new Date("2024-01-15"),
      updatedAt: new Date("2024-01-16"),
      aiSuggestion: "Suggest password reset and 2FA setup",
    },
    {
      id: "TICKET-002",
      title: "Billing Discrepancy",
      description: "Incorrect charges on my account",
      category: "Billing",
      priority: "Medium",
      status: "Open",
      assignedTo: "Billing Team",
      customer: "Jane Smith",
      createdAt: new Date("2024-01-14"),
      updatedAt: new Date("2024-01-14"),
      aiSuggestion: "Review transaction history and apply refund if necessary",
    },
    {
      id: "TICKET-003",
      title: "Service Outage",
      description: "Website not accessible",
      category: "Technical",
      priority: "Critical",
      status: "Open",
      assignedTo: "Infrastructure Team",
      customer: "Bob Johnson",
      createdAt: new Date("2024-01-16"),
      updatedAt: new Date("2024-01-16"),
      aiSuggestion: "Escalate to senior technical team immediately",
    },
    {
      id: "TICKET-004",
      title: "Slow Service",
      description: "The service has been very slow lately.",
      category: "Service",
      priority: "Low",
      status: "Open",
      assignedTo: "Support Team",
      customer: "Alice Williams",
      createdAt: new Date("2024-01-18"),
      updatedAt: new Date("2024-01-18"),
      aiSuggestion: "Check for any ongoing service disruptions.",
    },
  ]);

  const [recentActivity] = useState<Activity[]>([
    { id: 1, type: 'new_ticket', details: 'New ticket #TICKET-004 created by Alice Williams.', timestamp: '2 hours ago', icon: <Ticket className="h-5 w-5 text-blue-500" /> },
    { id: 2, type: 'status_change', details: 'Ticket #TICKET-001 status changed to In Progress.', timestamp: '3 hours ago', icon: <UserCheck className="h-5 w-5 text-green-500" /> },
    { id: 3, type: 'new_message', details: 'New message from John Doe on #TICKET-001.', timestamp: '5 hours ago', icon: <MessageSquare className="h-5 w-5 text-yellow-500" /> },
  ]);

  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");

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

  const filteredTickets = tickets.filter(ticket => {
    const matchesSearch = ticket.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         ticket.customer.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         ticket.id.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === "all" || ticket.status === statusFilter;
    const matchesPriority = priorityFilter === "all" || ticket.priority === priorityFilter;
    
    return matchesSearch && matchesStatus && matchesPriority;
  });

  const statsData = [
    {
      title: "Total Tickets",
      value: tickets.length,
      description: "All time submissions",
      icon: <Users className="h-6 w-6 text-primary" />,
    },
    {
      title: "Open Tickets",
      value: tickets.filter(t => t.status === "Open").length,
      description: "Awaiting assignment",
      icon: <Clock className="h-6 w-6 text-yellow-500" />,
    },
    {
      title: "In Progress",
      value: tickets.filter(t => t.status === "In Progress").length,
      description: "Being worked on",
      icon: <TrendingUp className="h-6 w-6 text-blue-500" />,
    },
    {
      title: "Critical Issues",
      value: tickets.filter(t => t.priority === "Critical").length,
      description: "Require immediate attention",
      icon: <AlertTriangle className="h-6 w-6 text-red-500" />,
    },
  ];

  const ticketStatusData = [
    { name: 'Open', value: tickets.filter(t => t.status === 'Open').length },
    { name: 'In Progress', value: tickets.filter(t => t.status === 'In Progress').length },
    { name: 'Resolved', value: tickets.filter(t => t.status === 'Resolved').length },
  ];
  
  const ticketPriorityData = [
    { name: 'Low', value: tickets.filter(t => t.priority === 'Low').length, color: '#60a5fa' },
    { name: 'Medium', value: tickets.filter(t => t.priority === 'Medium').length, color: '#facc15' },
    { name: 'High', value: tickets.filter(t => t.priority === 'High').length, color: '#f97316' },
    { name: 'Critical', value: tickets.filter(t => t.priority === 'Critical').length, color: '#ef4444' },
  ];

  return (
    <div className="min-h-screen bg-gray-50/50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Admin Dashboard</h1>
            <p className="text-muted-foreground">Manage and monitor all support tickets</p>
          </div>
          <Button variant="outline" className="flex items-center gap-2">
            <Settings className="h-4 w-4" />
            Settings
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {statsData.map((stat, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">{stat.title}</CardTitle>
                {stat.icon}
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">{stat.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Charts */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Tickets by Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <RechartsBarChart data={ticketStatusData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                    </RechartsBarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Tickets by Priority</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <RechartsPieChart>
                      <Pie data={ticketPriorityData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                        {ticketPriorityData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </RechartsPieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
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

        {/* Tickets Table */}
        <Card>
          <CardHeader>
            <CardTitle>Support Tickets</CardTitle>
            <CardDescription>Manage and track all customer complaints</CardDescription>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search tickets..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full sm:w-[180px]">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="Open">Open</SelectItem>
                  <SelectItem value="In Progress">In Progress</SelectItem>
                  <SelectItem value="Resolved">Resolved</SelectItem>
                  <SelectItem value="Closed">Closed</SelectItem>
                </SelectContent>
              </Select>
              <Select value={priorityFilter} onValueChange={setPriorityFilter}>
                <SelectTrigger className="w-full sm:w-[180px]">
                  <SelectValue placeholder="Filter by priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Priority</SelectItem>
                  <SelectItem value="Critical">Critical</SelectItem>
                  <SelectItem value="High">High</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="Low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ticket ID</TableHead>
                    <TableHead>Customer</TableHead>
                    <TableHead>Title</TableHead>
                    <TableHead>Priority</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Assigned To</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredTickets.map((ticket) => (
                    <TableRow key={ticket.id} className="hover:bg-gray-50">
                      <TableCell className="font-medium">{ticket.id}</TableCell>
                      <TableCell>{ticket.customer}</TableCell>
                      <TableCell className="max-w-xs truncate">{ticket.title}</TableCell>
                      <TableCell>
                        <Badge variant={getPriorityColor(ticket.priority)}>
                          {ticket.priority}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(ticket.status)}
                          <span className="text-sm">{ticket.status}</span>
                        </div>
                      </TableCell>
                      <TableCell>{ticket.assignedTo}</TableCell>
                      <TableCell>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm">View</Button>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Ticket Details</DialogTitle>
                            </DialogHeader>
                            <div className="space-y-4 py-4">
                              <p><strong>ID:</strong> {ticket.id}</p>
                              <p><strong>Customer:</strong> {ticket.customer}</p>
                              <p><strong>Title:</strong> {ticket.title}</p>
                              <p><strong>Description:</strong> {ticket.description}</p>
                              <p><strong>Category:</strong> {ticket.category}</p>
                              <p><strong>Priority:</strong> {ticket.priority}</p>
                              <p><strong>Status:</strong> {ticket.status}</p>
                              <p><strong>Assigned To:</strong> {ticket.assignedTo}</p>
                              {ticket.aiSuggestion && <p className="text-sm bg-blue-50 p-3 rounded-lg"><strong>AI Suggestion:</strong> {ticket.aiSuggestion}</p>}
                            </div>
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default AdminDashboard;
