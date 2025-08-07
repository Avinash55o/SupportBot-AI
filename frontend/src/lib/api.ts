const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  priority: 'low' | 'normal' | 'high' | 'urgent';
  user_id: number;
  created_at: string;
  updated_at: string;
  assigned_to?: number;
  notes?: string;
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
    const url = `${this.baseURL}${endpoint}`;
    
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
      const data = await response.json();

      if (!response.ok) {
        return { error: data.error || 'An error occurred' };
      }

      return { data };
    } catch (error) {
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

  // User ticket endpoints
  async getUserTickets(userId: number): Promise<ApiResponse<{ tickets: Ticket[] }>> {
    return this.request<{ tickets: Ticket[] }>(`/user/tickets?user_id=${userId}`);
  }

  async getTicket(ticketId: number, userId: number): Promise<ApiResponse<Ticket>> {
    return this.request<Ticket>(`/user/tickets/${ticketId}?user_id=${userId}`);
  }

  // Admin endpoints
  async getAllTickets(params?: {
    status?: string;
    priority?: string;
    page?: number;
    per_page?: number;
  }): Promise<ApiResponse<{ tickets: Ticket[]; total: number; page: number; per_page: number }>> {
    const searchParams = new URLSearchParams();
    if (params?.status) searchParams.append('status', params.status);
    if (params?.priority) searchParams.append('priority', params.priority);
    if (params?.page) searchParams.append('page', params.page.toString());
    if (params?.per_page) searchParams.append('per_page', params.per_page.toString());

    const queryString = searchParams.toString();
    return this.request<{ tickets: Ticket[]; total: number; page: number; per_page: number }>(
      `/admin/tickets${queryString ? `?${queryString}` : ''}`
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
}

export const apiService = new ApiService();
