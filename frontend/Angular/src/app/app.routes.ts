import { Routes } from '@angular/router';
import { Login } from './components/login/login';
import { Dashboard } from './components/dashboard/dashboard';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  { path: 'login', component: Login },
  { 
    path: 'dashboard', 
    component: Dashboard, 
    canActivate: [authGuard] // Aquí se aplica la protección
  },
  { path: '', redirectTo: '/login', pathMatch: 'full' }, // Redirigir raíz al login
  { path: '**', redirectTo: '/login' } // Por si escriben cualquier cosa
];