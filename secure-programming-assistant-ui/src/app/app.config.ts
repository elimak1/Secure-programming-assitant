import { ApplicationConfig } from '@angular/core'
import { provideRouter } from '@angular/router'

import { routes } from './app.routes'
import { provideClientHydration } from '@angular/platform-browser'
import { provideHttpClient, withInterceptors } from '@angular/common/http'
import { authHttpInterceptorFn, provideAuth0 } from '@auth0/auth0-angular'
import { environment } from '../environment/environment'

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideClientHydration(),
    provideHttpClient(withInterceptors([authHttpInterceptorFn])),
    provideAuth0({
      ...environment.auth,
      httpInterceptor: {
        ...environment.httpInterceptor
      }
    })
  ]
}
