import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Terminal, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AIChat = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'TACTICAL OS v4.0 ONLINE.\nAwaiting command inputs. Type "Sitrep" for status.' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await axios.post('http://localhost:8000/api/chat', { message: userMsg.text });
      const botMsg = { sender: 'bot', text: res.data.reply };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error: Link failure. Command center offline.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  const formatText = (text) => {
    return text.split('\n').map((line, i) => (
      <div key={i} className={`min-h-[1.2em] ${line.startsWith('-') ? 'pl-4' : ''}`}>
        {line.split(/(\*\*.*?\*\*|`.*?`)/g).map((part, j) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return <strong key={j} className="text-cyan-400 font-bold">{part.slice(2, -2)}</strong>;
          }
          if (part.startsWith('`') && part.endsWith('`')) {
            return <code key={j} className="bg-slate-800 text-green-400 px-1 rounded text-xs font-mono">{part.slice(1, -1)}</code>;
          }
          return part;
        })}
      </div>
    ));
  };

  return (
    <div className="flex flex-col h-full bg-slate-950/80 font-mono text-sm border border-cyan-900/30">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-slate-300 custom-scrollbar">
        {messages.map((msg, idx) => (
          <motion.div 
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            key={idx} 
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-[95%] p-3 rounded-sm text-[11px] leading-relaxed ${
              msg.sender === 'user' 
                ? 'bg-cyan-900/20 text-cyan-100 border-l-2 border-cyan-500' 
                : 'bg-slate-900/50 text-slate-300 border-l-2 border-green-500/50'
            }`}>
              <div className="text-[9px] uppercase font-black mb-1 opacity-50 flex items-center gap-1">
                {msg.sender === 'user' ? '> OPERATOR' : '> TACTICAL_AI'}
              </div>
              {formatText(msg.text)}
            </div>
          </motion.div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
             <div className="bg-slate-900/50 p-2 border-l-2 border-green-500/50 flex items-center gap-2">
                <Loader2 size={12} className="animate-spin text-green-500" />
                <span className="text-[10px] text-slate-500 animate-pulse uppercase">Thinking...</span>
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 bg-slate-900 border-t border-cyan-900/30 flex gap-2">
        <span className="text-green-500 py-2 font-bold">{'>'}</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Command input..."
          className="flex-1 bg-transparent text-slate-100 placeholder-slate-700 focus:outline-none font-mono text-xs"
        />
        <button 
          onClick={sendMessage} 
          className="p-2 text-cyan-600 hover:text-cyan-400 transition-colors"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
};

export default AIChat;
