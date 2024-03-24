import { Component } from '@angular/core'
import { CommonModule } from '@angular/common'
import { AuthService } from '@auth0/auth0-angular'
import { Router } from '@angular/router'
import { HttpService } from '../http.service'
import { environment } from '../../environment/environment'

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
    private httpService: HttpService
  ) {}

  ngOnInit() {
    this.authService.user$.subscribe((user) => {
      if (user) this.username = user['name']
    })
  }

  login() {
    console.log(environment.auth)
    this.authService.loginWithRedirect()
  }

  logout() {
    this.authService.logout()
  }

  test() {
    this.httpService.test().subscribe((res) => {
      console.log(res)
    })
  }
}
