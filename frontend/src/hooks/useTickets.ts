import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService, Ticket } from '@/lib/api';

export const useUserTickets = (userId: number) => {
  return useQuery({
    queryKey: ['userTickets', userId],
    queryFn: () => apiService.getUserTickets(userId),
    enabled: !!userId,
  });
};

export const useTicket = (ticketId: number, userId: number) => {
  return useQuery({
    queryKey: ['ticket', ticketId, userId],
    queryFn: () => apiService.getTicket(ticketId, userId),
    enabled: !!ticketId && !!userId,
  });
};

export const useAllTickets = (params?: {
  status?: string;
  priority?: string;
  page?: number;
  per_page?: number;
}) => {
  return useQuery({
    queryKey: ['allTickets', params],
    queryFn: () => apiService.getAllTickets(params),
  });
};

export const useTicketDetails = (ticketId: number) => {
  return useQuery({
    queryKey: ['ticketDetails', ticketId],
    queryFn: () => apiService.getTicketDetails(ticketId),
    enabled: !!ticketId,
  });
};

export const useAnalytics = () => {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: () => apiService.getAnalytics(),
  });
};

export const useAssignTicket = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ ticketId, adminId }: { ticketId: number; adminId: number }) =>
      apiService.assignTicket(ticketId, adminId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['allTickets'] });
      queryClient.invalidateQueries({ queryKey: ['ticketDetails'] });
    },
  });
};

export const useUpdateTicketStatus = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ 
      ticketId, 
      status, 
      notes 
    }: { 
      ticketId: number; 
      status: string; 
      notes?: string;
    }) => apiService.updateTicketStatus(ticketId, status, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['allTickets'] });
      queryClient.invalidateQueries({ queryKey: ['ticketDetails'] });
      queryClient.invalidateQueries({ queryKey: ['userTickets'] });
    },
  });
};

export const useUpdateTicketPriority = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ 
      ticketId, 
      priority 
    }: { 
      ticketId: number; 
      priority: string;
    }) => apiService.updateTicketPriority(ticketId, priority),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['allTickets'] });
      queryClient.invalidateQueries({ queryKey: ['ticketDetails'] });
    },
  });
};
