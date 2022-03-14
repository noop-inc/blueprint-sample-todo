export const fetchAllTodos = async () => {
  const res = await window.fetch('/api/todos')
  return await res.json()
}

export const fetchTodo = async id => {
  const res = await window.fetch(`/api/todos/${id}`)
  return await res.json()
}

export const createTodo = async item => {
  const res = await window.fetch(
    '/api/todos/',
    { method: 'POST', body: item }
  )
  return await res.json()
}

export const updateTodo = async item => {
  const res = await window.fetch(
    `/api/todos/${item.id}`,
    {
      method: 'PUT',
      body: JSON.stringify(item),
      headers: {
        'Content-Type': 'application/json'
      }
    }
  )
  return await res.json()
}

export const deleteTodo = async id => {
  const res = await window.fetch(
    `/api/todos/${id}`,
    { method: 'DELETE' }
  )
  return await res.json()
}
