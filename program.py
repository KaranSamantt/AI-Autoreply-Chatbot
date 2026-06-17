import pyautogui
import pyperclip
import time
import base64
import io
from groq import Groq

client = Groq(api_key="YOUR API KEY HERE")
pyautogui.FAILSAFE = False

# --- CONFIG ---
CHAT_REGION = (708, 165, 1857, 917)
INPUT_BOX   = (1181, 968)
SEND_BTN    = (1863, 965)
# --------------

last_replied_to = ""
replied_this_cycle = False

print("Starting in 5 seconds...")
time.sleep(5)


def capture_screenshot_base64(region):
    x1, y1, x2, y2 = region
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def analyze_chat(image_b64):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"}
                    },
                    {
                        "type": "text",
                        "text": (
                            "This is a chat screenshot.\n"
                            "Find the LAST message from the OTHER person (not me).\n"
                            "If the last message is MINE → say: NO_REPLY\n"
                            "If the last message is THEIRS → return ONLY their exact word-for-word message text. Nothing added, nothing removed.\n"
                            "Do not translate. Do not summarize. Do not explain."
                        )
                    }
                ]
            }
        ],
        temperature=0.0,
        max_tokens=100
    )

    result = response.choices[0].message.content.strip()
    if not result or result == "NO_REPLY":
        return None, False
    return result, True


def generate_reply(incoming_message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Karan, a 22 year old Indian guy chatting on WhatsApp/Instagram.\n"
                    "Rules:\n"
                    "- MOST IMPORTANT: Reply ONLY to exactly what they said. Do not assume, add context, or go off-topic.\n"
                    "- If they ask a question, answer it directly and briefly.\n"
                    "- If they make a statement, react to that statement only.\n"
                    "- Never bring up new topics.\n"
                    "- Write in Hinglish (Hindi + English mixed naturally)\n"
                    "- Use 1-2 relevant emojis that match the emotion\n"
                    "- Max 1 sentence. Sometimes just 2-4 words is enough\n"
                    "- Always lowercase. No full stops.\n"
                    "- Be emotionally reactive: laugh when funny, curious when questioned, chill otherwise\n"
                    "- Use fillers naturally: haha, arre, yaar, bhai, lol, haan, achha\n"
                    "- Never sound formal, helpful, or robotic\n"
                    "- Example replies:\n"
                    "  'haha bhai ye toh sahi hai 😂'\n"
                    "  'arre yaar kya baat hai 🔥'\n"
                    "  'haan haan pata hai 😭'\n"
                    "  'kya? sach mein? 😭'\n"
                    "  'lol same yaar 💀'\n"
                    "  'achha okay 👍'\n"
                )
            },
            {
                "role": "user",
                "content": f"They said: \"{incoming_message}\"\nReply as Karan:"
            }
        ],
        temperature=1.0,
        max_tokens=50
    )
    return response.choices[0].message.content.strip()


def send_message(text):
    pyautogui.click(*INPUT_BOX)
    time.sleep(0.4)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.click(*SEND_BTN)


while True:
    print("Capturing screen...")
    img_b64 = capture_screenshot_base64(CHAT_REGION)
    incoming, should_reply = analyze_chat(img_b64)
    print(f"Detected: {incoming!r}")

    if should_reply and incoming != last_replied_to and not replied_this_cycle:
        last_replied_to = incoming
        replied_this_cycle = True

        reply = generate_reply(incoming)
        print(f"Replying: {reply}")
        send_message(reply)
        print("Sent!")
        time.sleep(4)

    else:
        print("No new message or already replied.")
        replied_this_cycle = False

    time.sleep(6)