import { GoogleGenerativeAI } from '@google/generative-ai'

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}

const apiKey = process.env.GOOGLE_API_KEY
const genAI = apiKey ? new GoogleGenerativeAI(apiKey) : null

export async function POST(req: Request) {
  if (!genAI) {
    return Response.json(
      { error: 'GOOGLE_API_KEY is not configured on the server.' },
      { status: 500 }
    )
  }

  try {
    const { messages } = await req.json()

    if (!Array.isArray(messages) || messages.length === 0) {
      return Response.json({ error: 'Messages array is required.' }, { status: 400 })
    }

    const model = genAI.getGenerativeModel({ model: 'gemini-pro' })

    const result = await model.generateContent({
      contents: messages.map((message: ChatMessage) => ({
        role: message.role === 'user' ? 'user' : 'model',
        parts: [{ text: message.content }]
      }))
    })

    const response = await result.response
    const text = response.text()

    if (!text) {
      return Response.json({ error: 'No response generated.' }, { status: 502 })
    }

    return Response.json({ response: text.trim() })
  } catch (error) {
    console.error('[chat-route] Error generating response', error)
    return Response.json(
      { error: 'Failed to generate response from Gemini model.' },
      { status: 500 }
    )
  }
}