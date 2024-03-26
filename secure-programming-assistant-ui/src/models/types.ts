export interface User {
  username: string
}

export interface NewUser extends User {
  password: string
  confirmPassword: string
  email: string
}

export interface Chat {
  id: string
  text: string
  created_at: Date
}

export interface parsedChatMessage {
  sender: string
  message: string
}

export interface PromptResponse {
  response: string
  prompt: string
  chatId: string
}
