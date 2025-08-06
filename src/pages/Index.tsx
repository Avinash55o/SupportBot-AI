import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageCircle, Users, Bot, Zap, Clock } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { ComplaintChatbot } from "@/components/ComplaintChatbot";

const Index = () => {
  const navigate = useNavigate();
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const features = [
    {
      icon: <Bot className="h-8 w-8 text-primary" />,
      title: "AI-Powered Chatbot",
      description: "Get instant help with our intelligent assistant that understands and categorizes your complaints automatically."
    },
    {
      icon: <Zap className="h-8 w-8 text-primary" />,
      title: "Smart Ticket Generation",
      description: "Automated ticket creation with intelligent prioritization based on urgency and complexity."
    },
    {
      icon: <Clock className="h-8 w-8 text-primary" />,
      title: "Real-Time Tracking",
      description: "Monitor your complaint status in real-time with detailed progress updates and notifications."
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary/5 to-accent/5 py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6 text-foreground">
            Intelligent Complaint Management
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Experience the future of customer support with AI-powered complaint resolution, 
            smart ticketing, and real-time tracking.
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg" onClick={() => navigate("/dashboard")} className="flex items-center gap-2">
              <MessageCircle className="h-5 w-5" />
              Get Started
            </Button>
            <Button variant="outline" size="lg" onClick={() => navigate("/dashboard")}>
              View Demo
            </Button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Powered by Artificial Intelligence</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our advanced AI system streamlines complaint management from submission to resolution
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* CTA Section */}
          <div className="text-center">
            <Card className="bg-muted/30 border-2 border-dashed border-primary/20">
              <CardContent className="py-12">
                <h3 className="text-2xl font-bold mb-4">Ready to Transform Your Support?</h3>
                <p className="text-muted-foreground mb-6 max-w-lg mx-auto">
                  Join thousands of businesses using our AI-powered complaint management system
                </p>
                <Button size="lg" onClick={() => navigate("/dashboard")} className="flex items-center gap-2 mx-auto">
                  <Users className="h-5 w-5" />
                  Access Dashboard
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
      
      {/* Floating Chatbot Icon */}
      <div className="fixed bottom-4 right-4 z-50">
        <Button
          variant="default"
          size="icon"
          className="h-14 w-14 rounded-full shadow-lg"
          onClick={() => setIsChatbotOpen(!isChatbotOpen)}
        >
          <MessageCircle className="h-8 w-8" />
        </Button>
      </div>

      {/* Chatbot Pop-up */}
      <ComplaintChatbot isOpen={isChatbotOpen} onClose={() => setIsChatbotOpen(false)} />
    </div>
  );
};

export default Index;