# Secure programming assistant

The application is a secure programming assistant that helps users to create secure applications. Logged in users can chat with the assitant which is using GPT-3.5 and using documents scraped from owasp.org as potential retrieved content to give user's up to date information on secure programming practices.

Main features of the program

- Retrieval augmented Chatbot
- Storing, deleting and continuing conversations
- Rate limiting for non-admin users
- User authentication (user management is handled by auth0 service)
- Slick UI

## Structure of the program

![Architecture](./images/architecture.png)

Available api endpoints:

- GET /chats - load list of all previous conversations of the user, only shows the first message of each conversation
- GET /chats/{chat_id} - load a specific conversation
- POST /chats/ - start a new conversation by sending initial message
- POST /chats/{chat_id} - continue a conversation by sending a new message
- DELETE /chats/{chat_id} - delete a conversation
- GET /ping - check if the server is running

Every route requires a valid access token in the Authorization header. The access token is obtained by logging in with auth0.

Structure of the repository:

- secure-programming-assistant-ui/ - contains the Angular application
- api/db - contains database schema and utility functions
- api/langchain_utils - defines the chatbot, connects to OpenAI API and retrieves relevant documents from vector store
- api/notebooks - has a notebook for creating the vector store
- api/vector_store - optional vector store which is loaded to memory when the application starts
- api/\_\_init\_\_.py - initializes the Flask application
- api/authenticate.py - contains the authentication logic
- api/core.py - contains rate limiting logic
- api/llm.py - contains the endpoints

## Secure programming solutions

- Follows Oauth2.0 protocol.
- Access control is implemented by requiring a valid access token in the Authorization header. The JWT token uses RS256 algorithm for signing and the public key is obtained from auth0. The token is verified in api/authenticate.py. All routes require a valid token except for the /ping route and user data is only accessed using the user_id from the token. In addition the admin role is accessed from the token and used to determine if the user is an admin.
- Allowed CORS origins are set to the frontend domain in the Flask application.
- All login and registration attempts are logged by Auth0.
- Api is rate limited by ip to 4 requestes per second and chat prompt api is further limited to 50 per hour or 100 per day to non admin users. In Auth0 threat protection is prevent access to bots and other malicious actors.
- Server does not store any session identifiers or cookies.

## Setup

## Testing

## Known security issues or vulnerabilities

Email verification is not implemented as it is not available in the auth0 free tier. This means that users can create accounts with fake email addresses. The issue is mitigated by enabling threat detection in auth0 which will block users with suspicious behavior.

## Future improvements
