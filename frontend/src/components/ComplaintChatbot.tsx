import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, X, Minimize2, Maximize2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";
import { apiService } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  content: string;
  isBot: boolean;
  timestamp: Date;
}

interface ComplaintChatbotProps {
  isOpen: boolean;
  onClose: () => void;
  onComplaintGenerated?: (complaint: any) => void;
}

export function ComplaintChatbot({ isOpen, onClose, onComplaintGenerated }: ComplaintChatbotProps) {
  const { user } = useAuth();
  const { toast } = useToast();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "Hello! I'm here to help you with your complaints. What seems to be the issue today?",
      isBot: true,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [shouldRender, setShouldRender] = useState(isOpen);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen) {
      setShouldRender(true);
    } else {
      const timeoutId = setTimeout(() => {
        setShouldRender(false);
      }, 300); // Match animation duration
      return () => clearTimeout(timeoutId);
    }
  }, [isOpen]);

  const handleClose = () => {
    onClose();
  };

  const toggleMaximize = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsMaximized(!isMaximized);
  };

  const generateBotResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes("billing") || lowerMessage.includes("payment")) {
      return "I understand you have a billing concern. Let me create a high-priority ticket for our billing team to review your account.";
    } else if (lowerMessage.includes("technical") || lowerMessage.includes("not working") || lowerMessage.includes("error")) {
      return "I see you're experiencing technical difficulties. I'll generate a technical support ticket with medium priority for our IT team.";
    } else if (lowerMessage.includes("urgent") || lowerMessage.includes("emergency")) {
      return "This sounds urgent! I'm creating a high-priority ticket that will be escalated immediately to our management team.";
    } else if (lowerMessage.includes("service") || lowerMessage.includes("support")) {
      return "Thank you for reaching out about our service. I'll create a support ticket to address your concerns promptly.";
    } else {
      return "I understand your concern. Let me create a general inquiry ticket for our team to review and respond to your issue.";
    }
  };

  const createTicketInBackend = async (description: string, issueType: string, priority: string) => {
    try {
      // For now, we'll create a simple ticket creation endpoint
      // You can extend this to use the actual API when you implement ticket creation
      const response = await fetch('http://localhost:5000/api/create-ticket', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          issue_type: issueType,
          description: description,
          user_id: user?.id,
          priority: priority
        })
      });

      if (response.ok) {
        const ticket = await response.json();
        return ticket;
      } else {
        throw new Error('Failed to create ticket');
      }
    } catch (error) {
      console.error('Error creating ticket:', error);
      // For now, return a mock ticket
      return {
        id: Date.now(),
        issue_type: issueType,
        description: description,
        status: 'open',
        priority: priority,
        user_id: user?.id,
        created_at: new Date().toISOString()
      };
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isBot: false,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue("");
    setIsTyping(true);

    setTimeout(async () => {
      const botResponse = generateBotResponse(currentInput);
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: botResponse,
        isBot: true,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);

      // Determine ticket details
      const issueType = currentInput.toLowerCase().includes("billing") || currentInput.toLowerCase().includes("payment") ? "Billing" :
                       currentInput.toLowerCase().includes("technical") || currentInput.toLowerCase().includes("not working") || currentInput.toLowerCase().includes("error") ? "Technical Support" :
                       currentInput.toLowerCase().includes("urgent") || currentInput.toLowerCase().includes("emergency") ? "Emergency" :
                       "General Inquiry";
      
      const priority = currentInput.toLowerCase().includes("urgent") || currentInput.toLowerCase().includes("emergency") ? "urgent" :
                       currentInput.toLowerCase().includes("billing") || currentInput.toLowerCase().includes("technical") ? "high" :
                       "normal";

      // Create ticket in backend
      setTimeout(async () => {
        try {
          const ticket = await createTicketInBackend(currentInput, issueType, priority);
          
          toast({
            title: "Ticket Created",
            description: `Your ticket #${ticket.id} has been created successfully!`,
          });

          onComplaintGenerated?.(ticket);
        } catch (error) {
          toast({
            title: "Error",
            description: "Failed to create ticket. Please try again.",
            variant: "destructive",
          });
        }
      }, 1000);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  if (!shouldRender) return null;

  return (
    <div className={cn(
        "fixed z-50",
        isOpen ? "animate-fade-in-slide-up" : "animate-fade-out-slide-down",
        isMaximized
          ? "inset-0 flex items-center justify-center p-4 bg-black/50"
          : "bottom-4 right-4"
    )}>
      <Card className={cn(
        "flex flex-col rounded-xl shadow-lg border-2 border-primary/20 transition-all duration-300 ease-in-out",
        isMaximized ? "w-full max-w-4xl h-full max-h-[90vh] mx-auto" : "w-96 h-[400px]"
      )}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-4 border-b">
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-6 w-6 text-primary" />
            <span className="text-xl">Support Assistant</span>
          </CardTitle>
          <div className="flex gap-2">
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full" onClick={toggleMaximize}>
              {isMaximized ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full" onClick={handleClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 flex flex-col p-4 overflow-hidden">
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 custom-scrollbar">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isBot ? "justify-start" : "justify-end"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl p-3 ${
                    message.isBot
                      ? "bg-muted text-muted-foreground"
                      : "bg-primary text-primary-foreground"
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {message.isBot && <Bot className="h-4 w-4 mt-0.5 flex-shrink-0" />}
                    <span className="text-sm leading-snug">{message.content}</span>
                    {!message.isBot && <User className="h-4 w-4 mt-0.5 flex-shrink-0" />}
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-muted text-muted-foreground rounded-2xl p-3 max-w-[80%]">
                  <div className="flex items-center gap-2">
                    <Bot className="h-4 w-4" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:0.1s]"></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:0.2s]"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="relative p-2 border-t flex items-center">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your issue..."
              className="w-full rounded-full pr-10"
            />
            <Button onClick={handleSendMessage} size="icon" className="absolute right-4 w-8 h-8 rounded-full">
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}