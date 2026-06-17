# AI-Autoreply-Chatbot
AI-powered auto-reply bot for WhatsApp/Instagram that uses vision LLMs to read chat screenshots and Groq's LLaMA models to generate human-like Hinglish replies, sent via simulated keyboard/mouse input.


AI Auto-Reply Chatbot (WhatsApp / Instagram)

A screen-vision based auto-reply bot that watches a chat window, detects new incoming messages using a vision LLM, generates a human-like Hinglish reply with an LLM, and sends it via simulated keyboard/mouse input.

How It Works

Screenshot – pyautogui captures a fixed region of the screen (CHAT_REGION) on a loop.
Detect – The screenshot is sent to a Groq vision model (llama-4-scout) which extracts the last message and decides if it's from the other person or from you.
Generate – If it's a new incoming message, a text model (llama-3.3-70b-versatile) generates a short, casual Hinglish reply.
Send – The reply is copied to the clipboard and pasted into the chat input box, then sent via a simulated click.

No platform APIs are used — this works purely by reading pixels and simulating clicks, so it's app-agnostic (works on any chat UI: WhatsApp Web, Instagram DMs, etc.) as long as the coordinates are configured correctly.

Setup

1. Install dependencies

bashpip install pyautogui pyperclip groq

2. Set your API key as an environment variable

Don't put it in the code. On Windows (PowerShell):

powershellsetx GROQ_API_KEY "your-key-here"

Then update the script:

pythonimport os
client = Groq(api_key=os.environ["GROQ_API_KEY"])

3. Configure screen coordinates

Open the target chat app, then find the right values for your screen/resolution:

VariableMeaningCHAT_REGION(x1, y1, x2, y2) — bounding box of the chat message area to screenshotINPUT_BOX(x, y) — coordinates of the message text input fieldSEND_BTN(x, y) — coordinates of the send button

Use pyautogui.position() in a Python shell (move your mouse, run it, read the printed coordinates) to find these.

4. Run

bashpython bot.py

You have 5 seconds after starting to switch focus to the chat window.

Limitations & Risks


Coordinates are screen/resolution-specific. This breaks immediately if you resize the window, change DPI scaling, or switch monitors.
No multi-chat support. It only watches one fixed region — it won't notice messages in other conversations.
Fragile message detection. A vision model reading a screenshot to determine "whose message is last" can misfire on group chats, reactions, edited messages, or read receipts changing layout.
Polling, not event-driven. It screenshots every ~6–10 seconds regardless of activity, which is inefficient and adds reply latency.
Terms of Service risk. Automating replies on WhatsApp and Instagram via simulated input likely violates their Terms of Service and can get your account flagged or banned. Use at your own risk, ideally on a test account.
No conversation memory. Each reply is generated from a single message in isolation — the bot has no context of the earlier conversation.


Possible Improvements


Replace polling with OS-level change detection (e.g., compare screenshot hashes) to reduce unnecessary API calls.
Maintain a short rolling conversation history and pass it to the reply model for better context.
Add per-platform coordinate profiles (e.g., a PLATFORMS dict) so you can switch targets without editing constants.
Add error handling/retries around the Groq API calls — currently a network blip or rate limit will crash the loop.


License

MIT — use freely, no warranty.
