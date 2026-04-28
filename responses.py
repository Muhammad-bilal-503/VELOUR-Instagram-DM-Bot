"""
responses.py — VELOUR Brand Response Logic
-------------------------------------------
Contains all brand data and the keyword-matching engine.
get_response(text) is the only function called from app.py.

To upgrade to AI: replace get_response() with a Groq API call
while keeping all the brand data as the system prompt.
"""

# ─────────────────────────────────────────
# VELOUR BRAND DATA
# ─────────────────────────────────────────

PRODUCTS = """
🛍️ VELOUR — Product Prices:

• Oversized Tee      → PKR 1,800 – 2,200   (XS/S/M/L/XL/XXL)
• Ribbed Polo        → PKR 2,400 – 2,800   (S/M/L/XL)
• Washed Shorts      → PKR 2,200 – 2,600   (S/M/L/XL)
• Cargo Trousers     → PKR 3,500 – 4,500   (S/M/L/XL)
• Pullover Hoodie    → PKR 4,200 – 5,500   (S/M/L/XXL)
• Cord Jacket        → PKR 6,000 – 8,500   (M/L/XL)

Prices may vary by colour/fabric. DM @shopvelour for exact stock.
"""

SIZE_GUIDE = """
📏 VELOUR Size Guide:

Size  | Chest        | Waist
------+--------------+--------------
XS    | 32–34 inches | 24–26 inches
S     | 34–36 inches | 26–28 inches
M     | 36–38 inches | 28–30 inches
L     | 38–40 inches | 30–32 inches
XL    | 40–42 inches | 32–34 inches
XXL   | 42–44 inches | 34–36 inches

Tip: If you're between sizes, size up for an oversized fit 🙌
"""

DELIVERY_INFO = """
🚚 VELOUR Delivery Info:

• Lahore / Karachi / Islamabad → 2–3 working days
• All other cities              → 4–6 working days

Flat delivery charge: PKR 200
FREE delivery on orders above PKR 5,000 🎉

Orders are dispatched within 24 hours on business days.
"""

RETURNS_POLICY = """
🔄 VELOUR Returns & Exchanges:

• Exchange window: 7 days from delivery
• Item must be unworn with original tags attached
• Sale items are not eligible for exchange

To start an exchange, reply with your Order ID and we'll guide you through it ✅
"""

PAYMENT_METHODS = """
💳 VELOUR Payment Methods:

✅ JazzCash
✅ EasyPaisa
✅ Bank Transfer
✅ Cash on Delivery (COD)

COD is available in all major cities across Pakistan 🇵🇰
No extra charges on any payment method.
"""

NEW_ARRIVALS = """
🆕 VELOUR New Arrivals:

New collections drop every Friday 🔥

To never miss a drop:
→ Follow @shopvelour on Instagram
→ Turn on post notifications 🔔
→ DM us to join the WhatsApp broadcast for early access

Next drop coming soon — stay tuned!
"""

ORDER_STATUS = """
📦 VELOUR Order Tracking:

A tracking number is sent to you via WhatsApp or SMS after dispatch.

To get a status update, please share your Order ID and we'll check it for you right away! 🙏
"""

GREETING = """
👋 Hey! Welcome to VELOUR — Premium Clothing 🖤

I'm the VELOUR assistant. Here's what I can help you with:

1️⃣  Sizing & Measurements
2️⃣  Prices & Products
3️⃣  Delivery Info
4️⃣  Returns & Exchanges
5️⃣  Payment Methods
6️⃣  New Arrivals & Drops
7️⃣  Order Status / Tracking

Just ask your question in English or Urdu — I've got you! 😊
"""

FALLBACK = """
Thanks for reaching out to VELOUR! 🖤

I couldn't find an exact match for your question, but our team will get back to you shortly.

You can also:
→ DM us directly on Instagram: @shopvelour
→ Check our highlights for FAQs and size guides

We usually reply within a few hours ⚡
"""


# ─────────────────────────────────────────
# KEYWORD MAPS
# Each topic has a list of trigger keywords.
# Matching is case-insensitive (text is lowercased before checking).
# ─────────────────────────────────────────

