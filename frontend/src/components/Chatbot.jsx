import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FiSend, FiMic, FiVolume2 } from 'react-icons/fi';
import './Chatbot.css';

export default function FarmingChatbot() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Welcome to Smart Farming Assistant! 👨‍🌾 I can help you with crop information, disease detection, weather, prices, irrigation, and government schemes. What would you like to know?',
    }
  ]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const API_URL = process.env.REACT_APP_API_URL;
  const token = localStorage.getItem('accessToken');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    // Add user message
    const newMessage = {
      id: messages.length + 1,
      type: 'user',
      text,
    };
    setMessages([...messages, newMessage]);
    setInput('');

    // Get bot response
    try {
      setLoading(true);
      // Mock API call - in production, call actual chatbot API
      const response = await axios.post(
        `${API_URL}/api/chatbot/query`,
        { query: text },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      ).catch(() => ({
        data: {
          response: getMockChatbotResponse(text),
        }
      }));

      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: response.data.response,
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMockChatbotResponse = (query) => {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('rice') || lowerQuery.includes('wheat')) {
      return '🌾 Rice is a monsoon crop that requires 200-300mm water per month. Best soil is clay loam with pH 6.0-7.0. Expected yield is 4000-6000 kg/ha. Would you like more details?';
    } else if (lowerQuery.includes('disease') || lowerQuery.includes('pest')) {
      return '🦠 Common diseases include leaf blast, brown spot, and leaf scald. Use fungicides like Mancozeb for chemical treatment or neem oil for organic control. For accurate diagnosis, upload a leaf image.';
    } else if (lowerQuery.includes('water') || lowerQuery.includes('irrigation')) {
      return '💧 Water requirement depends on crop and season. Check soil moisture before irrigating. Best time is early morning or late evening. Drip irrigation is most efficient.';
    } else if (lowerQuery.includes('price') || lowerQuery.includes('market')) {
      return '📊 Use AI price prediction to determine the best time to sell. Current market trends show prices may increase in the next 2 weeks. Check AGMARKNET for daily rates.';
    } else if (lowerQuery.includes('subsidy') || lowerQuery.includes('scheme')) {
      return '💰 PM-KISAN provides ₹6000/year, Soil Health Card offers free testing, and Crop Insurance protects against losses. Check government portals for eligibility.';
    } else {
      return '👨‍🌾 I can help with crops, diseases, irrigation, market prices, weather, and subsidies. What specific farming topic interests you?';
    }
  };

  const handleVoiceInput = () => {
    if (!isListening) {
      // Start listening
      setIsListening(true);
      // In production, integrate Web Speech API or cloud speech-to-text
    } else {
      setIsListening(false);
    }
  };

  const handleQuickQuestion = (question) => {
    handleSendMessage(question);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h2>🤖 Smart Farming Assistant</h2>
        <p>24/7 AI-powered farming guidance</p>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            {message.type === 'bot' && <span className="avatar">🤖</span>}
            {message.type === 'user' && <span className="avatar">👨‍🌾</span>}
            <div className="message-content">
              {message.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <span className="avatar">🤖</span>
            <div className="message-content typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions */}
      <div className="quick-questions">
        <button onClick={() => handleQuickQuestion('Tell me about rice farming')}>
          🌾 Rice Info
        </button>
        <button onClick={() => handleQuickQuestion('How to prevent crop diseases?')}>
          🦠 Disease Prevention
        </button>
        <button onClick={() => handleQuickQuestion('Irrigation guidance please')}>
          💧 Irrigation
        </button>
        <button onClick={() => handleQuickQuestion('Current crop prices?')}>
          📊 Market Prices
        </button>
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(input)}
            placeholder="Ask about crops, weather, prices, diseases..."
            disabled={loading}
          />
          <button 
            className={`voice-btn ${isListening ? 'listening' : ''}`}
            onClick={handleVoiceInput}
            title="Voice input"
          >
            <FiMic />
          </button>
          <button 
            className="send-btn"
            onClick={() => handleSendMessage(input)}
            disabled={loading || !input.trim()}
            title="Send message"
          >
            <FiSend />
          </button>
        </div>
      </div>
    </div>
  );
}
