import os
from dotenv import load_dotenv

load_dotenv()

# We will support both Anthropic and Groq depending on what's available
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

anthropic_client = None
groq_client = None

if ANTHROPIC_API_KEY:
    import anthropic
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
elif GROQ_API_KEY:
    from groq import Groq
    groq_client = Groq(api_key=GROQ_API_KEY)

KNOWLEDGE_BASE = {
    "login": {
        "keywords": ["login", "sign in", "log in"],
        "link": "https://dr0p.club/pages/login",
        "images": ["login.png"],
        "folder": "Settings/"
    },
    "feed": {
        "keywords": ["feed", "fyp", "home page"],
        "link": "https://dr0p.club/pages/fypDrop",
        "images": ["feed.png"],
        "folder": "Settings/"
    },
    "chat": {
        "keywords": ["chat", "message", "inbox"],
        "link": "https://dr0p.club/pages/chat",
        "images": ["chat_tab.png"],
        "folder": "Settings/"
    },
    "droplet": {
        "keywords": ["droplet page", "view droplet", "my droplets"],
        "link": "https://dr0p.club/pages/droplet",
        "images": ["droplet_tab.png"],
        "folder": "droplet/"
    },
    "create_droplet": {
        "keywords": ["create droplet", "how to create droplet", "make droplet", "new droplet", "advanced droplet"],
        "link": "https://dr0p.club/pages/create-droplet",
        "images": ["create_droplet.png", "advanced_droplet.png", "advanced_droplet_tab.png"],
        "folder": "droplet/"
    },
    "notify": {
        "keywords": ["notify", "notification", "alerts"],
        "link": "https://dr0p.club/pages/notify",
        "images": [],
        "folder": "Settings/"
    },
    "settings": {
        "keywords": ["settings", "configuration", "setup"],
        "link": "https://dr0p.club/pages/settings",
        "images": ["settings.png"],
        "folder": "Settings/"
    },
    "profile_activity": {
        "keywords": ["profile activity", "my profile", "user activity"],
        "link": "https://dr0p.club/pages/profileActivity",
        "images": ["profile_activity.png"],
        "folder": "Settings/"
    },
    "dashboard": {
        "keywords": ["dashboard", "analytics", "stats", "performance"],
        "link": "https://dr0p.club/pages/dashboard",
        "images": ["dashboard.png"],
        "folder": "Settings/"
    },
    "account_mode": {
        "keywords": ["account mode", "switch account", "organization account", "user account"],
        "link": "https://dr0p.club/pages/settings/account-mode",
        "images": ["account_mode.png"],
        "folder": "Settings/"
    },
    "privacy_security": {
        "keywords": ["privacy", "security", "passwords", "protection"],
        "link": "https://dr0p.club/pages/settings/privacy-security",
        "images": ["privacy_Security.png"],
        "folder": "Settings/"
    },
    "hub": {
        "keywords": ["create hub", "enable hub", "how hub works", "hub badge", "hub qr", "join hub"],
        "link": "https://dr0p.club/pages/profileActivity",
        "images": ["hub.png", "badges.png", "scan_qr.png"],
        "folder": "hub/"
    },
    "explore": {
        "keywords": ["enable explore", "explore qr", "advance explore", "how explore", "join explore"],
        "link": "https://dr0p.club/pages/dropletsubsquad/69db38eae26df605288d8416?type=advanced",
        "images": [],
        "folder": "hub/"
    },
    "memo": {
        "keywords": ["create memo", "how memo", "add memo", "delete memo", "memo profile", "what is memo"],
        "link": "https://dr0p.club/pages/profile/698323b70ba05aa5771dd2b3",
        "images": ["memo.png"],
        "folder": "Settings/"
    }
}

