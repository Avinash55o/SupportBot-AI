const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Ticket {
  id: number;
  token: string;
  title?: string;
  issue_type: string;
  description: string;
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  priority: 'low' | 'normal' | 'high' | 'urgent';
  user_id: number;
  created_at: string;
  updated_at: string;
  assigned_to?: number;
  notes?: string;
}

export interface AIAnalysis {
  category: string;
  category_confidence: number;
  priority: string;
  priority_confidence: number;
  sentiment: {
    sentiment: string;
    score: number;
    subjectivity: number;
  };
  keywords: string[];
  urgency_score: number;
  analysis_timestamp: string;
}

export interface AIInsights {
  total_analyzed: number;
  category_distribution: Record<string, number>;
  priority_distribution: Record<string, number>;
  average_sentiment: number;
  top_categories: [string, number][];
  top_priorities: [string, number][];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = this.baseURL ? `${this.baseURL}${endpoint}` : endpoint;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers = {
        ...config.headers,
        'Authorization': `Bearer ${token}`,
      };
    }

    try {
      const response = await fetch(url, config);
      
      // Check if response is ok before trying to parse JSON
      if (!response.ok) {
        let errorMessage = 'An error occurred';
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || errorMessage;
        } catch {
          // If we can't parse the error response, use the status text
          errorMessage = response.statusText || errorMessage;
        }
        return { error: errorMessage };
      }

      // Try to parse JSON response
      let data;
      try {
        data = await response.json();
      } catch (error) {
        return { error: 'Invalid response format' };
      }

      return { data };
    } catch (error) {
      console.error('Network error:', error);
      // Check if it's a network error (no internet, server down, etc.)
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return { error: 'Network error occurred. Please check your connection and ensure the backend server is running.' };
      }
      return { error: 'Network error occurred' };
    }
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<ApiResponse<{ token: string; user: User }>> {
    return this.request<{ token: string; user: User }>('/user/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async register(userData: RegisterRequest): Promise<ApiResponse<{ user_id: number }>> {
    return this.request<{ user_id: number }>('/user/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async adminLogin(credentials: LoginRequest): Promise<ApiResponse<{ token: string }>> {
    return this.request<{ token: string }>('/admin/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  // Ticket endpoints
  async getUserTickets(userId: number): Promise<ApiResponse<{ tickets: Ticket[] }>> {
    return this.request<{ tickets: Ticket[] }>(`/user/tickets?user_id=${userId}`);
  }

  async getTicket(ticketId: number, userId: number): Promise<ApiResponse<Ticket>> {
    return this.request<Ticket>(`/user/tickets/${ticketId}?user_id=${userId}`);
  }

  async getAllTickets(params?: {
    status?: string;
    priority?: string;
    page?: number;
    per_page?: number;
  }): Promise<ApiResponse<{ tickets: Ticket[]; total: number; page: number; per_page: number }>> {
    const queryParams = new URLSearchParams();
    if (params?.status) queryParams.append('status', params.status);
    if (params?.priority) queryParams.append('priority', params.priority);
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());

    return this.request<{ tickets: Ticket[]; total: number; page: number; per_page: number }>(
      `/admin/tickets?${queryParams.toString()}`
    );
  }

  async createTicket(ticketData: {
    description: string;
    user_id?: number;
  }): Promise<ApiResponse<{ ticket: Ticket; analysis: AIAnalysis; intelligent_response: string; entities: any; similar_tickets: Ticket[] }>> {
    return this.request<{ ticket: Ticket; analysis: AIAnalysis; intelligent_response: string; entities: any; similar_tickets: Ticket[] }>(
      '/api/create-ticket',
      {
        method: 'POST',
        body: JSON.stringify(ticketData),
      }
    );
  }

  async assignTicket(ticketId: number, adminId: number): Promise<ApiResponse<{ ticket: Ticket }>> {
    return this.request<{ ticket: Ticket }>(`/admin/tickets/${ticketId}/assign`, {
      method: 'PUT',
      body: JSON.stringify({ admin_id: adminId }),
    });
  }

  async updateTicketStatus(
    ticketId: number,
    status: string,
    notes?: string
  ): Promise<ApiResponse<{ ticket: Ticket }>> {
    return this.request<{ ticket: Ticket }>(`/admin/tickets/${ticketId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status, notes }),
    });
  }

  async updateTicketPriority(
    ticketId: number,
    priority: string
  ): Promise<ApiResponse<{ ticket: Ticket }>> {
    return this.request<{ ticket: Ticket }>(`/admin/tickets/${ticketId}/priority`, {
      method: 'PUT',
      body: JSON.stringify({ priority }),
    });
  }

  async getTicketDetails(ticketId: number): Promise<ApiResponse<Ticket>> {
    return this.request<Ticket>(`/admin/tickets/${ticketId}`);
  }

  async getAnalytics(): Promise<ApiResponse<any>> {
    return this.request<any>('/admin/analytics');
  }

  // AI/ML endpoints
  async analyzeComplaint(text: string): Promise<ApiResponse<{
    analysis: AIAnalysis;
    intelligent_response: string;
    entities: any;
    similar_tickets: Ticket[];
  }>> {
    return this.request<{
      analysis: AIAnalysis;
      intelligent_response: string;
      entities: any;
      similar_tickets: Ticket[];
    }>('/api/analyze-complaint', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  }

  async suggestTicketAssignment(ticketId: number): Promise<ApiResponse<{
    suggested_admin: User;
    reasoning: string;
    analysis: AIAnalysis;
  }>> {
    return this.request<{
      suggested_admin: User;
      reasoning: string;
      analysis: AIAnalysis;
    }>(`/api/suggest-assignment/${ticketId}`);
  }

  async getSimilarTickets(ticketId: number): Promise<ApiResponse<{ similar_tickets: Ticket[] }>> {
    return this.request<{ similar_tickets: Ticket[] }>(`/api/similar-tickets/${ticketId}`);
  }

  async retrainModels(ticketId: number, actualCategory?: string, actualPriority?: string): Promise<ApiResponse<{
    success: boolean;
    category_accuracy?: number;
    priority_accuracy?: number;
    training_samples?: number;
  }>> {
    return this.request<{
      success: boolean;
      category_accuracy?: number;
      priority_accuracy?: number;
      training_samples?: number;
    }>('/api/retrain-models', {
      method: 'POST',
      body: JSON.stringify({
        ticket_id: ticketId,
        actual_category: actualCategory,
        actual_priority: actualPriority,
      }),
    });
  }

  async getAIInsights(): Promise<ApiResponse<{
    total_tickets: number;
    open_tickets: number;
    in_progress_tickets: number;
    resolved_tickets: number;
    ai_insights: AIInsights;
  }>> {
    return this.request<{
      total_tickets: number;
      open_tickets: number;
      in_progress_tickets: number;
      resolved_tickets: number;
      ai_insights: AIInsights;
    }>('/api/ai-insights');
  }
}

export const apiService = new ApiService();
