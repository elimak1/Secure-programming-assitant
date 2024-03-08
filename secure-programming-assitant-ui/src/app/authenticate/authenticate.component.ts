import { Component } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { NewUser } from '../../models/types';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-authenticate',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule],
  templateUrl: './authenticate.component.html',
  styleUrl: './authenticate.component.scss'
})
export class AuthenticateComponent {

  public registerForm = new FormGroup({
    username: new FormControl('',
      [Validators.required, Validators.minLength(3)]),
    email: new FormControl('',
      [Validators.required, Validators.email]),
    password: new FormControl('',
      [Validators.required, Validators.minLength(8)]),
    confirmPassword: new FormControl('',
      [Validators.required, Validators.minLength(8)])
  });

  public errorMessage = "";

  constructor() {
  }

  ngOnInit(){
  }

  onRegister() {
    if (!this.validateConfirmPassword()){
      this.errorMessage = "Passwords do not match";
      return
    }
    this.errorMessage = "";
    console.log(this.registerForm.value);
  }

  validateConfirmPassword(): boolean {
    const password = this.registerForm.get('password')?.value;
    const confirmPassword = this.registerForm.get('confirmPassword')?.value;
    return !!password && password === confirmPassword;
  }

  get username() {
    return this.registerForm.get('username');
  }

  get email() {
    return this.registerForm.get('email');
  }

  get password() {
    return this.registerForm.get('password');
  }

  get confirmPassword() {
    return this.registerForm.get('confirmPassword');
  }
}
