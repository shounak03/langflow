import React, { useState, useEffect } from 'react';
import { Button } from "../../ui/button";
import { Input } from "../../ui/input";
import { MessageCircle, X, Send } from "lucide-react";
import { cn } from "@/lib/utils";
import { api } from "@/controllers/API/api";

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

function ChatSupport() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchMessages = async () => {
    try {
      const response = await api.get('/api/v1/chat_history');
      const data = response.data;
      console.log('Chat history:', data);
      
      const formattedMessages = data.map((msg: any) => [
        { role: 'user' as const, content: msg.prompt, timestamp: msg.timestamp },
        { role: 'assistant' as const, content: msg.response, timestamp: msg.timestamp }
      ]).flat();
      
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchMessages();
    }
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.post('/api/v1/chat_gpt', { prompt: input });
      const data = response.data;
      console.log(data);
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, there was an error processing your request.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <Button
        onClick={() => setIsOpen(true)}
        className="h-12 w-12 rounded-full shadow-lg bg-primary hover:bg-primary/90"
        variant="default"
      >
        <MessageCircle className="h-6 w-6 text-primary-foreground" />
      </Button>

      {isOpen && (
        <div className="fixed bottom-20 right-4 w-96 rounded-lg border bg-background shadow-lg z-50">
          <div className="flex items-center justify-between border-b p-4">
            <h3 className="font-semibold">Chat Support</h3>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsOpen(false)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="h-96 overflow-y-auto p-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={cn(
                  "mb-4 rounded-lg p-3",
                  message.role === 'user'
                    ? "ml-auto bg-primary text-primary-foreground"
                    : "mr-auto bg-muted"
                )}
              >
                <div className="text-sm">{message.content}</div>
                {message.timestamp && (
                  <div className="text-xs opacity-70 mt-1">
                    {new Date(message.timestamp).toLocaleString()}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="mr-auto rounded-lg bg-muted p-3">
                Thinking...
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="border-t p-4">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                disabled={isLoading}
              />
              <Button type="submit" disabled={isLoading}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default ChatSupport;