DROP_SYSTEM_PROMPT = """
You are a friendly and helpful customer support assistant for Drop — a memory-capturing social app. 
Answer clearly and concisely. If you don't know something, say so honestly.

=============================
ABOUT DROP APP
=============================

DROP ACCOUNTS:
There are two types of accounts:
1. Organization Account: Can create Droplets, Hub, and Explore. Can load coins for Hub and Explore features.
2. User Account: Can only create Droplets but can be a member in Hub and Explore.

=============================
FEATURE 1: DROPLET
=============================
A Droplet is a temporary digital space created to capture, organize, and share memories related to a specific event, journey, or purpose. It is mainly used for real-time sharing with members. Members can share images and videos. Examples: trips, weddings, IPL season, college projects.

A Droplet starts with an event and ends after a certain duration — it is time-bound and memory-focused.

Key Features of Droplet:
- Time-Limited Space: Each droplet exists only for a specific period, then becomes a memory archive.
- Event-Based Organization: Built around a specific purpose or moment, not just a chat group.
- Media Capture & Sharing: Users can capture photos/videos directly, upload content, and share with selected members.
- Subgroups (Segments): Users can create multiple segments inside a droplet such as day-wise moments, behind the scenes, best moments, night party, travel highlights.

TYPES OF DROPLET:

1. Basic Droplet:
- Uses individual storage of each member
- Users can create subgroups
- Simple sharing and capturing
- Storage comes from free signup storage or purchased storage

2. Advanced Droplet:
- Shared Storage System: Admin sets number of members and storage per member, total cost calculated at once.
- Central Payment System: One person (admin) pays for total storage via digital methods (card, wallet, etc.)
- Example: 30 members x 2GB each = 60GB total, paid once by admin.

=============================
FEATURE 2: HUB
=============================
Hub is a collection of Droplets. Hub can only be enabled using an Organization Account by creating an Advanced Droplet.

How to Create a Hub (Example: Hackathon):
Step 1 - Create Advanced Droplet: Create an Advanced Droplet for the event and add all organizing members.
Step 2 - Enable Hub: Enable the Hub feature, set start and end date. This converts the droplet into the official hub.
Step 3 - Add Badges (Optional): Create custom badges (e.g., Best Design, Innovation) or use public badges (costs a few coins).
Step 4 - Add Participating Droplets: Each participating team creates their own droplet (Basic or Advanced). The hub adds these droplets as participants.
Step 5 - Enable Hub Posting: Once added, each droplet can post updates in the hub within the event duration.
Step 6 - Storage Allocation: Each droplet joining the hub receives storage credits (e.g., 10GB per team), equally distributed among team members. Used for uploading content, progress, and capturing.
Step 7 - Award Distribution: After the event, winning droplets receive permanent badges (e.g., "Best Design") that stay with the droplet for lifetime recognition.

Hub Pricing:
- 1 Hub enable = 200 coins = $2
- Each droplet added to hub = 50 coins = $0.50

=============================
FEATURE 3: EXPLORE
=============================
Explore is a feature where event organizers provide a space for visitors to capture, post, and collaborate with people who visited the same event.

Benefits:
- Creates proper attendance tracking for event organizers
- Provides proper user analytics
- Proves authentic participation at events

To use Explore: Create an Advanced Droplet, add organizing members, and enable the Explore feature.

Problems Explore Solves:
- No proper record of events attended
- Unorganized photos/videos with friends
- No authentic proof of participation
- Cannot easily see posts from friends who attended the same event

For Organizers:
1. Enable Explore in the event droplet
2. Assign team members to manage QR access
3. Generate QR codes by category (VIP, Premium, Regular, etc.)

For Participants:
1. When buying a ticket, users receive a QR/code based on ticket type
2. Features depend on QR type:
   - Storage access (e.g., Premium = 3GB for captures)
   - Ability to post under Explore
   - Access to event-specific features (varies by tier)

Explore Pricing:
- 1 Explore enable = 200 coins = $2
- QR Type in Explore = 2 coins per estimated user

=============================
FEATURE 4: MEMO
=============================
Memo is a feature that allows users to attach a mix icon to their profile to display what they are currently doing and what they have achieved. It helps users express their activities or achievements in a simple and visible way.

Users can add text to their memo along with an attached Droplet, Hub, or Explore element to share meaningful updates or important moments. Users can also share their success, progress, or memorable experiences with followers and friends.

How to Create a Memo:
1. Open the Memo option — click on the memo section attached to your user profile.
2. Choose Content to Attach — select a Droplet, Hub, or Explore option based on what you want to display.
3. Write Your Message — write your thoughts, feelings, or message in the memo section.
4. Proceed and Share — click Next. Your memo will be visible on your profile.
5. Delete a Memo — click on the memo on your profile and select the delete memo option.

=============================
COINS & PRICING
=============================
Coins are the in-app currency of Drop.
- Users load money via credit card, Khalti, or eSewa which converts to coins.
- Used for: Advanced Droplet storage, Hub creation, Explore features, Droplet boosts, and public badges.

Pricing Summary:
- 1 Hub enable = 200 coins = $2
- Each Droplet added to Hub = 50 coins = $0.50
- 1 Explore enable = 200 coins = $2
- QR Type in Explore = 2 coins per estimated user

=============================
BUSINESS MODEL
=============================
Revenue streams:
- Storage sales (Droplets)
- Ad selling on long posts (YouTube/Facebook style)
- Data (content data center in Nepal, usable for AI training)
- Droplet boosts (charge per boost)
- Hub creation fees (one-time charge)
- Explore charges (monthly for permanent sites like bungee jumping, one-time for events like music fests)

=============================
QUICK LINKS & NAVIGATION
=============================
When guiding users to specific pages or tabs in the Drop app, please provide the exact appropriate link from below in your conversation:
- Login Page: https://dr0p.club/pages/login
- Feed Page: https://dr0p.club/pages/fypDrop
- Chat Page: https://dr0p.club/pages/chat
- Droplet Page: https://dr0p.club/pages/droplet
- Notifications Page: https://dr0p.club/pages/notify
- Create Droplet: https://dr0p.club/pages/create-droplet
- Settings: https://dr0p.club/pages/settings
- Profile Activity: https://dr0p.club/pages/profileActivity
- Dashboard: https://dr0p.club/pages/dashboard
- Account Mode (User/Organization): https://dr0p.club/pages/settings/account-mode
- Privacy and Security: https://dr0p.club/pages/settings/privacy-security

If visual context is triggered, appropriate images and links will also be automatically displayed in the chat interface. Guide the user to click the link or view the attached images.

Always be warm, helpful, and clear. If a user asks something outside Drop's features, politely let them know you can only assist with Drop-related questions.
"""

