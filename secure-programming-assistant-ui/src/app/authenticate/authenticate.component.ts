import { Component, Input } from '@angular/core'
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from '@angular/forms'
import { NewUser } from '../../models/types'
import { CommonModule } from '@angular/common'
import { AuthService } from '../services/auth.service'
import { Router, RouterModule } from '@angular/router'

@Component({
  selector: 'app-authenticate',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './authenticate.component.html',
  styleUrl: './authenticate.component.scss'
})
export class AuthenticateComponent {
  @Input() public isRegister = false

  public registerForm = new FormGroup({
    username: new FormControl('', [
      Validators.required,
      Validators.minLength(3)
    ]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8)
    ]),
    confirmPassword: new FormControl('', [
      Validators.required,
      Validators.minLength(8)
    ])
  })

  public loginForm = new FormGroup({
    username: new FormControl('', [
      Validators.required,
      Validators.minLength(3)
    ]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8)
    ])
  })

  public errorMessage = ''
  public isLoading = false

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {}

  onRegister() {
    if (!this.validateConfirmPassword()) {
      this.errorMessage = 'Passwords do not match'
      return
    }
    this.errorMessage = ''
    this.isLoading = true
    this.authService
      .register(this.registerForm.value as NewUser)
      .subscribe((user) => {
        this.isLoading = false
        if (user) {
          this.errorMessage = ''
          this.redirectToHome()
        } else {
          this.errorMessage = 'Username or email already exists'
        }
      })
  }

  validateConfirmPassword(): boolean {
    const password = this.registerForm.get('password')?.value
    const confirmPassword = this.registerForm.get('confirmPassword')?.value
    return !!password && password === confirmPassword
  }

  onLogin() {
    this.errorMessage = ''
    this.isLoading = true
    this.authService
      .login(this.loginForm.value as { username: string; password: string })
      .subscribe((user) => {
        this.isLoading = false
        if (user) {
          this.errorMessage = ''
          this.redirectToHome()
        } else {
          this.errorMessage = 'Invalid username or password'
        }
      })
  }

  toggleForm() {
    this.isRegister = !this.isRegister
    this.errorMessage = ''
  }

  private redirectToHome() {
    this.router.navigate(['/'])
  }

  get username() {
    return this.isRegister
      ? this.registerForm.get('username')
      : this.loginForm.get('username')
  }

  get email() {
    return this.registerForm.get('email')
  }

  get password() {
    return this.isRegister
      ? this.registerForm.get('password')
      : this.loginForm.get('password')
  }

  get confirmPassword() {
    return this.registerForm.get('confirmPassword')
  }
}
