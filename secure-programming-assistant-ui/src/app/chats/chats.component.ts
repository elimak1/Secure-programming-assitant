import { Component, ViewChild } from '@angular/core'
import { AuthService } from '@auth0/auth0-angular'
import { HttpService } from '../services/http.service'
import { Router } from '@angular/router'
import { Message } from '../../models/types'
import { SpinnerComponent } from '../spinner/spinner.component'
import { CommonModule } from '@angular/common'
import moment from 'moment'
import { FormatMessageComponent } from '../format-message/format-message.component'
import { MatSort, MatSortModule } from '@angular/material/sort'
import { MatTableDataSource, MatTableModule } from '@angular/material/table'

@Component({
  selector: 'app-chats',
  standalone: true,
  imports: [
    SpinnerComponent,
    MatTableModule,
    CommonModule,
    FormatMessageComponent,
    MatSortModule
  ],
  templateUrl: './chats.component.html',
  styleUrl: './chats.component.scss'
})
export class ChatsComponent {
  public isLoading: boolean = true
  public moment = moment

  public dataSource: MatTableDataSource<Message> =
    new MatTableDataSource<Message>([])

  constructor(
    private authService: AuthService,
    private httpService: HttpService,
    private router: Router
  ) {}

  @ViewChild(MatSort, { static: false }) sort?: MatSort

  ngAfterViewInit() {
    console.log(this.sort)
    if (this.sort) {
      this.dataSource.sort = this.sort
    }
  }

  ngOnInit() {
    this.authService.user$.subscribe((user) => {
      if (user) {
        this.httpService.getChats().subscribe((chats) => {
          this.dataSource.data = chats
          this.isLoading = false
        })
      }
    })
  }

  deleteChat(chatId: string, event: MouseEvent) {
    event.stopPropagation()
    this.httpService.deleteChat(chatId).subscribe(() => {
      this.dataSource.data = this.dataSource.data.filter(
        (chat: Message) => chat.chatId !== chatId
      )
    })
  }

  openChat(message: Message) {
    this.router.navigate(['/'], { queryParams: { chatId: message.chatId } })
  }
}
