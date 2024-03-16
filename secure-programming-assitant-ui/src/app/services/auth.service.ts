import { Injectable } from '@angular/core';
import { NewUser, User } from '../../models/types';
import { BehaviorSubject, Observable, catchError, map } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _user = new BehaviorSubject<User|undefined>(undefined)
  constructor(private httpClient: HttpClient) { 
  }


  getLoggedInUser(): Observable<User|undefined>{
    return this._user;
  }

  register(user: NewUser): Observable<User|undefined>{
    return this.httpClient.post<User|undefined>(`${environment.apiUrl}/auth/register`, user).pipe(
      catchError((err) => {
        return new Observable<User|undefined>((observer) => {
          observer.next(undefined);
        })
      }),
      map((user: User|undefined) => {
        this._user.next(user);
        return user;
      }
    ))
  }

  login(user: {username:string, password:string}): Observable<User|undefined>{
    return this.httpClient.post<User|undefined>(`${environment.apiUrl}/auth/login`, user).pipe(
      catchError((err) => {
        return new Observable<User|undefined>((observer) => {
          observer.next(undefined);
        })
      }),
      map((user: User|undefined) => {
        this._user.next(user);
        return user;
      }
    ))
  }

  logout(): Observable<undefined>{
    return this.httpClient.post<undefined>(`${environment.apiUrl}/auth/logout`, {}).pipe(
      catchError((err) => {
        return new Observable<undefined>((observer) => {
          observer.next(undefined);
        })
      }),
      map(() => {
        this._user.next(undefined);
        return undefined;
      }
    ))
  }
}
