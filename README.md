# VELOUR Instagram DM Bot 🖤
**Automated Instagram DM replies for VELOUR — Premium Clothing**  
Built with Python 3 + Flask + Meta Graph API (Instagram Messenger API)

---

## Team Members
| Name | Role |
|------|------|
| M Bilal | Setup |
| Ali Ahmad | Backend |
| Tayyeb | Logic |
| Marwa | API |
| Junaid | Documentation & Testing |
| Abusalam | Deployment |

---

## What This Bot Does
A customer sends a DM to the VELOUR Instagram account → Meta forwards it to this Flask server via a webhook → the bot matches keywords and sends back the right reply automatically.

**Topics the bot handles:**
- Greeting / welcome
- Product prices
- Size guide
- Delivery info
- Returns & exchanges
- Payment methods
- New arrivals
- Order tracking
- Fallback for anything unrecognised

---

## Project Structure
```
velour-bot/
├── app.py               ← Flask server + webhook routes (main file)
├── responses.py         ← Keyword matching logic + all brand data
├── responses_groq.py    ← AI version using Groq LLaMA 3 (optional upgrade)
├── requirements.txt     ← Python dependencies
├── .env.example         ← Template for your secret tokens
├── .env                 ← YOUR actual secrets (never commit this)
├── .gitignore           ← Keeps .env out of GitHub
└── README.md            ← This file
```

---

## Step-by-Step Setup

### STEP 1 — Prerequisites (do this first)
Before writing any code, make sure you have:
- [ ] Python 3.8 or later installed
- [ ] pip installed (comes with Python)
- [ ] A **Facebook Developer account** — free at developers.facebook.com
- [ ] An **Instagram Business or Creator account** (personal accounts do NOT work)
- [ ] A **Facebook Page** connected to your Instagram account
- [ ] A free **ngrok account** at ngrok.com

---

### STEP 2 — Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

---

### STEP 3 — Create Your .env File
Copy the example file and fill in your tokens:
```bash
# On Windows:
copy .env.example .env

# On Mac/Linux:
cp .env.example .env
```
Then open `.env` and fill in your values (instructions in next steps).

---

### STEP 4 — Meta App Setup

#### 4a. Create a Meta Developer App
1. Go to **developers.facebook.com** and log in
2. Click **My Apps → Create App**
3. Choose **Business** as app type
4. Name it (e.g. `VELOUR Bot`), enter email, click Create
5. Inside the dashboard, find **Messenger** under Add Products and click **Set Up**

#### 4b. Connect Your Instagram Account
1. In Messenger settings, open the **Instagram** tab
2. Click **Add or Remove Instagram Accounts**
3. Select your VELOUR Instagram Business account
4. Authorize it

#### 4c. Generate Access Token
1. In Messenger settings → **Access Tokens**
2. Click **Generate Token** next to your account
3. Copy the token
4. Paste it in your `.env` file as `ACCESS_TOKEN`

> ⚠️ **Security:** Never paste your token directly in any Python file. Keep it only in `.env`.

---

### STEP 5 — Choose Your VERIFY_TOKEN
This is just any string YOU decide — like a password for your webhook.
Example: `velour_secret_2024`

Add it to your `.env` file as `VERIFY_TOKEN`.  
You will use this exact same string in the Meta dashboard in Step 7.

---

### STEP 6 — Run the Flask Server
In your terminal:
```bash
python app.py
```
You should see:
```
* Running on http://127.0.0.1:5000
```
Visit **http://localhost:5000** in your browser — you should see:
```json
{"status": "running", "bot": "VELOUR Instagram DM Bot"}
```

---

### STEP 7 — Start ngrok (in a second terminal)
ngrok creates a public URL pointing to your local Flask server.

```bash
ngrok http 5000
```

You will see something like:
```
Forwarding   https://abc123.ngrok-free.app → http://localhost:5000
```

Copy that `https://` URL — you need it for the next step.

> 💡 **Note:** Free ngrok gives a new URL every time you restart it. Update the Meta webhook URL each time.

---

### STEP 8 — Register Webhook in Meta

1. Go to your Meta App → **Messenger → Webhooks**
2. Click **Add Callback URL**
3. Paste your ngrok URL with `/webhook` added at the end:
   ```
   https://abc123.ngrok-free.app/webhook
   ```
4. In **Verify Token**, type the exact same string you put in `.env` as `VERIFY_TOKEN`
5. Click **Verify and Save**
6. Under **Webhook Fields**, subscribe to the **messages** event

If verification passes ✅ you are connected. If it fails, check that:
- Flask is still running
- ngrok is still running
- `VERIFY_TOKEN` in `.env` matches exactly what you typed in Meta

---

### STEP 9 — Test the Bot
Send a DM to your Instagram account from a different account and watch your terminal.

**Test messages to try:**

| Send This | Should Get |
|-----------|-----------|
| `Hello` | Welcome message with menu |
| `hoodie ka price kya hai` | Pricing with all products |
| `size guide bhejo` | Full size chart |
| `do you deliver to Multan` | Delivery times + charges |
| `I want to return my order` | Returns policy |
| `can I pay with JazzCash` | Payment methods |
| `koi naya drop aya hai` | New arrivals info |
| `where is my parcel` | Ask for order ID |
| `do you do custom stitching` | Fallback message |

---

## Optional — Upgrade to AI Replies (Groq)

Once the keyword version is working, you can upgrade to real AI responses.

#### Get Free Groq API Key
1. Sign up free at **console.groq.com** (no credit card needed)
2. Create an API key
3. Add it to `.env` as `GROQ_API_KEY`

#### Switch to AI Mode
In `app.py`, find this line:
```python
from responses import get_response
```
Change it to:
```python
from responses_groq import get_response
```

That's it. Everything else stays the same. The AI handles Urdu + English naturally.

---

## Submission Checklist
- [ ] Code pushed to **public GitHub repo**
- [ ] `.env` is **NOT visible** anywhere in the repo
- [ ] `.env` is listed in `.gitignore`
- [ ] Short **screen recording** showing one complete DM flow (send → webhook → reply)
- [ ] README is complete

---

## Useful Links
| Resource | Link |
|----------|------|
| Meta IG Messaging Docs | https://developers.facebook.com/docs/messenger-platform/instagram |
| Meta Webhooks Reference | https://developers.facebook.com/docs/graph-api/webhooks |
| Flask Docs | https://flask.palletsprojects.com |
| Groq Free API | https://console.groq.com |
| ngrok Download | https://ngrok.com/download |
