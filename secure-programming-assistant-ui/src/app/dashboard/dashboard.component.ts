import { Component } from '@angular/core'
import { AuthService } from '@auth0/auth0-angular'
import { HttpService } from '../services/http.service'
import { CommonModule } from '@angular/common'
import { Message } from '../../models/types'
import { FormsModule } from '@angular/forms'
import moment from 'moment'
import { SpinnerComponent } from '../spinner/spinner.component'
import { FormatMessageComponent } from '../format-message/format-message.component'

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    SpinnerComponent,
    FormatMessageComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  public isLoggedIn: boolean = false

  public currentChatMessages: Message[] = []
  private currentChatId: string | undefined = undefined
  public currentMessage: string = ''

  public isLoading = false

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

    const queryParams = new URLSearchParams(window.location.search)
    const chatId = queryParams.get('chatId')
    if (chatId) {
      this.currentChatId = chatId
      this.isLoading = true
      this.httpService.getChat(chatId).subscribe((chats) => {
        this.currentChatMessages = chats
        this.isLoading = false
        this.scrollToBottom()
      })
    }
  }

  sendMessage() {
    this.currentChatMessages.push({
      from_entity: 'User',
      text: this.currentMessage,
      created_at: moment(),
      chatId: this.currentChatId ?? ''
    })
    this.scrollToBottom()
    this.isLoading = true
    const prompt = this.currentMessage
    this.currentMessage = ''
    this.httpService.postPrompt(prompt, this.currentChatId).subscribe((res) => {
      this.isLoading = false
      this.currentChatMessages.push(res)
      this.currentChatId = res.chatId
      this.scrollToBottom()
    })
  }

  scrollToBottom(): void {
    setTimeout(() => {
      window.scrollTo(0, document.body.scrollHeight)
    }, 50)
  }
}
