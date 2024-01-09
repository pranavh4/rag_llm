import logo from './logo.svg';
import './App.css';
import { Widget, toggleWidget, addResponseMessage } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import {useEffect} from 'react'


function App() {
  useEffect(() => {
    toggleWidget()
  }, []);

  const handleNewUserMessage = (newMessage) => {
    console.log(`New message incoming! ${newMessage}`);
    // Now send the message throught the backend API
    addResponseMessage("test")
  };


  return (
    <div className="App">
      <Widget
        fullScreenMode={true}
        showChat={true}
        emojis={true}
        title="FinBot"
        subtitle="Chatbot for Financial Analysts powered by LLMs and Retrieveal Augmented Generation"
        handleNewUserMessage={handleNewUserMessage}
      />
    </div>
  );
}

export default App;
