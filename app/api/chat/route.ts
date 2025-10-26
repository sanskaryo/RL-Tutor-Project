import { GoogleGenerativeAI } from '@google/generative-ai'
import { GoogleGenerativeAIStream, Message, StreamingTextResponse } from 'ai'

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || '')

export async function POST(req: Request) {
  const { messages } = await req.json()
  const model = genAI.getGenerativeModel({ model: 'gemini-pro' })

  const geminiStream = await model.generateContentStream({
    contents: messages.map((m: Message) => ({
      role: m.role === 'user' ? 'user' : 'model',
      parts: [{ text: m.content }]
    }))
  })

  const stream = GoogleGenerativeAIStream(geminiStream)

  return new StreamingTextResponse(stream)
}