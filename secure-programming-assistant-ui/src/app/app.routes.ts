import { Routes } from '@angular/router'
import { DashboardComponent } from './dashboard/dashboard.component'
import { AuthGuard } from '@auth0/auth0-angular'
import { ChatsComponent } from './chats/chats.component'

export const routes: Routes = [
  { path: 'chats', component: ChatsComponent, canActivate: [AuthGuard] },
  { path: '**', component: DashboardComponent }
]
