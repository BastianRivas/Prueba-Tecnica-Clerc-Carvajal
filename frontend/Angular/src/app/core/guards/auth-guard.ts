import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token'); // Verificamos si hay token

  if (token) {
    return true; // Permite el paso
  } else {
    router.navigate(['/login']); // Redirige si no está logueado
    return false;
  }
};