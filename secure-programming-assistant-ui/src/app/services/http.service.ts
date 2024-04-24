import { Injectable } from '@angular/core'
import { HttpClient, HttpErrorResponse } from '@angular/common/http'
import { environment } from '../../environment/environment'
import { Observable, map, catchError, pipe, of } from 'rxjs'
import { Message } from '../../models/types'
import moment from 'moment'
import { AuthService } from '@auth0/auth0-angular'
import { ToastrService } from 'ngx-toastr'
import e from 'express'

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(
    private httpClient: HttpClient,
    private authService: AuthService,
    private toastr: ToastrService
  ) {}

  test(): Observable<string | undefined> {
    return this.httpClient
      .get<string>(`${environment.apiUri}/auth/user`)
      .pipe(catchError(this.handleError.bind(this)))
  }

  getChats(): Observable<Message[] | undefined> {
    return this.httpClient.get<Message[]>(`${environment.apiUri}/chats`).pipe(
      map((chats: Message[]) => {
        return chats.map((chat: Message) => {
          chat.created_at = moment.utc(chat.created_at)
          return chat
        })
      }),
      catchError(this.handleError.bind(this))
    )
  }

  postPrompt(
    prompt: string,
    chatId: string | undefined
  ): Observable<Message | undefined> {
    return this.httpClient
      .post<Message>(`${environment.apiUri}/chat/${chatId ?? ''}`, { prompt })
      .pipe(catchError(this.handleError.bind(this)))
  }

  getChat(chatId: string): Observable<Message[] | undefined> {
    return this.httpClient
      .get<Message[]>(`${environment.apiUri}/chat/${chatId}`)
      .pipe(
        map((chats: Message[]) => {
          return chats.map((chat: Message) => {
            chat.created_at = moment.utc(chat.created_at)
            return chat
          })
        }),
        catchError(this.handleError.bind(this))
      )
  }
  deleteChat(chatId: string): Observable<void> {
    return this.httpClient
      .delete<void>(`${environment.apiUri}/chat/${chatId}`)
      .pipe(catchError(this.handleError.bind(this)))
  }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 401 && error.error.error === 'invalid_token') {
      this.toastr.error('Please login again', 'Session Expired')
      setTimeout(() => {
        this.authService.logout()
      }, 2000)
    } else {
      if (typeof error.error === 'string') {
        this.toastr.error(error.error, 'Error')
      } else {
        this.toastr.error('An error occurred', error.statusText)
      }
    }
    return of(undefined)
  }
}
