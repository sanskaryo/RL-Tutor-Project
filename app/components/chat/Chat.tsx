'use client'

import { useRef, useState, useEffect } from 'react'
import { nanoid } from 'nanoid'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Volume2, VolumeX, Send, Loader2 } from 'lucide-react'
import { useSpeechRecognition, useTextToSpeech } from '@/hooks/use-speech'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

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
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const { isListening, transcript, startListening, stopListening, resetTranscript, isSupported: speechSupported } = useSpeechRecognition()
  const { speak, stop: stopSpeaking, isSpeaking, isSupported: ttsSupported } = useTextToSpeech()

  useEffect(() => {
    if (transcript) {
      setInput(transcript)
    }
  }, [transcript])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const toggleListening = () => {
    if (isListening) {
      stopListening()
    } else {
      resetTranscript()
      startListening()
    }
  }

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

      // Auto-speak assistant response if TTS is supported
      if (ttsSupported) {
        speak(data.response)
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  return (
    <Card className="h-[calc(100vh-12rem)] flex flex-col">
      <CardContent className="flex-1 flex flex-col p-4 gap-4">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          <AnimatePresence initial={false}>
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.3 }}
                className={cn(
                  "flex",
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                <div
                  className={cn(
                    "rounded-lg px-4 py-3 max-w-[80%] shadow-sm",
                    message.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-foreground'
                  )}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  {message.role === 'assistant' && ttsSupported && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="mt-2 h-6 px-2"
                      onClick={() => isSpeaking ? stopSpeaking() : speak(message.content)}
                    >
                      {isSpeaking ? <VolumeX className="h-3 w-3" /> : <Volume2 className="h-3 w-3" />}
                    </Button>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-muted rounded-lg px-4 py-3">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="flex items-end gap-2">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSubmit(e)
                }
              }}
              placeholder="Type a message... (Shift+Enter for new line)"
              className="w-full rounded-lg border bg-background px-4 py-3 pr-12 resize-none focus:outline-none focus:ring-2 focus:ring-ring"
              rows={2}
              disabled={loading}
            />
            {speechSupported && (
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className={cn(
                  "absolute right-2 top-2",
                  isListening && "text-destructive animate-pulse"
                )}
                onClick={toggleListening}
              >
                {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
              </Button>
            )}
          </div>
          <Button
            type="submit"
            disabled={loading || !input.trim()}
            size="icon"
            className="h-12 w-12"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}