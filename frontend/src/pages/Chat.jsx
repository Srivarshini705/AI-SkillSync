import { useState } from 'react'
import './Chat.css'

function Chat() {
  const [message, setMessage] = useState('')

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: 'Hi! I am SkillSync. How can I help you with your career today?',
    },
  ])

  function handleSubmit(event) {
    event.preventDefault()

    if (!message.trim()) {
      return
    }

    const newUserMessage = {
      id: Date.now(),
      sender: 'user',
      text: message,
    }

    setMessages((previousMessages) => [
      ...previousMessages,
      newUserMessage,
    ])

    setMessage('')
  }

  return (
    <div className="chat-page">
      <div className="chat-header">
        <h1>Chat with SkillSync</h1>
        <p>
          Ask questions about your career, skills, resumes, and opportunities.
        </p>
      </div>

      <div className="chat-container">
        <div className="messages-area">
          {messages.map((chatMessage) => (
            <div
              key={chatMessage.id}
              className={`message ${
                chatMessage.sender === 'user'
                  ? 'user-message'
                  : 'assistant-message'
              }`}
            >
              <div className="message-label">
                {chatMessage.sender === 'user'
                  ? 'You'
                  : 'SkillSync'}
              </div>

              <div className="message-text">
                {chatMessage.text}
              </div>
            </div>
          ))}
        </div>

        <form
          className="chat-input-area"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Ask SkillSync something..."
          />

          <button type="submit">
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

export default Chat