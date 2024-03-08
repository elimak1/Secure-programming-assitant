import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {

  public username: string | undefined;
  constructor(private authService: AuthService) {
  }

  ngOnInit(){
    this.authService.getLoggedInUser().subscribe(user => {
      this.username = user?.username;
    });
  }
}
