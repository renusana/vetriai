import { useEffect, useRef, useState } from "react";
import "./AIChat.css";

function AIChat() {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello! I am Vetri AI BO Assistant. How can I help you today?",
    },
  ]);

  const [conversationId, setConversationId] = useState(null);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  /*
   * Load the current user's latest conversation
   * when AI Chat page opens.
   */
  useEffect(() => {
    const loadConversationHistory = async () => {
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        setIsLoadingHistory(false);
        return;
      }

      try {
        /*
         * Get all conversations belonging to
         * the currently authenticated user.
         */
        const response = await fetch(
          "http://127.0.0.1:8000/api/conversations/",
          {
            method: "GET",
            credentials: "include",
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to load conversations");
        }

        const data = await response.json();

        const conversations = data.conversations || [];

        /*
         * If the user has previous conversations,
         * use the latest one.
         */
        if (conversations.length > 0) {
          const latestConversation = conversations[0];

          setConversationId(latestConversation.id);

          /*
           * Get the complete conversation including
           * all messages.
           */
          const detailResponse = await fetch(
            `http://127.0.0.1:8000/api/conversations/${latestConversation.id}/`,
            {
              method: "GET",
              credentials: "include",
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            }
          );

          if (!detailResponse.ok) {
            throw new Error(
              "Failed to load conversation details"
            );
          }

          const detailData = await detailResponse.json();

          const savedMessages =
            detailData.conversation?.messages || [];

          /*
           * Convert backend message format:
           *
           * user      -> user
           * assistant -> ai
           *
           * content -> text
           */
          const formattedMessages = savedMessages.map(
            (message) => ({
              sender:
                message.sender === "user"
                  ? "user"
                  : "ai",
              text: message.content,
            })
          );

          if (formattedMessages.length > 0) {
            setMessages(formattedMessages);
          }
        }
      } catch (error) {
        console.error(
          "Conversation History Error:",
          error
        );
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadConversationHistory();
  }, []);

  /*
   * Keep chat scrolled to the latest message.
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  const handleSend = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isLoading) {
      return;
    }

    const userMessage = {
      sender: "user",
      text: trimmedQuestion,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);

    setQuestion("");
    setIsLoading(true);

    const accessToken = localStorage.getItem("access_token");

    try {
      /*
       * Send the conversation ID when available.
       *
       * If it is null, the backend will create a
       * new conversation automatically.
       */
      const requestBody = {
        message: trimmedQuestion,
      };

      if (conversationId) {
        requestBody.conversation_id = conversationId;
      }

      const response = await fetch(
        "http://127.0.0.1:8000/api/chat/",
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify(requestBody),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Failed to get response from AI"
        );
      }

      const data = await response.json();

      /*
       * Store conversation ID returned by backend.
       *
       * This is especially important when this is
       * the first message of a new conversation.
       */
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      const aiMessage = {
        sender: "ai",
        text:
          data.response ||
          "No response received from AI.",
        metadata: data.metadata || null,
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        aiMessage,
      ]);
    } catch (error) {
      console.error("Chat API Error:", error);

      const aiMessage = {
        sender: "ai",
        text: "Sorry, I could not connect to the AI service.",
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        aiMessage,
      ]);
    } finally {
      setIsLoading(false);

      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleSuggestion = (text) => {
    setQuestion(text);
    inputRef.current?.focus();
  };

  return (
    <div className="ai-chat-page">

      {/* Page Header */}

      <div className="ai-chat-topbar">

        <div>
          <h2 className="ai-chat-page-title">
            AI Chat
          </h2>

          <p className="ai-chat-page-subtitle">
            Interact with Vetri AI Business Operations Assistant
          </p>
        </div>

        <div className="ai-status">
          <span className="ai-status-dot"></span>
          AI Online
        </div>

      </div>


      {/* Chat Container */}

      <div className="ai-chat-container">

        {/* Chat Header */}

        <div className="ai-chat-header">

          <div className="ai-chat-brand">

            <div className="ai-chat-avatar">
              <i className="bi bi-stars"></i>
            </div>

            <div>
              <h5 className="mb-1">
                Vetri AI BO Assistant
              </h5>

              <div className="ai-chat-online">
                <span></span>
                Ready to assist
              </div>
            </div>

          </div>

          <div className="ai-chat-header-icon">
            <i className="bi bi-three-dots-vertical"></i>
          </div>

        </div>


        {/* Messages */}

        <div className="ai-chat-messages">

          {!isLoadingHistory &&
            messages.length === 1 &&
            messages[0].sender === "ai" && (
              <div className="ai-welcome">

                <div className="ai-welcome-icon">
                  <i className="bi bi-stars"></i>
                </div>

                <h4>
                  How can I help you?
                </h4>

                <p>
                  Ask me about employees, projects,
                  sales, reports, tasks and more.
                </p>

                <div className="ai-suggestions">

                  <button
                    type="button"
                    onClick={() =>
                      handleSuggestion(
                        "Show finance summary"
                      )
                    }
                  >
                    <i className="bi bi-currency-rupee"></i>
                    Finance summary
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      handleSuggestion(
                        "Show my projects"
                      )
                    }
                  >
                    <i className="bi bi-kanban"></i>
                    My projects
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      handleSuggestion(
                        "Show pending tasks"
                      )
                    }
                  >
                    <i className="bi bi-list-check"></i>
                    Pending tasks
                  </button>

                </div>

              </div>
            )}


          {messages.map((message, index) => (

            <div
              key={index}
              className={`ai-message-row ${message.sender === "user"
                ? "user-message-row"
                : "ai-message-row-left"
                }`}
            >

              {/* AI Avatar */}

              {message.sender === "ai" && (
                <div className="message-avatar ai-avatar">
                  <i className="bi bi-stars"></i>
                </div>
              )}


              <div
                className={`ai-message ${message.sender === "user"
                  ? "user-message"
                  : "assistant-message"
                  }`}
              >

                <div className="message-name">
                  {message.sender === "user"
                    ? "You"
                    : "Vetri AI"}
                </div>

                <div className="message-text">
                  {message.text}
                </div>

                {message.sender === "ai" && message.metadata && (
                  <div className="ai-message-metadata">
                    <div>
                      <strong>Source:</strong>{" "}
                      {message.metadata.source || "Vetri AI"}
                    </div>

                    <div>
                      <strong>Updated:</strong>{" "}
                      {message.metadata.updated_at
                        ? new Date(message.metadata.updated_at).toLocaleString()
                        : "Not available"}
                    </div>

                    <div>
                      <strong>Confidence:</strong>{" "}
                      {message.metadata.confidence || "Not available"}
                    </div>
                  </div>
                )}

              </div>


              {/* User Avatar */}

              {message.sender === "user" && (
                <div className="message-avatar user-avatar">
                  <i className="bi bi-person-fill"></i>
                </div>
              )}

            </div>

          ))}


          {/* Loading */}

          {isLoading && (
            <div className="ai-message-row ai-message-row-left">

              <div className="message-avatar ai-avatar">
                <i className="bi bi-stars"></i>
              </div>

              <div className="ai-message assistant-message typing-message">

                <div className="message-name">
                  Vetri AI
                </div>

                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

              </div>

            </div>
          )}

          <div ref={messagesEndRef}></div>

        </div>


        {/* Input */}

        <div className="ai-chat-input-area">

          <div className="ai-chat-input-wrapper">

            <input
              ref={inputRef}
              type="text"
              className="ai-chat-input"
              placeholder="Ask Vetri AI anything..."
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              onKeyDown={handleKeyDown}
              disabled={isLoading}
            />

            <button
              type="button"
              className="ai-send-button"
              onClick={handleSend}
              disabled={
                !question.trim() || isLoading
              }
              aria-label="Send message"
            >
              <i className="bi bi-send-fill"></i>
            </button>

          </div>

          <div className="ai-chat-footer-text">
            <i className="bi bi-shield-check"></i>
            Vetri AI can make mistakes. Verify important information.
          </div>

        </div>

      </div>

    </div>
  );
}

export default AIChat;