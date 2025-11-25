"use client";

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, BookOpen, AlertCircle, Mic, MicOff, Volume2, VolumeX, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSpeechRecognition, useTextToSpeech } from '@/hooks/use-speech';
import { Button } from '@/components/ui/button';
import { api } from '@/app/api/client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceInfo[];
  timestamp: Date;
}

interface SourceInfo {
  text: string;
  subject?: string;
  chapter?: string;
  source?: string;
  relevance_score: number;
}

export default function DoubtSolverChat() {
  // State management
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [showSources, setShowSources] = useState<string | null>(null);

  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Retry configuration
  const retryConfig = {
    maxRetries: 3,
    initialDelay: 1000
  };
  const retryConfig = {
    maxRetries: 3,
    initialDelay: 1000
  };
  
  const { isListening, transcript, startListening, stopListening, resetTranscript, isSupported: speechSupported } = useSpeechRecognition();
  const { speak, stop: stopSpeaking, isSpeaking, isSupported: ttsSupported } = useTextToSpeech();
  
  useEffect(() => {
    if (transcript) {
      setInput(transcript);
    }
  }, [transcript]);
  
  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      resetTranscript();
      startListening();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const retryableRequest = async (
    request: () => Promise<any>,
    maxRetries: number = 3,
    initialDelay: number = 1000
  ) => {
    let retryCount = 0;
    let lastError: Error | null = null;

    while (retryCount < maxRetries) {
      try {
        return await request();
      } catch (error) {
        console.error(`Attempt ${retryCount + 1}/${maxRetries} failed:`, error);
        lastError = error instanceof Error ? error : new Error(String(error));
        
        if (retryCount < maxRetries - 1) {
          const delay = Math.min(initialDelay * Math.pow(2, retryCount), 5000);
          await new Promise(resolve => setTimeout(resolve, delay));
          retryCount++;
          continue;
        }
        
        throw lastError;
      }
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const maxRetries = 3;
    let retryCount = 0;

    while (retryCount < maxRetries) {
      try {
        console.log('[DoubtSolverChat] sending request', {
          input: input.trim(),
          selectedSubject: selectedSubject || null,
          attempt: retryCount + 1,
        });

        const data = await api.askDoubt(input.trim(), selectedSubject || null);

        if (!data || typeof data.answer !== 'string') {
          console.warn('[DoubtSolverChat] unexpected API response payload', data);
          throw new Error('API response missing "answer" field');
        }

        if (data.sources && !Array.isArray(data.sources)) {
          console.warn('[DoubtSolverChat] sources payload is not an array', data.sources);
        }

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
          timestamp: new Date(),
        };

        // Clear any previous error messages for this query
        setMessages(prev => prev.filter(m => 
          !(m.role === 'assistant' && m.content.includes('Sorry, I encountered an error'))
        ));

      setMessages((prev) => [...prev, assistantMessage]);
      
      // Auto-speak response
      if (ttsSupported) {
        speak(data.answer);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error processing your question. ${error instanceof Error ? error.message : 'Please try again.'}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Card className="h-[calc(100vh-8rem)] flex flex-col">
      <CardHeader className="border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Sparkles className="w-5 h-5 text-primary" />
            </div>
            <div>
              <CardTitle>JEE Doubt Solver</CardTitle>
              <CardDescription>Get instant answers with source citations</CardDescription>
            </div>
          </div>
          
          <select
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            className="px-3 py-2 border border-input rounded-md bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">All Subjects</option>
            <option value="Physics">Physics</option>
            <option value="Chemistry">Chemistry</option>
            <option value="Mathematics">Mathematics</option>
          </select>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col p-4 gap-4 overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col items-center justify-center h-full text-center"
            >
              <div className="p-4 bg-accent/20 rounded-full mb-4">
                <BookOpen className="w-12 h-12 text-accent" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Ask Your JEE Doubts!</h3>
              <p className="text-sm text-muted-foreground max-w-md">
                I'll provide detailed answers based on NCERT and JEE study materials with source citations.
              </p>
            </motion.div>
          ) : (
            <AnimatePresence initial={false}>
              {messages.map((message) => (
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
                      "max-w-[85%] rounded-lg p-4 shadow-sm",
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted text-foreground'
                    )}
                  >
                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-4 pt-3 border-t border-border/50">
                        <button
                          onClick={() => setShowSources(showSources === message.id ? null : message.id)}
                          className="text-xs font-semibold mb-2 flex items-center gap-1 hover:underline"
                        >
                          <BookOpen className="w-3 h-3" />
                          {message.sources.length} Source{message.sources.length > 1 ? 's' : ''}
                        </button>
                        
                        <AnimatePresence>
                          {showSources === message.id && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              className="space-y-2 overflow-hidden"
                            >
                              {message.sources.map((source, idx) => (
                                <div
                                  key={idx}
                                  className="text-xs bg-background/50 p-3 rounded border border-border"
                                >
                                  {source.subject && source.chapter && (
                                    <div className="font-medium text-accent mb-1">
                                      {source.subject} • {source.chapter}
                                    </div>
                                  )}
                                  <div className="text-muted-foreground line-clamp-2">
                                    {source.text}
                                  </div>
                                  <div className="text-muted-foreground/70 mt-1">
                                    Relevance: {(source.relevance_score * 100).toFixed(0)}%
                                  </div>
                                </div>
                              ))}
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    )}
                    
                    <div className="flex items-center justify-between mt-3 pt-2 border-t border-border/30">
                      <p className="text-xs opacity-70">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                      {message.role === 'assistant' && ttsSupported && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 px-2"
                          onClick={() => isSpeaking ? stopSpeaking() : speak(message.content)}
                        >
                          {isSpeaking ? <VolumeX className="h-3 w-3" /> : <Volume2 className="h-3 w-3" />}
                        </Button>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
          
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-muted rounded-lg p-4 shadow-sm">
                <Loader2 className="w-5 h-5 animate-spin text-primary" />
              </div>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="flex items-end gap-2">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Ask your JEE doubt... (Shift+Enter for new line)"
              className="w-full rounded-lg border bg-background px-4 py-3 pr-12 resize-none focus:outline-none focus:ring-2 focus:ring-ring"
              rows={2}
              disabled={isLoading}
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
            disabled={!input.trim() || isLoading}
            size="icon"
            className="h-12 w-12"
          >
            {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
