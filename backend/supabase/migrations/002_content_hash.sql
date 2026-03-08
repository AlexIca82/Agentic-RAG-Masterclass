-- Add content_hash column to documents
ALTER TABLE documents ADD COLUMN IF NOT EXISTS content_hash TEXT;

-- Create index for faster hash lookups
CREATE INDEX IF NOT EXISTS idx_documents_content_hash ON documents(content_hash);

-- Create unique constraint for user_id + content_hash combination
CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_user_hash ON documents(user_id, content_hash);
