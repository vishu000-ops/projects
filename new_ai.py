import os
import math
import threading
import tkinter as tk
import customtkinter as ctk
import pyttsx3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------- CONFIG ----------
ctk.set_appearance_mode("dark")

BG = "#050b16"
PANEL = "#0b1628"
CYAN = "#00d9ff"
BLUE = "#087cff"
TEXT = "#e4f3ff"

MODEL = "gemini-3.1-flash-lite"
key = os.getenv("GOOGLE_API_KEY")

client = OpenAI(
    api_key=key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
) if key else None

app = ctk.CTk()
app.title("ULTRON | AI COMMAND CENTER")
app.geometry("1150x720")
app.minsize(850, 560)
app.configure(fg_color=BG)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# ---------- SIDEBAR ----------
side = ctk.CTkFrame(app, width=205, corner_radius=0,
                    fg_color="#07101f")
side.grid(row=0, column=0, sticky="nsew")
side.grid_propagate(False)

ctk.CTkLabel(
    side, text="◈ ULTRON",
    font=("Consolas", 27, "bold"),
    text_color=CYAN
).pack(pady=(35, 3))

ctk.CTkLabel(
    side, text="AI COMMAND CENTER",
    font=("Consolas", 10), text_color="#7996b7"
).pack(pady=(0, 35))

def section(text):
    ctk.CTkLabel(
        side, text=text, anchor="w",
        font=("Consolas", 12, "bold"),
        text_color="#6386aa"
    ).pack(fill="x", padx=20, pady=(15, 8))

section("NAVIGATION")

for name in ["⌂   Dashboard", "◉   AI Chat",
             "♬   Voice Assistant", "⚙   Settings"]:
    ctk.CTkButton(
        side, text=name, anchor="w", height=42,
        fg_color="transparent", hover_color="#102b46",
        text_color=TEXT, font=("Segoe UI", 13),
        command=lambda n=name: status.configure(
            text="● " + n.split("   ")[-1].upper()
        )
    ).pack(fill="x", padx=12, pady=3)

section("SYSTEM")

status = ctk.CTkLabel(
    side, text="● SYSTEM ONLINE",
    text_color="#28e7b5", font=("Consolas", 12)
)
status.pack(anchor="w", padx=18, pady=8)

ctk.CTkLabel(
    side, text="GEMINI CORE\nVOICE ENGINE\nPYTHON SYSTEM",
    justify="left", text_color="#6482a3",
    font=("Consolas", 11)
).pack(side="bottom", anchor="w", padx=20, pady=25)

# ---------- MAIN PANEL ----------
main = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
main.grid(row=0, column=1, sticky="nsew", padx=18, pady=16)
main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=1)

header = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=12)
header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
header.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    header, text="ULTRON AI / INTERFACE",
    font=("Consolas", 19, "bold"), text_color=CYAN
).grid(row=0, column=0, sticky="w", padx=18, pady=17)

ctk.CTkLabel(
    header, text="GEMINI CONNECTED  ◉",
    font=("Consolas", 11), text_color="#28e7b5"
).grid(row=0, column=1, padx=18)

# Two-column workspace
workspace = ctk.CTkFrame(main, fg_color="transparent")
workspace.grid(row=1, column=0, sticky="nsew")
workspace.grid_columnconfigure(0, weight=3)
workspace.grid_columnconfigure(1, weight=2)
workspace.grid_rowconfigure(0, weight=1)

# ---------- CHAT ----------
chat_panel = ctk.CTkFrame(workspace, fg_color=PANEL, corner_radius=15)
chat_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
chat_panel.grid_columnconfigure(0, weight=1)
chat_panel.grid_rowconfigure(1, weight=1)

ctk.CTkLabel(
    chat_panel, text="◈  CONVERSATION LOG",
    text_color=CYAN, font=("Consolas", 13, "bold")
).grid(row=0, column=0, sticky="w", padx=15, pady=15)

chat = ctk.CTkScrollableFrame(
    chat_panel, fg_color="#07111f", corner_radius=10
)
chat.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
chat.grid_columnconfigure(0, weight=1)

def add_message(sender, message):
    color = CYAN if sender == "ULTRON" else "#a5b4fc"

    bubble = ctk.CTkFrame(
        chat, fg_color="#12243a", corner_radius=10
    )
    bubble.pack(fill="x", padx=5, pady=6)

    ctk.CTkLabel(
        bubble, text=sender, text_color=color,
        font=("Consolas", 11, "bold")
    ).pack(anchor="w", padx=12, pady=(8, 2))

    ctk.CTkLabel(
        bubble, text=message, text_color=TEXT,
        font=("Segoe UI", 12), wraplength=380,
        justify="left", anchor="w"
    ).pack(fill="x", padx=12, pady=(2, 10))

