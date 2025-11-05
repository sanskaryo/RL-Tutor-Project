import { Chat } from '@/app/components/chat/Chat'
import { AppLayout } from '@/components/app-layout'

export default function ChatPage() {
  return (
    <AppLayout title="Educational Assistant" showBackButton>
      <div className="container mx-auto max-w-4xl p-6">
        <div className="mb-4">
          <p className="text-muted-foreground">
            Ask me anything about your coursework, concepts, or learning journey!
          </p>
        </div>
        <Chat />
      </div>
    </AppLayout>
  )
}