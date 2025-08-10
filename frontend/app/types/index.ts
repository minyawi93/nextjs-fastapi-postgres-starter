export type User = {
  id: number;
  name: string;
  api_key: string;
};

export type Message = {
  id: number;
  content: string;
  is_from_user: boolean;
  created_at: string;
};

export type Thread = {
  id: number;
  messages: Message[];
};

export type ApiResponse<T> = {
  data?: T;
  error?: string;
};
