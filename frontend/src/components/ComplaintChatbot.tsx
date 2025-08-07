import React, { useState, useRef, useEffect } from "react";
import { 
  Send, 
  Bot, 
  User, 
  X, 
  Minimize2, 
  Maximize2, 
  Brain, 
  Zap, 
  Ticket, 
  AlertCircle, 
  Copy,
  CheckCircle,
  Clock,
  MessageCircle,
  ChevronDown,
  ChevronUp
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";
import { apiService } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  content: string;
  isBot: boolean;
  timestamp: Date;
  analysis?: any;
  entities?: any;
  ticketCreated?: boolean;
  ticketId?: number;
  ticketToken?: string;
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
      content: "Hello! I'm your AI-powered support assistant. I can help you with complaints, categorize issues, and create tickets automatically. What seems to be the issue today?",
      isBot: true,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [aiAnalysis, setAiAnalysis] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [copiedToken, setCopiedToken] = useState<string | null>(null);
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
      setIsMinimized(false);
    } else {
      const timeoutId = setTimeout(() => {
        setShouldRender(false);
      }, 300);
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

  const toggleMinimize = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsMinimized(!isMinimized);
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedToken(text);
      toast({
        title: "Token Copied!",
        description: "Ticket token has been copied to clipboard",
      });
      setTimeout(() => setCopiedToken(null), 2000);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

  const analyzeComplaintWithAI = async (text: string) => {
    try {
      const response = await apiService.analyzeComplaint(text);
      if (response.data) {
        return response.data;
      } else {
        throw new Error(response.error || 'Failed to analyze complaint');
      }
    } catch (error) {
      console.error('Error analyzing complaint:', error);
      return null;
    }
  };

  const createTicketWithAI = async (description: string) => {
    try {
      const response = await apiService.createTicket({
        description: description,
        user_id: user?.id
      });
      
      if (response.data) {
        return response.data;
      } else {
        throw new Error(response.error || 'Failed to create ticket');
      }
    } catch (error) {
      console.error('Error creating ticket:', error);
      return null;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

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
    setIsProcessing(true);

    try {
      // Analyze complaint with AI
      const analysis = await analyzeComplaintWithAI(currentInput);
      
      if (analysis) {
        setAiAnalysis(analysis);
        
        // Create intelligent response
        const intelligentResponse = analysis.intelligent_response || 
          "I understand your concern. Let me create a ticket for our team to review and address your issue.";
        
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: intelligentResponse,
          isBot: true,
          timestamp: new Date(),
          analysis: analysis.analysis,
          entities: analysis.entities
        };

        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);

        // Create ticket with AI analysis
        setTimeout(async () => {
          const ticketResult = await createTicketWithAI(currentInput);
          
          if (ticketResult && ticketResult.ticket) {
            // Add ticket creation confirmation message
            const ticketMessage: Message = {
              id: (Date.now() + 2).toString(),
              content: `✅ Your ticket has been created successfully! Our team will review your issue and get back to you soon.`,
              isBot: true,
              timestamp: new Date(),
              ticketCreated: true,
              ticketId: ticketResult.ticket.id,
              ticketToken: ticketResult.ticket.token
            };

            setMessages(prev => [...prev, ticketMessage]);
            
            toast({
              title: "Ticket Created Successfully",
              description: `Ticket ${ticketResult.ticket.token} has been created with AI analysis!`,
            });

            onComplaintGenerated?.(ticketResult);
          } else {
            // Add error message
            const errorMessage: Message = {
              id: (Date.now() + 2).toString(),
              content: "I apologize, but I encountered an issue creating your ticket. Please try again or contact support directly.",
              isBot: true,
              timestamp: new Date(),
            };

            setMessages(prev => [...prev, errorMessage]);
            
            toast({
              title: "Error",
              description: "Failed to create ticket. Please try again.",
              variant: "destructive",
            });
          }
          setIsProcessing(false);
        }, 1000);
      } else {
        // Fallback response
        const fallbackResponse = "I understand your concern. Let me create a ticket for our team to review and address your issue.";
        
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: fallbackResponse,
          isBot: true,
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);
        setIsProcessing(false);
      }
    } catch (error) {
      console.error('Error processing message:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I apologize, but I'm experiencing some technical difficulties. Please try again or contact support directly.",
        isBot: true,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!shouldRender) return null;

  // Minimized state
  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-50 overflow-hidden">
        <Card className="w-80 shadow-2xl border-2 border-primary/20">
          <CardHeader className="bg-gradient-to-r from-primary to-primary/80 text-primary-foreground p-3 rounded-t-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Brain className="h-4 w-4" />
                <span className="text-sm font-medium">AI Support Assistant</span>
              </div>
              <div className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={toggleMinimize}
                  className="text-primary-foreground hover:bg-primary-foreground/20 h-6 w-6 p-0"
                >
                  <ChevronUp className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleClose}
                  className="text-primary-foreground hover:bg-primary-foreground/20 h-6 w-6 p-0"
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            </div>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <TooltipProvider>
      <div
        className={cn(
          "fixed bottom-4 right-4 z-50 transition-all duration-300 ease-in-out max-w-[90vw] max-h-[90vh]",
          isOpen ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"
        )}
      >
        <Card className={cn(
          "shadow-2xl border-2 border-primary/20 transition-all duration-300 overflow-hidden",
          isMaximized ? "w-[700px] h-[800px]" : "w-96 h-[600px]"
        )}>
          <CardHeader className="bg-gradient-to-r from-primary via-primary/90 to-primary/80 text-primary-foreground p-4 rounded-t-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Brain className="h-6 w-6 animate-pulse" />
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
                </div>
                <div>
                  <CardTitle className="text-lg">AI Support Assistant</CardTitle>
                  <p className="text-xs text-primary-foreground/80">Powered by Machine Learning</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={toggleMinimize}
                      className="text-primary-foreground hover:bg-primary-foreground/20"
                    >
                      <ChevronDown className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Minimize</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={toggleMaximize}
                      className="text-primary-foreground hover:bg-primary-foreground/20"
                    >
                      {isMaximized ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>{isMaximized ? "Minimize" : "Maximize"}</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleClose}
                      className="text-primary-foreground hover:bg-primary-foreground/20"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Close</TooltipContent>
                </Tooltip>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="flex-1 flex flex-col p-4 overflow-hidden">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 chat-scrollbar" style={{ maxHeight: 'calc(100vh - 300px)' }}>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isBot ? "justify-start" : "justify-end"}`}
                >
                                     <div
                     className={cn(
                       "max-w-[85%] rounded-2xl p-4 transition-all duration-200 break-words",
                       message.isBot
                         ? "bg-gradient-to-br from-muted to-muted/80 text-muted-foreground shadow-md"
                         : "bg-gradient-to-br from-primary to-primary/90 text-primary-foreground shadow-lg"
                     )}
                   >
                    <div className="flex items-start gap-3">
                      {message.isBot && (
                        <div className="relative">
                          <Bot className="h-5 w-5 mt-0.5 flex-shrink-0" />
                          <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        </div>
                      )}
                      <div className="flex-1 space-y-3 min-w-0">
                        <span className="text-sm leading-relaxed break-words">{message.content}</span>
                        
                                                 {/* Show AI analysis if available */}
                         {message.analysis && (
                           <div className="space-y-2 p-3 bg-background/50 rounded-lg border border-border/50 break-words">
                            <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
                              <Zap className="h-3 w-3 text-yellow-500" />
                              AI Analysis
                            </div>
                            <div className="flex flex-wrap items-center gap-2">
                              <Badge variant="outline" className="text-xs bg-blue-50 border-blue-200 text-blue-700">
                                {message.analysis.category} ({Math.round(message.analysis.category_confidence * 100)}%)
                              </Badge>
                              <Badge 
                                variant={message.analysis.priority === 'urgent' ? 'destructive' : 
                                       message.analysis.priority === 'high' ? 'default' : 'secondary'} 
                                className="text-xs"
                              >
                                {message.analysis.priority}
                              </Badge>
                            </div>
                            {message.analysis.keywords && message.analysis.keywords.length > 0 && (
                              <div className="flex flex-wrap gap-1">
                                {message.analysis.keywords.slice(0, 4).map((keyword: string, index: number) => (
                                  <Badge key={index} variant="outline" className="text-xs bg-gray-50">
                                    #{keyword}
                                  </Badge>
                                ))}
                              </div>
                            )}
                          </div>
                        )}

                                                 {/* Show ticket creation status */}
                         {message.ticketCreated && message.ticketToken && (
                           <Alert className="border-green-200 bg-green-50/80 break-words">
                            <div className="flex items-start gap-3">
                              <CheckCircle className="h-4 w-4 text-green-600 mt-0.5" />
                              <div className="flex-1">
                                <AlertDescription className="text-green-800 text-sm font-medium mb-2">
                                  Ticket Created Successfully!
                                </AlertDescription>
                                                                 <div className="flex items-center gap-2 flex-wrap">
                                   <div className="flex items-center gap-2 bg-white px-3 py-1 rounded-md border border-green-200 max-w-full">
                                     <Ticket className="h-3 w-3 text-green-600 flex-shrink-0" />
                                     <span className="text-xs font-mono font-medium text-green-700 break-all">
                                       {message.ticketToken}
                                     </span>
                                   </div>
                                  <Tooltip>
                                    <TooltipTrigger asChild>
                                      <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => copyToClipboard(message.ticketToken!)}
                                        className="h-6 w-6 p-0 hover:bg-green-100"
                                      >
                                        {copiedToken === message.ticketToken ? (
                                          <CheckCircle className="h-3 w-3 text-green-600" />
                                        ) : (
                                          <Copy className="h-3 w-3 text-green-600" />
                                        )}
                                      </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                      {copiedToken === message.ticketToken ? "Copied!" : "Copy token"}
                                    </TooltipContent>
                                  </Tooltip>
                                </div>
                                <p className="text-xs text-green-600 mt-2">
                                  Use this token to track your ticket in the dashboard
                                </p>
                              </div>
                            </div>
                          </Alert>
                        )}
                      </div>
                      {!message.isBot && (
                        <div className="relative">
                          <User className="h-5 w-5 mt-0.5 flex-shrink-0" />
                          <div className="absolute -top-1 -right-1 w-2 h-2 bg-blue-400 rounded-full"></div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gradient-to-br from-muted to-muted/80 text-muted-foreground rounded-2xl p-4 max-w-[85%] shadow-md">
                    <div className="flex items-center gap-3">
                      <div className="relative">
                        <Bot className="h-5 w-5" />
                        <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                      </div>
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:0.1s]"></div>
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:0.2s]"></div>
                      </div>
                      <span className="text-xs text-muted-foreground/70">AI is analyzing...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            
                         <div className="relative">
               <div className="relative">
                 <Input
                   value={inputValue}
                   onChange={(e) => setInputValue(e.target.value)}
                   onKeyPress={handleKeyPress}
                   placeholder="Describe your issue... (AI will analyze and categorize automatically)"
                   className="w-full rounded-full pr-12 py-3 border-2 focus:border-primary transition-all duration-200 break-words"
                   disabled={isProcessing}
                 />
                <Button 
                  onClick={handleSendMessage} 
                  size="icon" 
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 w-8 h-8 rounded-full shadow-lg"
                  disabled={isProcessing || !inputValue.trim()}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
                <span>Press Enter to send</span>
                <span className="flex items-center gap-1">
                  <MessageCircle className="h-3 w-3" />
                  {messages.length - 1} messages
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </TooltipProvider>
  );
}