KEYWORD_MAP = [
    (
        "greeting",
        # Use whole-word patterns to avoid matching "hi" inside words like "stitching"
        # We check these with word-boundary logic in get_response below
        ["hello", "hey", "salam", "assalam", "assalamu", "aoa", "good morning",
         "good evening", "good afternoon", "sup", "helo", "hii"],
        GREETING
    ),
    (
        "sizing",
        ["size", "sizing", "fit", "measurement", "measure", "xl", "xxl", "medium",
         "small", "large", "chest", "waist", "fitting", "size guide", "kitna size",
         "kaun sa size", "size chart", "bhejo size", "measurements"],
        SIZE_GUIDE
    ),
    (
        "pricing",
        ["price", "cost", "how much", "rate", "pkr", "rupee", "rupees", "kitna",
         "kitne", "dam", "daam", "paisa", "kitna paise", "charges", "fee", "amount",
         "expensive", "cheap", "affordable"],
        PRODUCTS
    ),
    (
        "returns",
        ["return", "exchange", "refund", "wrong size", "wapas", "replace",
         "replacement", "defect", "defective", "broken", "damaged", "wrong item",
         "not fitting", "want to return", "return policy", "exchange policy"],
        RETURNS_POLICY
    ),
    (
        "payment",
        ["jazzcash", "easypaisa", "easy paisa", "jazz cash",
         "cod", "cash on delivery", "bank transfer", "online payment", "kaise pay",
         "how to pay", "payment method", "payment", "debit", "credit"],
        PAYMENT_METHODS
    ),
    (
        "new_arrivals",
        ["new drop", "new collection", "new stock", "new arrival", "restock",
         "latest collection", "kab aayega", "when is next", "upcoming drop",
         "naya drop", "nayi collection", "naye kapre", "friday drop"],
        NEW_ARRIVALS
    ),
    # order_status BEFORE delivery so "track" hits order first
    (
        "order_status",
        ["track order", "order track", "order status", "where is my order",
         "mera order", "my order", "order id", "order number", "parcel",
         "not received", "not delivered", "kahan hai mera", "order kahan"],
        ORDER_STATUS
    ),
    (
        "delivery",
        ["deliver", "delivery", "shipping", "dispatch", "kitne din",
         "kab milega", "when will", "courier", "multan", "peshawar",
         "quetta", "lahore", "karachi", "islamabad", "city", "arrive",
         "arrival", "free delivery", "delivery charge"],
        DELIVERY_INFO
    ),
    (
        "new_arrivals_broad",
        ["new", "drop", "latest", "collection", "launch", "naya",
         "nayi", "naye", "upcoming", "notify", "notification", "alert", "update"],
        NEW_ARRIVALS
    ),
    (
        "payment_broad",
        ["pay", "card"],
        PAYMENT_METHODS
    ),
]

# Greeting uses whole-word matching to avoid "hi" inside words like "stitching"
GREETING_WHOLE_WORDS = ["hi", "hello", "hey", "hii", "helo", "sup", "aoa",
                         "salam", "assalam", "assalamu"]


# ─────────────────────────────────────────
# CORE MATCHING FUNCTION
# ─────────────────────────────────────────

def get_response(text: str) -> str:
    """
    Match incoming message text against keyword lists and return
    the appropriate VELOUR brand response.

    Greeting words use whole-word matching to avoid false positives
    (e.g. 'hi' inside 'stitching' should NOT trigger a greeting reply).

    Args:
        text: Raw message text from the customer

    Returns:
        A string reply to send back via the API
    """
    import re

    if not text or not text.strip():
        return FALLBACK

    lowered = text.lower().strip()

    # ── Greeting: whole-word match only ──────────────────────────────
    for word in GREETING_WHOLE_WORDS:
        # \b = word boundary — matches "hi" but not "stitching"
        if re.search(r'\b' + re.escape(word) + r'\b', lowered):
            print(f"[MATCH] Topic: 'greeting' | Keyword: {word!r}")
            return GREETING

    # ── All other topics: substring match ────────────────────────────
    for topic, keywords, response in KEYWORD_MAP:
        if topic == "greeting":
            continue  # Already handled above
        for keyword in keywords:
            if keyword in lowered:
                print(f"[MATCH] Topic: {topic!r} | Keyword: {keyword!r}")
                return response

    # Nothing matched — send the fallback
    print(f"[FALLBACK] No keyword matched for: {text!r}")
    return FALLBACK
