import { useState, useEffect, createContext, useContext } from 'react';
import { apiService, User, LoginRequest, RegisterRequest } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<{ success: boolean; error?: string }>;
  register: (userData: RegisterRequest) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  adminLogin: (credentials: LoginRequest) => Promise<{ success: boolean; error?: string }>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on app start
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    if (token && userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
      }
    }
    
    setIsLoading(false);
  }, []);

  const login = async (credentials: LoginRequest) => {
    try {
      const response = await apiService.login(credentials);
      
      if (response.error) {
        return { success: false, error: response.error };
      }
      
      if (response.data) {
        const { token, user } = response.data;
        localStorage.setItem('authToken', token);
        localStorage.setItem('userData', JSON.stringify(user));
        setUser(user);
        return { success: true };
      }
      
      return { success: false, error: 'Login failed' };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const register = async (userData: RegisterRequest) => {
    try {
      const response = await apiService.register(userData);
      
      if (response.error) {
        return { success: false, error: response.error };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const adminLogin = async (credentials: LoginRequest) => {
    try {
      const response = await apiService.adminLogin(credentials);
      
      if (response.error) {
        return { success: false, error: response.error };
      }
      
      if (response.data) {
        const { token } = response.data;
        localStorage.setItem('authToken', token);
        localStorage.setItem('isAdmin', 'true');
        return { success: true };
      }
      
      return { success: false, error: 'Admin login failed' };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    localStorage.removeItem('isAdmin');
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    adminLogin,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