# ---------- ANIMATED CORE ----------
visual = ctk.CTkFrame(workspace, fg_color=PANEL, corner_radius=15)
visual.grid(row=0, column=1, sticky="nsew")
visual.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    visual, text="NEURAL CORE",
    font=("Consolas", 14, "bold"), text_color=CYAN
).pack(pady=(18, 4))

canvas = tk.Canvas(
    visual, width=280, height=280,
    bg=PANEL, highlightthickness=0
)
canvas.pack(fill="x", padx=5, pady=5)

angle = 0
core_active = True

def animate():
    global angle
    canvas.delete("all")

    w = max(canvas.winfo_width(), 240)
    h = max(canvas.winfo_height(), 240)
    cx, cy = w / 2, h / 2
    radius = min(w, h) * 0.35

    # Concentric energy rings
    for i in range(4):
        r = radius - i * 13
        canvas.create_oval(
            cx-r, cy-r, cx+r, cy+r,
            outline=CYAN if i % 2 == 0 else BLUE,
            width=2
        )

    # Orbiting energy particles
    for i in range(12):
        a = math.radians(angle + i * 30)
        x = cx + radius * math.cos(a)
        y = cy + radius * math.sin(a)
        canvas.create_oval(
            x-3, y-3, x+3, y+3,
            fill=CYAN, outline=""
        )

    # Central AI core
    pulse = 35 + 4 * math.sin(math.radians(angle * 3))
    canvas.create_oval(
        cx-pulse, cy-pulse, cx+pulse, cy+pulse,
        fill="#102e51", outline=CYAN, width=3
    )
    canvas.create_text(
        cx, cy, text="AI", fill="white",
        font=("Consolas", 24, "bold")
    )

    angle = (angle + 3) % 360
    app.after(40, animate)

ctk.CTkLabel(
    visual, text="● CORE ACTIVE",
    text_color="#28e7b5", font=("Consolas", 12)
).pack(pady=8)

ctk.CTkLabel(
    visual, text="INTELLIGENCE SYSTEM",
    text_color="#7996b7", font=("Consolas", 10)
).pack(pady=3)

# ---------- INPUT ----------
bottom = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=12)
bottom.grid(row=2, column=0, sticky="ew", pady=(14, 0))
bottom.grid_columnconfigure(0, weight=1)

entry = ctk.CTkEntry(
    bottom, height=46,
    placeholder_text="Enter a command for ULTRON...",
    fg_color="#091322", border_color="#16476a",
    text_color=TEXT
)
entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# ---------- VOICE + AI ----------
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Voice error:", e)

def request_ai(question):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are ULTRON, a helpful AI assistant."
                },
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        if not answer:
            answer = "The AI returned an empty response."

        app.after(0, display_answer, answer)

    except Exception as e:
        app.after(0, display_error, str(e))

def display_answer(answer):
    add_message("ULTRON", answer)
    status.configure(text="● SYSTEM ONLINE", text_color="#28e7b5")
    send.configure(state="normal", text="SEND")

    threading.Thread(
        target=speak, args=(answer,), daemon=True
    ).start()

def display_error(error):
    add_message("SYSTEM", error)
    status.configure(text="● CONNECTION ERROR", text_color="#ff657a")
    send.configure(state="normal", text="SEND")

def send_message(event=None):
    question = entry.get().strip()
    if not question:
        return

    if client is None:
        add_message(
            "SYSTEM",
            "API key missing. Set the GEMINI_API_KEY environment variable."
        )
        return

    entry.delete(0, "end")
    add_message("YOU", question)
    status.configure(text="● PROCESSING", text_color="#ffd166")
    send.configure(state="disabled", text="WAIT")

    threading.Thread(
        target=request_ai, args=(question,), daemon=True
    ).start()

send = ctk.CTkButton(
    bottom, text="SEND  ➤", width=105, height=44,
    fg_color="#087cff", hover_color="#0054b8",
    font=("Consolas", 12, "bold"),
    command=send_message
)
send.grid(row=0, column=1, padx=(0, 10), pady=10)

entry.bind("<Return>", send_message)

add_message(
    "ULTRON",
    "Neural core initialized. Systems ready. "
    "Enter a command to begin."
)

animate()
entry.focus()
app.mainloop()
