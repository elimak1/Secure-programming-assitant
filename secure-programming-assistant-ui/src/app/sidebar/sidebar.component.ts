import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {

  public username: string | undefined;
  constructor(private authService: AuthService, private router: Router) {
  }

  ngOnInit(){
    this.authService.getLoggedInUser().subscribe(user => {
      this.username = user?.username;
    });
  }

  login(){
    this.router.navigate(['/authenticate']);
  }

  logout(){
    this.authService.logout().subscribe(() => {
      console.log("Logged out");
    });
  }

  test(){
    this.authService.test().subscribe(() => {
      console.log("Tested");
    });
  }
}
