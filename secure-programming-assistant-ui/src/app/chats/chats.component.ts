import { Component } from '@angular/core'
import { AuthService } from '@auth0/auth0-angular'
import { HttpService } from '../services/http.service'
import { Chat } from '../../models/types'
import { SpinnerComponent } from '../spinner/spinner.component'
import { MatTableModule } from '@angular/material/table'
import { CommonModule } from '@angular/common'

@Component({
  selector: 'app-chats',
  standalone: true,
  imports: [SpinnerComponent, MatTableModule, CommonModule],
  templateUrl: './chats.component.html',
  styleUrl: './chats.component.scss'
})
export class ChatsComponent {
  public isLoading: boolean = true
  public oldChats: Chat[] = [
    {
      text: 'Hello',
      created_at: new Date(),
      id: '1'
    }
  ]

  constructor(
    private authService: AuthService,
    private httpService: HttpService
  ) {}

  ngOnInit() {
    this.authService.user$.subscribe((user) => {
      if (user) {
        this.httpService.getChats().subscribe((chats) => {
          this.oldChats = chats
          this.isLoading = false
        })
      }
    })
  }
}
