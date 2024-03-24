const apiUri = 'http://127.0.0.1:5000'

export const environment = {
  production: false,
  apiUri,
  auth: {
    domain: 'dev-1s63jkyhuhdslcn0.us.auth0.com',
    clientId: 'OTOHMlIIPMBfdwOIgHEMXBZNM4Sx6oCt',
    authorizationParams: {
      redirect_uri: window.location.origin,
      audience: 'https://dev-1s63jkyhuhdslcn0.us.auth0.com/api/v2/'
    }
  },
  httpInterceptor: {
    allowedList: [
      {
        uri: apiUri + '/*',
        tokenOptions: {
          authorizationParams: {}
        }
      }
    ]
  }
}
