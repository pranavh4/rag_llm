import './App.css';
import {Widget, toggleWidget, addResponseMessage, deleteMessages, renderCustomComponent} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import {useEffect} from 'react'

function App() {
    useEffect(() => {
        toggleWidget()
    }, []);

    const handleNewUserMessage = (newMessage) => {
        renderCustomComponent(typingIndicator)

        fetch("/response", {
            "method": "POST",
            "body": JSON.stringify({"text": newMessage}),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(res => {
                if (res.status > 299 || res.status < 200) {
                    return {"status": "failure"}
                }

                return res.json()
            })
            .then(data => {
                deleteMessages(1)
                if (data.status === "failure") {
                    alert("Server Error")
                } else {
                    addResponseMessage(data.response || '')
                }
            })
    };

    return (
        <div className="App">
            <Widget
                fullScreenMode={true}
                showChat={true}
                emojis={true}
                title="FinBot"
                subtitle="Chatbot for Financial Analysts powered by LLMs and Retrieval Augmented Generation"
                handleNewUserMessage={handleNewUserMessage}
            />
        </div>
    );
}

const typingIndicator = () => {
    return (
        <img className="typing-indicator" src="/typing-animation-3x.gif" alt='Typing...'/>
    )
}
export default App;
