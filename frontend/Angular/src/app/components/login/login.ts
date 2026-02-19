import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Importante para el formulario
import { Router } from '@angular/router';
import { Auth } from '../../core/services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule], // Importamos FormsModule aquí
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  credentials = { username: '', password: '' };
  errorMessage: string = '';
  isLoading: boolean = false;

  constructor(private authService: Auth, private router: Router) {}

  onLogin() {
    this.isLoading = true;
    this.authService.login(this.credentials).subscribe({
      next: (response: { access_token: string; role: string; }) => {
        // Guardamos el token y rol (esto lo ideal es que lo haga el servicio)
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('role', response.role);
        
        this.router.navigate(['/dashboard']);
      },
      error: () => {
        this.errorMessage = 'Credenciales inválidas o error de servidor';
        this.isLoading = false;
      }
    });
  }
}