const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function streamChat(messages: { role: string; content: string }[], useRag = true) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages, use_rag: useRag }),
  })

  if (!response.ok) {
    throw new Error('Chat request failed')
  }

  return response.body
}

export async function checkHealth() {
  const response = await fetch(`${API_URL}/api/health`)
  return response.json()
}

export async function uploadDocument(file: File) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_URL}/api/documents`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Upload failed')
  }

  return response.json()
}

export async function getDocuments() {
  const response = await fetch(`${API_URL}/api/documents`)
  return response.json()
}

export async function deleteDocument(id: string) {
  const response = await fetch(`${API_URL}/api/documents/${id}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error('Delete failed')
  }

  return response.json()
}

export async function createThread(title?: string) {
  const response = await fetch(`${API_URL}/api/threads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })
  return response.json()
}

export async function getThreads() {
  const response = await fetch(`${API_URL}/api/threads`)
  return response.json()
}

export async function getThreadMessages(threadId: string) {
  const response = await fetch(`${API_URL}/api/threads/${threadId}/messages`)
  return response.json()
}
