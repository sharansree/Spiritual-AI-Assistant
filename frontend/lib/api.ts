const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function request(path: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('sathya_token') : null

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Something went wrong')
  return data
}

export const api = {
  auth: {
    register: (body: { name: string; email: string; password: string }) =>
      request('/auth/register', { method: 'POST', body: JSON.stringify(body) }),
    login: (body: { email: string; password: string }) =>
      request('/auth/login', { method: 'POST', body: JSON.stringify(body) }),
    verify: (token: string) =>
      request(`/auth/verify?token=${token}`),
    forgotPassword: (email: string) =>
      request('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),
    resetPassword: (token: string, new_password: string) =>
      request('/auth/reset-password', { method: 'POST', body: JSON.stringify({ token, new_password }) }),
  },
  questions: {
    ask: (question: string) =>
      request('/questions/ask', { method: 'POST', body: JSON.stringify({ question }) }),
    history: () =>
      request('/questions/history'),
    delete: (id: string) =>
      request(`/questions/${id}`, { method: 'DELETE' }),
  },
}