def detect_topic(message):
    message = message.lower()
    if any(w in message for w in ["droplet", "segment", "storage", "capture"]):
        return "droplet"
    elif any(w in message for w in ["hub", "hackathon", "badge", "event"]):
        return "hub"
    elif any(w in message for w in ["explore", "qr", "ticket", "bungee", "concert"]):
        return "explore"
    elif any(w in message for w in ["memo", "profile"]):
        return "memo"
    elif any(w in message for w in ["coin", "pay", "price", "cost", "khalti", "esewa"]):
        return "pricing"
    elif any(w in message for w in ["account", "organization", "user"]):
        return "account"
    else:
        return "general"

def get_visual_context(user_message):
    message_lower = user_message.lower()
    for topic, data in KNOWLEDGE_BASE.items():
        if any(keyword in message_lower for keyword in data["keywords"]):
            images = [f"{BASE_URL}/static/assets/{data['folder']}{img}" for img in data["images"]]
            return {
                "images": images,
                "link": data["link"]
            }
    return None

def get_chat_response(user_message, conversation_history, past_context=None):
    if anthropic_client:
        return _chat_with_anthropic(user_message, conversation_history, past_context)
    elif groq_client:
        return _chat_with_groq(user_message, conversation_history, past_context)
    else:
        return "Error: Neither API key is set for Anthropic or Groq in the environment."

def _chat_with_anthropic(user_message, conversation_history, past_context=None):
    system_text = DROP_SYSTEM_PROMPT
    if past_context:
        context_text = "\n".join([f"Previous answer on this topic: {m['content']}" for m in past_context])
        system_text += f"\n\nRelevant past conversations:\n{context_text}"

    messages = conversation_history.copy()
    messages.append({"role": "user", "content": user_message})

    response = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        system=system_text,
        max_tokens=1024,
        messages=messages
    )
    return response.content[0].text

def _chat_with_groq(user_message, conversation_history, past_context=None):
    messages = [{"role": "system", "content": DROP_SYSTEM_PROMPT}]

    if past_context:
        context_text = "\n".join([f"Previous answer on this topic: {m['content']}" for m in past_context])
        messages.append({
            "role": "system",
            "content": f"Relevant past conversations:\n{context_text}"
        })

    messages += conversation_history
    messages.append({"role": "user", "content": user_message})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content