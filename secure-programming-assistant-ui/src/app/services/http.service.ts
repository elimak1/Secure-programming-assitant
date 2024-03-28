import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environment/environment'
import { Observable, map } from 'rxjs'
import { Message } from '../../models/types'
import moment from 'moment'

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private httpClient: HttpClient) {}

  test(): Observable<string> {
    return this.httpClient.get<string>(`${environment.apiUri}/auth/user`)
  }

  getChats(): Observable<Message[]> {
    return this.httpClient.get<Message[]>(`${environment.apiUri}/chats`).pipe(
      map((chats: Message[]) => {
        return chats.map((chat: Message) => {
          chat.created_at = moment.utc(chat.created_at)
          return chat
        })
      })
    )
  }

  postPrompt(
    prompt: string,
    chatId: string | undefined
  ): Observable<Message> {
    return this.httpClient.post<Message>(`${environment.apiUri}/chat/${chatId ?? ''}`, {
      prompt,
    })
  }

  getChat(chatId: string): Observable<Message[]> {
    return this.httpClient
      .get<Message[]>(`${environment.apiUri}/chat/${chatId}`)
      .pipe(
        map((chats: Message[]) => {
          return chats.map((chat: Message) => {
            chat.created_at = moment.utc(chat.created_at)
            return chat
          })
        })
      )
  }
  deleteChat(chatId: string): Observable<void> {
    return this.httpClient.delete<void>(`${environment.apiUri}/chat/${chatId}`)
  }
}
