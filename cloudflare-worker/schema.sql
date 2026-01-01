-- D1 Database Schema for AZ-104 Study Hub
-- Run this with: wrangler d1 execute az104-study-db --file=schema.sql

CREATE TABLE IF NOT EXISTS user_scores (
  user_id TEXT PRIMARY KEY,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_scores_updated ON user_scores(updated_at);
