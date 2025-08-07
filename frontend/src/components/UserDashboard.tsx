import React, { useState } from "react";
import { MessageCircle, Plus, Search, Clock, CheckCircle, AlertTriangle, ChevronRight, Ticket, UserCheck, Copy } from "lucide-react";
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
import { useAuth } from "@/hooks/useAuth";
import { useUserTickets } from "@/hooks/useTickets";
import { Ticket as TicketType } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface Activity {
  id: number;
  type: "new_ticket" | "status_change" | "new_message";
  details: string;
  timestamp: string;
  icon: React.ReactNode;
}

export const UserDashboard = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [searchQuery, setSearchQuery] = useState("");
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  // Fetch tickets from backend
  const { data: ticketsData, isLoading, error } = useUserTickets(user?.id || 0);

  const tickets = ticketsData?.data?.tickets || [];

  const [recentActivity] = useState<Activity[]>([
    { id: 1, type: 'new_ticket', details: 'You created a new ticket.', timestamp: '2 hours ago', icon: <Ticket className="h-5 w-5 text-blue-500" /> },
    { id: 2, type: 'status_change', details: 'Your ticket status was updated.', timestamp: '3 hours ago', icon: <UserCheck className="h-5 w-5 text-green-500" /> },
    { id: 3, type: 'new_message', details: 'You received a new message.', timestamp: '5 hours ago', icon: <MessageCircle className="h-5 w-5 text-yellow-500" /> },
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

  const handleComplaintGenerated = (newComplaint: any) => {
    toast({
      title: "Ticket Created",
      description: "Your complaint has been submitted successfully!",
    });
    setIsChatbotOpen(false);
  };

  const filteredTickets = tickets.filter(ticket =>
    ticket.issue_type.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ticket.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const statsData = [
    {
      title: "Total Complaints",
      value: tickets.length,
      description: "All time submissions",
    },
    {
      title: "Open Issues",
      value: tickets.filter(t => t.status === "open" || t.status === "in_progress").length,
      description: "Awaiting resolution",
    },
    {
      title: "Resolved",
      value: tickets.filter(t => t.status === "resolved" || t.status === "closed").length,
      description: "Successfully handled",
    },
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50/50 p-4 sm:p-6 lg:p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="flex justify-center items-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Loading your tickets...</p>
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
              <p className="text-muted-foreground mb-4">Unable to load your tickets. Please try again.</p>
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
            <h1 className="text-3xl font-bold text-gray-800">Welcome Back, {user?.name}!</h1>
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
                      <TableHead>Ticket Token</TableHead>
                      <TableHead>Issue Type</TableHead>
                      <TableHead>Priority</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredTickets.length > 0 ? (
                      filteredTickets.map((ticket) => (
                        <TableRow key={ticket.id} className="hover:bg-gray-50">
                          <TableCell>
                            <div className="flex items-center gap-2">
                              {getStatusIcon(ticket.status)}
                              <span>{formatStatus(ticket.status)}</span>
                            </div>
                          </TableCell>
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
                          <TableCell>
                            <Badge variant={getPriorityColor(ticket.priority)}>
                              {formatPriority(ticket.priority)}
                            </Badge>
                          </TableCell>
                          <TableCell>{new Date(ticket.created_at).toLocaleDateString()}</TableCell>
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
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={6} className="h-24 text-center">
                          {searchQuery ? "No complaints found matching your search." : "No complaints found. Create your first one!"}
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
};