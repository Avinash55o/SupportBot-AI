import React, { useState } from "react";
import { Users, Clock, TrendingUp, AlertTriangle, CheckCircle, Settings, Search, Ticket, MessageSquare, UserCheck, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Bar, BarChart as RechartsBarChart, Pie, PieChart as RechartsPieChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Cell } from "recharts";
import { useAllTickets, useUpdateTicketStatus, useAnalytics } from "@/hooks/useTickets";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/use-toast";

interface Activity {
  id: number;
  type: "new_ticket" | "status_change" | "new_message";
  details: string;
  timestamp: string;
  icon: React.ReactNode;
}

export const AdminDashboard = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");

  // Fetch all tickets from backend
  const { data: ticketsData, isLoading, error } = useAllTickets();
  const { data: analyticsData } = useAnalytics();
  const updateTicketStatus = useUpdateTicketStatus();

  const tickets = ticketsData?.data?.tickets || [];

  const [recentActivity] = useState<Activity[]>([
    { id: 1, type: 'new_ticket', details: 'New ticket created.', timestamp: '2 hours ago', icon: <Ticket className="h-5 w-5 text-blue-500" /> },
    { id: 2, type: 'status_change', details: 'Ticket status updated.', timestamp: '3 hours ago', icon: <UserCheck className="h-5 w-5 text-green-500" /> },
    { id: 3, type: 'new_message', details: 'New message received.', timestamp: '5 hours ago', icon: <MessageSquare className="h-5 w-5 text-yellow-500" /> },
  ]);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "urgent": return "destructive";
      case "high": return "destructive";
      case "normal": return "secondary";
      case "low": return "outline";
      default: return "outline";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "open": return <Clock className="h-4 w-4 text-yellow-500" />;
      case "in_progress": return <AlertTriangle className="h-4 w-4 text-blue-500" />;
      case "resolved": return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "closed": return <CheckCircle className="h-4 w-4 text-gray-500" />;
      default: return <Clock className="h-4 w-4" />;
    }
  };

  const formatStatus = (status: string) => {
    return status.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const formatPriority = (priority: string) => {
    return priority.charAt(0).toUpperCase() + priority.slice(1);
  };

  const handleStatusUpdate = async (ticketId: number, newStatus: string) => {
    try {
      await updateTicketStatus.mutateAsync({
        ticketId,
        status: newStatus,
        notes: `Status updated to ${formatStatus(newStatus)} by admin`
      });
      
      toast({
        title: "Status Updated",
        description: `Ticket #${ticketId} status has been updated to ${formatStatus(newStatus)}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update ticket status",
        variant: "destructive",
      });
    }
  };

  const filteredTickets = tickets.filter(ticket => {
    const matchesSearch = ticket.issue_type.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         ticket.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         ticket.id.toString().includes(searchQuery);
    
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
      value: tickets.filter(t => t.status === "open").length,
      description: "Awaiting assignment",
      icon: <Clock className="h-6 w-6 text-yellow-500" />,
    },
    {
      title: "In Progress",
      value: tickets.filter(t => t.status === "in_progress").length,
      description: "Being worked on",
      icon: <TrendingUp className="h-6 w-6 text-blue-500" />,
    },
    {
      title: "High Priority",
      value: tickets.filter(t => t.priority === "high" || t.priority === "urgent").length,
      description: "Require attention",
      icon: <AlertTriangle className="h-6 w-6 text-red-500" />,
    },
  ];

  const ticketStatusData = [
    { name: 'Open', value: tickets.filter(t => t.status === 'open').length },
    { name: 'In Progress', value: tickets.filter(t => t.status === 'in_progress').length },
    { name: 'Resolved', value: tickets.filter(t => t.status === 'resolved').length },
    { name: 'Closed', value: tickets.filter(t => t.status === 'closed').length },
  ];
  
  const ticketPriorityData = [
    { name: 'Low', value: tickets.filter(t => t.priority === 'low').length, color: '#60a5fa' },
    { name: 'Normal', value: tickets.filter(t => t.priority === 'normal').length, color: '#facc15' },
    { name: 'High', value: tickets.filter(t => t.priority === 'high').length, color: '#f97316' },
    { name: 'Urgent', value: tickets.filter(t => t.priority === 'urgent').length, color: '#ef4444' },
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50/50 p-4 sm:p-6 lg:p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="flex justify-center items-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Loading tickets...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50/50 p-4 sm:p-6 lg:p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="flex justify-center items-center h-64">
            <div className="text-center">
              <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Error Loading Tickets</h3>
              <p className="text-muted-foreground mb-4">Unable to load tickets. Please try again.</p>
              <Button onClick={() => window.location.reload()}>Retry</Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

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
                  <SelectItem value="open">Open</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="resolved">Resolved</SelectItem>
                  <SelectItem value="closed">Closed</SelectItem>
                </SelectContent>
              </Select>
              <Select value={priorityFilter} onValueChange={setPriorityFilter}>
                <SelectTrigger className="w-full sm:w-[180px]">
                  <SelectValue placeholder="Filter by priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Priority</SelectItem>
                  <SelectItem value="urgent">Urgent</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="normal">Normal</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ticket Token</TableHead>
                    <TableHead>Issue Type</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Priority</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredTickets.map((ticket) => (
                    <TableRow key={ticket.id} className="hover:bg-gray-50">
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="font-mono text-xs bg-blue-50 border-blue-200 text-blue-700">
                            {ticket.token}
                          </Badge>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => navigator.clipboard.writeText(ticket.token)}
                            className="h-6 w-6 p-0 hover:bg-blue-100"
                          >
                            <Copy className="h-3 w-3 text-blue-600" />
                          </Button>
                        </div>
                      </TableCell>
                      <TableCell>{ticket.issue_type}</TableCell>
                      <TableCell className="max-w-xs truncate">{ticket.description}</TableCell>
                      <TableCell>
                        <Badge variant={getPriorityColor(ticket.priority)}>
                          {formatPriority(ticket.priority)}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(ticket.status)}
                          <span className="text-sm">{formatStatus(ticket.status)}</span>
                        </div>
                      </TableCell>
                      <TableCell>{new Date(ticket.created_at).toLocaleDateString()}</TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm">View</Button>
                            </DialogTrigger>
                            <DialogContent>
                              <DialogHeader>
                                <DialogTitle>Ticket Details</DialogTitle>
                              </DialogHeader>
                              <div className="space-y-4 py-4">
                                <div className="flex items-center gap-2">
                                  <p><strong>Token:</strong></p>
                                  <Badge variant="outline" className="font-mono bg-blue-50 border-blue-200 text-blue-700">
                                    {ticket.token}
                                  </Badge>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => navigator.clipboard.writeText(ticket.token)}
                                    className="h-6 w-6 p-0 hover:bg-blue-100"
                                  >
                                    <Copy className="h-3 w-3 text-blue-600" />
                                  </Button>
                                </div>
                                <p><strong>ID:</strong> #{ticket.id}</p>
                                <p><strong>Issue Type:</strong> {ticket.issue_type}</p>
                                <p><strong>Description:</strong> {ticket.description}</p>
                                <p><strong>Priority:</strong> {formatPriority(ticket.priority)}</p>
                                <p><strong>Status:</strong> {formatStatus(ticket.status)}</p>
                                <p><strong>Created:</strong> {new Date(ticket.created_at).toLocaleString()}</p>
                                <p><strong>Updated:</strong> {new Date(ticket.updated_at).toLocaleString()}</p>
                                {ticket.notes && <p><strong>Notes:</strong> {ticket.notes}</p>}
                              </div>
                            </DialogContent>
                          </Dialog>
                          <Select onValueChange={(value) => handleStatusUpdate(ticket.id, value)}>
                            <SelectTrigger className="w-[140px]">
                              <SelectValue placeholder="Update Status" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="open">Open</SelectItem>
                              <SelectItem value="in_progress">In Progress</SelectItem>
                              <SelectItem value="resolved">Resolved</SelectItem>
                              <SelectItem value="closed">Closed</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
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
};

export default AdminDashboard;