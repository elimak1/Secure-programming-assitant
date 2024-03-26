import { Component } from '@angular/core'
import { AuthService } from '@auth0/auth0-angular'
import { HttpService } from '../services/http.service'
import { CommonModule } from '@angular/common'
import { Chat, parsedChatMessage } from '../../models/types'
import { FormsModule } from '@angular/forms'

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  public isLoggedIn: boolean = false

  public currentChatMessages: parsedChatMessage[] = []
  private currentChatId: string | undefined = undefined
  public oldChats: Chat[] = []
  public currentMessage: string = ''

  constructor(
    private authService: AuthService,
    private httpService: HttpService
  ) {}

  ngOnInit() {
    this.authService.user$.subscribe((user) => {
      if (user) {
        this.isLoggedIn = true
      }
    })
    this.httpService.getChats().subscribe((chats) => {
      this.oldChats = chats
    })
  }

  sendMessage() {
    this.currentChatMessages.push({
      sender: 'User',
      message: this.currentMessage
    })
    this.httpService
      .postPrompt(this.currentMessage, this.currentChatId)
      .subscribe((res) => {
        this.currentMessage = ''
        this.currentChatMessages.push({
          sender: 'Kev',
          message: res.response
        })
        this.currentChatId = res.chatId
      })
  }

  parseChatMessages(chatMessages: string[]): parsedChatMessage[] {
    return []
  }
}
