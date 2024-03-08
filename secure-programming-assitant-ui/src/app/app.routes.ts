import { Routes } from '@angular/router';
import { AuthenticateComponent } from './authenticate/authenticate.component';
import { DashboardComponent } from './dashboard/dashboard.component';

export const routes: Routes = [
    {
        path: 'authenticate',
        component: AuthenticateComponent
    },
    { path: '**', component: DashboardComponent}
];
