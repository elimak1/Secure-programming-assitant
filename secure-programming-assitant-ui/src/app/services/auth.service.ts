import { Injectable } from '@angular/core';
import { User } from '../../models/types';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _user = new BehaviorSubject<User|undefined>(undefined)
  constructor() { 
    //this._user.next({username: 'admin'});
  }


  getLoggedInUser(): Observable<User|undefined>{
    return this._user;
  }
}
