import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);

  // Usamos Signals para reactividad automática
  allData = signal<any[]>([]);
  loading = signal<boolean>(true);
  
  userRole = localStorage.getItem('user_role') || '';
  username = localStorage.getItem('username') || '';

  // Esta señal se actualiza SOLA cuando 'allData' cambia
  filteredData = computed(() => {
    const data = this.allData();
    const role = this.userRole;
    const name = this.username.toLowerCase().trim();

    if (role === 'admin') return data;
    if (role === 'supervisor') return data.filter(item => item.rol !== 'admin');
    
    return data.filter(item => item.nombre?.toLowerCase().trim() === name);
  });

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    const url = 'https://prueba-tecnica-clerc-carvajal.onrender.com/auth/data';
    
    this.http.get<any[]>(url, { withCredentials: true })
      .subscribe({
        next: (data) => {
          this.allData.set(data || []);
          this.loading.set(false);
        },
        error: (err) => {
          console.error('Error:', err);
          this.loading.set(false);
        }
      });
  }

  logout() {
    this.http.post('https://prueba-tecnica-clerc-carvajal.onrender.com/auth/logout', {}, { withCredentials: true })
      .subscribe({
        next: () => this.clearAndRedirect(),
        error: () => this.clearAndRedirect()
      });
  }

  private clearAndRedirect() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}