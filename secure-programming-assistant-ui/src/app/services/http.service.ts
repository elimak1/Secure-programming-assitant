import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environment/environment'
import { Observable, map } from 'rxjs'
import { Chat, PromptResponse } from '../../models/types'

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private httpClient: HttpClient) {}

  test(): Observable<string> {
    return this.httpClient.get<string>(`${environment.apiUri}/auth/user`)
  }

  getChats(): Observable<Chat[]> {
    return this.httpClient.get<Chat[]>(`${environment.apiUri}/chats`).pipe(
      map((chats: Chat[]) => {
        return chats.map((chat: Chat) => {
          chat.created_at = new Date(chat.created_at)
          return chat
        })
      })
    )
  }

  postPrompt(
    prompt: string,
    chatId: string | undefined
  ): Observable<PromptResponse> {
    return this.httpClient.post<PromptResponse>(`${environment.apiUri}/chat`, {
      prompt,
      ...(chatId ? { chatId } : {})
    })
  }

  getChat(chatId: string): Observable<Chat> {
    return this.httpClient
      .get<Chat>(`${environment.apiUri}/chat/${chatId}`)
      .pipe(
        map((chat: Chat) => {
          chat.created_at = new Date(chat.created_at)
          return chat
        })
      )
  }
  deleteChat(chatId: string): Observable<void> {
    return this.httpClient.delete<void>(`${environment.apiUri}/chat/${chatId}`)
  }
}
