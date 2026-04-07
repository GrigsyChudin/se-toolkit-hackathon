export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Tag {
  id: number;
  name: string;
  color: string;
  created_at: string;
}

export interface Link {
  id: number;
  url: string;
  title: string | null;
  description: string | null;
  user_id: number;
  tags: Tag[];
  created_at: string;
  updated_at: string;
}

export interface TagList {
  tags: Tag[];
  total: number;
}

export interface LinkList {
  links: Link[];
  total: number;
}

export interface ApiError {
  code: string;
  message: string;
  details: Record<string, unknown>;
}
