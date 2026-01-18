import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';
import RobotIcon from './RobotIcon';

const API_URL = 'http://localhost:8000';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Capture text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection ? selection.toString().trim() : '';
      if (text.length > 0 && text.length <= 5000) {
        setSelectedText(text);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  }, [isOpen]);

  // Prevent body scroll when chat is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedQuestion = question.trim();

    // Validation
    if (!trimmedQuestion) {
      setError('Please enter a question');
      return;
    }
    if (trimmedQuestion.length > 2000) {
      setError('Question is too long (max 2000 characters)');
      return;
    }

    // Add user message to chat
    const userMessage = {
      type: 'user',
      content: trimmedQuestion,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setLoading(true);
    setError(null);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 60000);

    try {
      const body = { question: trimmedQuestion };
      if (selectedText) {
        body.selected_text = selectedText;
      }

      const res = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${res.status}`);
      }

      const data = await res.json();

      // Add assistant message to chat
      const assistantMessage = {
        type: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      setSelectedText(''); // Clear after use
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('Request timed out. Please try again.');
      } else if (err.message.includes('Failed to fetch')) {
        setError('Unable to connect to the assistant. Please ensure the backend is running.');
      } else {
        setError(err.message || 'An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
  };

  const clearSelection = () => {
    setSelectedText('');
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      handleClose();
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {/* Floating Robot Button */}
      <button
        className={`${styles.toggleButton} ${isOpen ? styles.hidden : ''}`}
        onClick={() => setIsOpen(true)}
        aria-label="Open AI Assistant"
      >
        <RobotIcon size={72} />
        <span className={styles.buttonPulse}></span>
      </button>

      {/* Overlay */}
      <div
        className={`${styles.overlay} ${isOpen ? styles.overlayVisible : ''}`}
        onClick={handleClose}
        aria-hidden="true"
      />

      {/* Chat Panel */}
      <div
        className={`${styles.chatPanel} ${isOpen ? styles.chatPanelOpen : ''}`}
        onKeyDown={handleKeyDown}
        role="dialog"
        aria-label="AI Assistant Chat"
      >
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.headerLeft}>
            <div className={styles.headerIcon}>
              <RobotIcon size={32} />
            </div>
            <div className={styles.headerInfo}>
              <h3>Physical AI Assistant</h3>
              <span className={styles.headerStatus}>
                <span className={styles.statusDot}></span>
                Online
              </span>
            </div>
          </div>
          <button
            className={styles.closeButton}
            onClick={handleClose}
            aria-label="Close chat"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages Area */}
        <div className={styles.messagesContainer}>
          {/* Welcome message if no messages */}
          {messages.length === 0 && !loading && (
            <div className={styles.welcomeMessage}>
              <div className={styles.welcomeIcon}>
                <RobotIcon size={64} />
              </div>
              <h4>Welcome to the Physical AI Assistant</h4>
              <p>Ask me anything about humanoid robotics, ROS 2, simulation, or any topic from the textbook.</p>
              <div className={styles.suggestedQuestions}>
                <span className={styles.suggestedLabel}>Try asking:</span>
                <button
                  className={styles.suggestedBtn}
                  onClick={() => setQuestion('What is ROS 2?')}
                >
                  What is ROS 2?
                </button>
                <button
                  className={styles.suggestedBtn}
                  onClick={() => setQuestion('How do I simulate a robot in Gazebo?')}
                >
                  How to simulate in Gazebo?
                </button>
                <button
                  className={styles.suggestedBtn}
                  onClick={() => setQuestion('What is NVIDIA Isaac Sim?')}
                >
                  What is Isaac Sim?
                </button>
              </div>
            </div>
          )}

          {/* Selected Text Indicator */}
          {selectedText && (
            <div className={styles.selectedTextBadge}>
              <div className={styles.selectedTextIcon}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
              </div>
              <span>Using selected text as context</span>
              <button onClick={clearSelection} aria-label="Clear selection">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}

          {/* Chat Messages */}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`${styles.message} ${msg.type === 'user' ? styles.userMessage : styles.assistantMessage}`}
            >
              {msg.type === 'assistant' && (
                <div className={styles.messageAvatar}>
                  <RobotIcon size={28} />
                </div>
              )}
              <div className={styles.messageContent}>
                <div className={styles.messageText}>{msg.content}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <span className={styles.sourcesLabel}>Sources:</span>
                    <div className={styles.sourcesList}>
                      {msg.sources.map((src, srcIdx) => (
                        <a
                          key={srcIdx}
                          href={src.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={styles.sourceLink}
                        >
                          <span className={styles.sourceChapter}>{src.chapter}</span>
                          <span className={styles.sourceSection}>{src.section}</span>
                          <span className={styles.sourceScore}>
                            {(src.relevance_score * 100).toFixed(0)}%
                          </span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className={`${styles.message} ${styles.assistantMessage}`}>
              <div className={styles.messageAvatar}>
                <RobotIcon size={28} />
              </div>
              <div className={styles.messageContent}>
                <div className={styles.typingIndicator}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className={styles.errorContainer}>
              <div className={styles.errorIcon}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
              </div>
              <p>{error}</p>
              <button onClick={handleRetry} className={styles.retryButton}>
                Dismiss
              </button>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className={styles.inputForm}>
          <div className={styles.inputWrapper}>
            <input
              ref={inputRef}
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about the textbook..."
              disabled={loading}
              maxLength={2000}
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className={styles.sendButton}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
          <div className={styles.inputHint}>
            Press Enter to send
          </div>
        </form>
      </div>
    </div>
  );
}
