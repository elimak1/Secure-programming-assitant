import moment from "moment"

export interface User {
  username: string
}

export interface Message {
  chatId: string
  text: string
  created_at: moment.Moment
  from_entity: string
}
