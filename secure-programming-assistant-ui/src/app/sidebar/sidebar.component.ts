import { Component } from '@angular/core'
import { CommonModule } from '@angular/common'
import { AuthService } from '@auth0/auth0-angular'
import { HttpService } from '../services/http.service'
import { Router } from '@angular/router'

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  public username: string | undefined
  constructor(
    private authService: AuthService,
    private httpService: HttpService,
    private router: Router
  ) {}

  ngOnInit() {
    this.authService.user$.subscribe((user) => {
      if (user) this.username = user['name']
    })
  }

  login() {
    this.authService.loginWithRedirect()
  }

  logout() {
    this.authService.logout()
  }

  navigate(route: string) {
    this.router.navigate([route])
  }
}
