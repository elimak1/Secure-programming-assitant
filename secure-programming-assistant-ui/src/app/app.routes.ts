import { Routes } from '@angular/router'
import { AuthenticateComponent } from './authenticate/authenticate.component'
import { DashboardComponent } from './dashboard/dashboard.component'
import { AuthGuard } from '@auth0/auth0-angular'

export const routes: Routes = [
  {
    path: 'authenticate',
    component: AuthenticateComponent
  },
  { path: '**', component: DashboardComponent }
]
