#!/usr/bin/env python3
"""
Script to generate chat interface HTML from prompts.yaml
"""

import yaml
import json
import re


def extract_qa_messages(file_path: str = "prompts.yaml"):
    """Extract Q&A messages and user initials from YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {}
            prompts = data.get('prompts', [])
            users = data.get('users', {})
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return [], {}
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return [], {}

    normalized_users = {
        str(key): str(value) for key, value in (users or {}).items()
    }

    messages = []
    for prompt in prompts:
        prompt = prompt.strip()
        if (prompt.startswith('Q') or prompt.startswith('A') or
            prompt.startswith('Q1') or prompt.startswith('Q2') or
            prompt.startswith('A1') or prompt.startswith('A2') or
            prompt.startswith('A3') or prompt.startswith('A4')):

            # Extract type and text using regex
            match = re.match(r'^([QA]\d*):?\s*(.*)$', prompt)
            if match:
                msg_type = match.group(1)
                msg_text = match.group(2)
                messages.append({"type": msg_type, "text": msg_text})

    return messages, normalized_users


def generate_html(messages, user_initials):
    """Generate complete HTML with embedded messages."""
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q&A Chat History</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');

        body {
            font-family: 'Lato', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background-color: #f2f2f7;
            padding: 20px;
            min-height: 100vh;
        }

        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            position: relative;
        }

        .chat-header {
            background: white;
            color: #333;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 20px;
            font-weight: 600;
            border-bottom: 1px solid #e0e0e0;
        }

        .header-nav {
            display: flex;
            align-items: center;
        }

        .back-button {
            font-size: 24px;
            color: #8e8e93;
            text-decoration: none;
            margin-right: 16px;
            cursor: pointer;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .demo-button {
            background-color: #9966cc;
            color: white;
            border: none;
            border-radius: 18px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s ease;
        }

        .demo-button:hover:not(:disabled) {
            opacity: 0.85;
        }

        .demo-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .kebab-menu {
            font-size: 20px;
            color: #8e8e93;
            cursor: pointer;
            transform: rotate(90deg);
        }

        .logo-placeholder {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            margin-right: 12px;
            flex-shrink: 0;
        }

        .header-title {
            margin-left: 12px;
            font-weight: 600;
        }

        .chat-messages {
            padding: 20px;
            max-height: 60vh;
            overflow-y: auto;
            background-color: #f8f9fa;
        }

        .message {
            margin-bottom: 16px;
            display: flex;
            align-items: flex-end;
        }

        .message.question {
            justify-content: flex-start;
        }

        .message.question .question-logo {
            width: 24px;
            height: 24px;
            margin-right: 8px;
            border-radius: 4px;
            flex-shrink: 0;
            align-self: flex-start;
        }

        .message.answer {
            justify-content: flex-end;
        }

        .message.answer .answer-avatar {
            width: 24px;
            height: 24px;
            margin-left: 8px;
            border-radius: 12px;
            flex-shrink: 0;
            align-self: flex-start;
            background-color: #CCCFDA;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 600;
            color: #333;
        }

        .message-bubble {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 16px;
            line-height: 1.4;
            word-wrap: break-word;
        }

        .question .message-bubble {
            background-color: #e5e5ea;
            color: #000;
            border-bottom-left-radius: 6px;
        }

        .answer .message-bubble {
            background-color: #9966cc;
            color: white;
            border-bottom-right-radius: 6px;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #8e8e93;
            font-size: 18px;
        }

        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #8e8e93;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        .error {
            text-align: center;
            padding: 40px;
            color: #ff3b30;
            font-size: 18px;
        }

        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .chat-container {
                border-radius: 0;
                height: 100vh;
            }

            .chat-messages {
                max-height: calc(100vh - 140px);
            }

            .message-bubble {
                max-width: 85%;
            }
        }

        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .input-wrapper {
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
            background: #f8f9fa;
            border-radius: 20px;
            padding: 12px 16px;
            border: 1px solid #e0e0e0;
        }

        .input-wrapper:focus-within {
            border-color: #9966cc;
            box-shadow: 0 0 0 2px rgba(153, 102, 204, 0.1);
        }

        .message-input {
            flex: 1;
            border: none;
            background: none;
            outline: none;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
            color: #333;
            padding: 0;
        }

        .message-input::placeholder {
            color: #8e8e93;
        }

        .mic-button {
            background: none;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            flex-shrink: 0;
            padding: 8px;
        }

        .mic-button:hover {
            opacity: 0.7;
        }

        .mic-button:active {
            opacity: 0.5;
        }

        .mic-icon {
            width: 16px;
            height: 20px;
            position: relative;
        }

        .mic-icon::before {
            content: '';
            position: absolute;
            width: 8px;
            height: 12px;
            background: white;
            border-radius: 4px;
            top: 0;
            left: 4px;
        }

        .mic-icon::after {
            content: '';
            position: absolute;
            width: 12px;
            height: 12px;
            border: 2px solid white;
            border-top: none;
            border-radius: 0 0 12px 12px;
            bottom: 4px;
            left: 2px;
        }

        @media (max-width: 768px) {
            .chat-input {
                padding: 15px;
            }

            .input-wrapper {
                padding: 10px 14px;
            }

            .mic-button {
                padding: 6px;
            }
        }

        .disclaimer {
            padding: 12px 20px;
            background: #f8f9fa;
            color: #8e8e93;
            font-size: 12px;
            line-height: 1.4;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }

        .demo-timer {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 600;
            display: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-nav">
                <span class="back-button">‹</span>
            </div>
            <div class="header-actions">
                <button class="demo-button" id="demoButton" type="button">Play Demo</button>
                <div class="kebab-menu">⋯</div>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
        </div>
        <div class="chat-input">
            <div class="input-wrapper">
                <input type="text" class="message-input" placeholder="Type a message..." />
            </div>
            <button class="mic-button" title="Voice input">
                <img src="microphone.png" alt="Microphone" style="width: 36px; height: 36px;">
            </button>
        </div>
        <div class="disclaimer">
            Please share openly. Your responses are private and help identify alignment gaps. Respectful summaries will be shared with everyone.
        </div>
    </div>
    <div class="demo-timer" id="demoTimer" aria-live="polite"></div>

    <script>
        const messages = {messages_json};
        const userInitials = {user_initials_json};

        const chatMessagesEl = document.getElementById('chatMessages');
        const demoButton = document.getElementById('demoButton');
        const demoTimerEl = document.getElementById('demoTimer');
        let demoRunning = false;
        const SPEED_FACTOR = 0.2;

        function displayMessages(list) {
            chatMessagesEl.innerHTML = '';

            list.forEach((message) => {
                const { messageDiv, bubbleDiv } = buildMessageElement(message);
                bubbleDiv.textContent = message.text;
                chatMessagesEl.appendChild(messageDiv);
            });

            chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
        }

        function buildMessageElement(message) {
            const messageDiv = document.createElement('div');
            const isQuestion = message.type.toLowerCase().startsWith('q');
            messageDiv.className = `message ${isQuestion ? 'question' : 'answer'}`;

            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'message-bubble';

            if (isQuestion) {
                const logoImg = document.createElement('img');
                logoImg.src = 'logo.png';
                logoImg.alt = 'Logo';
                logoImg.className = 'question-logo';
                messageDiv.appendChild(logoImg);
            }

            messageDiv.appendChild(bubbleDiv);

            if (message.type.toLowerCase().startsWith('a')) {
                const avatarDiv = document.createElement('div');
                avatarDiv.className = 'answer-avatar';
                avatarDiv.textContent = getInitialsForAnswer(message.type);
                messageDiv.appendChild(avatarDiv);
            }

            return { messageDiv, bubbleDiv };
        }

        function getInitialsForAnswer(messageType) {
            const match = messageType.match(/^a(\\d+)/i);
            if (!match) return userInitials.default || 'BG';

            return userInitials[match[1]] || userInitials.default || 'BG';
        }

        async function startDemo() {
            if (demoRunning) return;
            demoRunning = true;
            hideDemoTimer();
            if (demoButton) {
                demoButton.disabled = true;
                demoButton.textContent = 'Playing…';
            }

            const startTime = performance.now();
            await playDemo(messages);
            const elapsedMs = performance.now() - startTime;

            demoRunning = false;
            if (demoButton) {
                demoButton.disabled = false;
                demoButton.textContent = 'Replay Demo';
            }
            showDemoTimer(elapsedMs);
        }

        async function playDemo(list) {
            chatMessagesEl.innerHTML = '';

            for (const message of list) {
                const { messageDiv, bubbleDiv } = buildMessageElement(message);
                bubbleDiv.textContent = '';
                chatMessagesEl.appendChild(messageDiv);
                chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
                await typeText(bubbleDiv, message.text, message.type.toLowerCase().startsWith('q') ? 'question' : 'answer');
                await pauseBetweenMessages(message);
            }
        }

        function typeText(node, text, role) {
            return new Promise((resolve) => {
                let index = 0;

                function typeNextChar() {
                    if (index >= text.length) {
                        resolve();
                        return;
                    }

                    const currentChar = text[index];
                    node.textContent += currentChar;
                    index += 1;

                    const delay = role === 'question' ? smoothDelay() : irregularDelay(currentChar);
                    setTimeout(typeNextChar, delay);
                }

                typeNextChar();
            });
        }

        function smoothDelay() {
            const base = 28 + Math.random() * 12;
            return base * SPEED_FACTOR;
        }

        function irregularDelay(char) {
            if (/[.!?]/.test(char)) {
                return (320 + Math.random() * 200) * SPEED_FACTOR;
            }
            if (char === ',') {
                return (180 + Math.random() * 120) * SPEED_FACTOR;
            }
            if (char.trim() === '') {
                return (90 + Math.random() * 90) * SPEED_FACTOR;
            }
            return (45 + Math.random() * 80) * SPEED_FACTOR;
        }

        function pauseBetweenMessages(message) {
            const isQuestion = message.type.toLowerCase().startsWith('q');
            const pause = (isQuestion ? 300 : 500) * SPEED_FACTOR;
            return new Promise((resolve) => setTimeout(resolve, pause));
        }

        document.addEventListener('DOMContentLoaded', () => {
            displayMessages(messages);

            if (demoButton) {
                demoButton.addEventListener('click', startDemo);
            }

            const params = new URLSearchParams(window.location.search);
            if (params.get('demo') === '1') {
                startDemo();
            }
        });

        function showDemoTimer(durationMs) {
            if (!demoTimerEl) return;
            demoTimerEl.textContent = `Total elapsed: ${formatDuration(durationMs)}`;
            demoTimerEl.style.display = 'block';
        }

        function hideDemoTimer() {
            if (!demoTimerEl) return;
            demoTimerEl.style.display = 'none';
        }

        function formatDuration(durationMs) {
            const totalSeconds = Math.round(durationMs / 1000);
            const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
            const seconds = String(totalSeconds % 60).padStart(2, '0');
            return `${minutes}:${seconds}`;
        }
    </script>
</body>
</html>'''

    return (
        html_template
        .replace('{messages_json}', json.dumps(messages, indent=2))
        .replace('{user_initials_json}', json.dumps(user_initials, indent=2))
    )


def main():
    """Main function to generate HTML from YAML."""
    messages, user_initials = extract_qa_messages()

    if not messages:
        print("No Q&A messages found.")
        return

    # Print summary like before
    print("Q&A Summary from prompts.yaml:")
    print("=" * 50)
    for msg in messages:
        print(f"{msg['type']}: {msg['text']}")
    print("=" * 50)

    # Generate and save HTML
    html_content = generate_html(messages, user_initials)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Generated index.html with {len(messages)} messages.")


if __name__ == "__main__":
    main()
