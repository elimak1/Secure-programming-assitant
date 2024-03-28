DROP TABLE IF EXISTS chat_history;

CREATE TABLE chat_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  from_entity TEXT NOT NULL,
  text TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  message_order INTEGER NOT NULL,
);
