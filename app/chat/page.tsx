import { Chat } from '@/app/components/chat/Chat'

export default function ChatPage() {
  return (
    <div className="container mx-auto max-w-4xl p-4">
      <div className="space-y-4">
        <h1 className="text-2xl font-bold">Educational Assistant</h1>
        <p className="text-muted-foreground">
          Ask me anything about your coursework, concepts, or learning journey!
        </p>
        <Chat />
      </div>
    </div>
  )
}