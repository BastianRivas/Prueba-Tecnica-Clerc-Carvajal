export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string; // O el nombre que use tu API de Litestar
  role: 'admin' | 'supervisor' | 'usuario';
  username: string;
}