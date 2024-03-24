const apiUri = 'http://127.0.0.1:5000'

export const environment = {
  production: false,
  apiUri,
  auth: {
    domain: 'dev-1s63jkyhuhdslcn0.us.auth0.com',
    clientId: 'OTOHMlIIPMBfdwOIgHEMXBZNM4Sx6oCt',
    authorizationParams: {
      redirect_uri: window.location.origin
    }
  },
  httpInterceptor: {
    allowedList: [`${apiUri}/*`]
  }
}
