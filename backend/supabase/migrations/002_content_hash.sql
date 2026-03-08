-- Add content_hash column to documents
ALTER TABLE documents ADD COLUMN IF NOT EXISTS content_hash TEXT;

-- Create index for faster hash lookups
CREATE INDEX IF NOT EXISTS idx_documents_content_hash ON documents(content_hash);

-- Drop existing unique index if it exists
DROP INDEX IF EXISTS idx_documents_user_hash;

-- Create unique constraint for user_id + content_hash combination
CREATE UNIQUE INDEX idx_documents_user_hash ON documents(user_id, content_hash) WHERE content_hash IS NOT NULL;
