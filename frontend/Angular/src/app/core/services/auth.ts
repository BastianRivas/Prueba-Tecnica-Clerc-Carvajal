import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class Auth {
  // URL de tu API en Render
  private readonly API_URL = 'https://prueba-tecnica-clerc-carvajal.onrender.com/auth/login';

  constructor(private http: HttpClient, private router: Router) {}

  // Método para iniciar sesión
  login(credentials: any): Observable<any> {
    return this.http.post<any>(this.API_URL, credentials,{ 
    withCredentials: true
  }).pipe(
      tap(response => {
        if (response.message === 'success') {
          // Guardamos los datos que Litestar nos da
          localStorage.setItem('username', response.nombre); 
          localStorage.setItem('user_role', response.rol);
        }
      })
    );
  }

  // Método para obtener el rol guardado
  getRole(): string | null {
    return localStorage.getItem('user_role');
  }

  // Método para verificar si está autenticado
  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  // Método para cerrar sesión (Logout)
  logout(): void {
    localStorage.clear(); // Limpia token y rol
    this.router.navigate(['/login']);
  }
}