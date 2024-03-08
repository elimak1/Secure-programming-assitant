import { Injectable } from '@angular/core';
import { User } from '../../models/types';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _user: User | undefined;
  constructor() { }


  getLoggedInUser() {
    return this._user;
  }
}
