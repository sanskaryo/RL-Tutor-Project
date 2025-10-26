'use client'

import { useRef, useState } from 'react'
import { nanoid } from 'nanoid'

export type Message = {
  id: string
  content: string
  role: 'user' | 'assistant'
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()

    if (input.trim() === '') {
      return
    }

    setLoading(true)
    const userMessage: Message = {
      id: nanoid(),
      content: input,
      role: 'user'
    }

    setMessages(messages => [...messages, userMessage])
    setInput('')

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          messages: [...messages, userMessage].map(message => ({
            role: message.role,
            content: message.content
          }))
        })
      })

      if (!response.ok) {
        throw new Error(response.statusText)
      }

      const data = await response.json()

      const assistantMessage: Message = {
        id: nanoid(),
        content: data.response,
        role: 'assistant'
      }

      setMessages(messages => [...messages, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  return (
    <div className="rounded-lg border bg-background p-4">
      <div className="space-y-4">
        <div className="space-y-4">
          {messages.map(message => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 rounded-lg border bg-background p-2"
            rows={1}
            disabled={loading}
          />
          <button
            type="submit"
            className="rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/90"
            disabled={loading}
          >
            {loading ? 'Thinking...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}