import { supabase } from './supabase'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function getAuthHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`
  }
  return headers
}

export async function streamChat(messages: { role: string; content: string }[], useRag = true) {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers,
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
  const { data: { session } } = await supabase.auth.getSession()
  const formData = new FormData()
  formData.append('file', file)

  const headers: Record<string, string> = {}
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`
  }

  const response = await fetch(`${API_URL}/api/documents`, {
    method: 'POST',
    headers,
    body: formData,
  })

  if (!response.ok) {
    const error = await response.text()
    throw new Error(error || 'Upload failed')
  }

  return response.json()
}

export async function getDocuments() {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/api/documents`, { headers })
  return response.json()
}

export async function deleteDocument(id: string) {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/api/documents/${id}`, {
    method: 'DELETE',
    headers,
  })

  if (!response.ok) {
    throw new Error('Delete failed')
  }

  return response.json()
}

export async function createThread(title?: string) {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/api/threads`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ title }),
  })
  return response.json()
}

export async function getThreads() {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/api/threads`, { headers })
  return response.json()
}

export async function getThreadMessages(threadId: string) {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/api/threads/${threadId}/messages`, { headers })
  return response.json()
}
