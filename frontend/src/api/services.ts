import api from './client';
import type { User, Token, Tag, TagList, Link, LinkList } from '../types';

export const authApi = {
  register: async (username: string, email: string, password: string): Promise<User> => {
    const { data } = await api.post<User>('/auth/register', { username, email, password });
    return data;
  },

  login: async (username: string, password: string): Promise<Token> => {
    const { data } = await api.post<Token>('/auth/login', { username, password });
    return data;
  },

  getMe: async (): Promise<User> => {
    const { data } = await api.get<User>('/auth/me');
    return data;
  },

  refreshToken: async (): Promise<Token> => {
    const { data } = await api.post<Token>('/auth/refresh');
    return data;
  },
};

export const tagsApi = {
  getAll: async (skip = 0, limit = 100): Promise<TagList> => {
    const { data } = await api.get<TagList>('/tags', { params: { skip, limit } });
    return data;
  },

  create: async (name: string, color: string): Promise<Tag> => {
    const { data } = await api.post<Tag>('/tags', { name, color });
    return data;
  },

  update: async (id: number, name: string, color: string): Promise<Tag> => {
    const { data } = await api.put<Tag>(`/tags/${id}`, { name, color });
    return data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/tags/${id}`);
  },
};

export const linksApi = {
  getAll: async (skip = 0, limit = 100): Promise<LinkList> => {
    const { data } = await api.get<LinkList>('/links', { params: { skip, limit } });
    return data;
  },

  getById: async (id: number): Promise<Link> => {
    const { data } = await api.get<Link>(`/links/${id}`);
    return data;
  },

  create: async (url: string, title?: string, description?: string, tagIds: number[] = []): Promise<Link> => {
    const { data } = await api.post<Link>('/links', { url, title, description, tag_ids: tagIds });
    return data;
  },

  update: async (id: number, data: Partial<{ url: string; title: string; description: string; tag_ids: number[] }>): Promise<Link> => {
    const { data: result } = await api.put<Link>(`/links/${id}`, data);
    return result;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/links/${id}`);
  },

  searchByTags: async (tags: string, skip = 0, limit = 100): Promise<LinkList> => {
    const { data } = await api.get<LinkList>('/links/search/tags', { params: { tags, skip, limit } });
    return data;
  },

  searchByQuery: async (q: string, skip = 0, limit = 100): Promise<LinkList> => {
    const { data } = await api.get<LinkList>('/links/search/query', { params: { q, skip, limit } });
    return data;
  },
};
