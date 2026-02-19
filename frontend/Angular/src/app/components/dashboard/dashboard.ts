import { Component, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common'; // Agregamos CurrencyPipe para la renta
import { Auth } from '../../core/services/auth';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard implements OnInit {
  filteredData: any[] = [];
  userRole: string | null = '';
  username: string | null = '';

  constructor(private authService: Auth, private http: HttpClient) {}

  ngOnInit() {
    this.userRole = this.authService.getRole();
    this.username = localStorage.getItem('username'); // Nombre con el que hizo login
    this.loadData();
  }

  loadData() {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    this.http.get<any[]>('https://prueba-tecnica-clerc-carvajal.onrender.com/auth/data', { 
    withCredentials: true 
    }).subscribe({
      next: (allData) => {
        // Aplicamos el filtro defensivo que mencionaste
        this.applyPermissions(allData);
      },
      error: (err) => {
        console.error('Error cargando datos', err);
        if (err.status === 401) this.authService.logout();
      }
    });
  }
  //Aqui por si acaso se vuelve a validar por si acaso el backend se equivoca, aunque no debería pasar.
  applyPermissions(allData: any[]) {
    if (this.userRole === 'admin') {
      this.filteredData = allData;
    } 
    else if (this.userRole === 'supervisor') {
      // Por si el backend se equivoca, filtramos admins
      this.filteredData = allData.filter(item => item.rol !== 'admin');
    } 
    else {
      // Solo su propio registro
      this.filteredData = allData.filter(item => item.nombre === this.username);
    }
  }
}