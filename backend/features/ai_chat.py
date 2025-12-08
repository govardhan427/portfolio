import os
import re
from django.core.cache import cache  # Better than lru_cache for Django
from openai import OpenAI
from core.models import Project, Skill, Journey, Certificate

# -------------------------------------------
# 1. GLOBAL CLIENT (Initialize once, reuse forever)
# -------------------------------------------
# This prevents reconnecting to Hugging Face on every single request.
try:
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_TOKEN"),
    )
except Exception:
    client = None  # Handle missing key gracefully

# -------------------------------------------
# 2. SMART CONTEXT CACHING (Auto-updates)
# -------------------------------------------
def get_website_context():
    """
    Fetches portfolio data. Uses Django's cache so it auto-refreshes
    every 15 minutes (900s), ensuring new projects appear without restarting server.
    """
    cached_context = cache.get("ai_website_context")
    if cached_context:
        return cached_context

    # -- Fetch Data --
    projects = Project.objects.all()
    # optimized list comprehension
    proj_list = [
        f"- {p.title}: {p.tagline} (Stack: {', '.join([s.name for s in p.skills.all()[:5]])})" 
        for p in projects
    ]
    project_text = "\n".join(proj_list) if proj_list else "No projects listed yet."

    skills = Skill.objects.all()
    skill_text = ", ".join([s.name for s in skills]) or "No skills listed."

    certs = Certificate.objects.all()
    cert_text = ", ".join([c.name for c in certs]) or "No certificates."

    site_features = """
    - Spy Mode (Analytics)
    - Secure Vault (Files)
    - Real-time Dashboard
    - 3D Visuals
    """

    # -- Build Prompt --
    prompt = f"""
    You are Govardhan's Portfolio Assistant.

    [REAL-TIME DATA]
    Projects: {project_text}
    Skills: {skill_text}
    Certificates: {cert_text}
    Features: {site_features}

    [STRICT GUIDELINES]
    1. BRIEF: Max 2-3 sentences.
    2. TONE: Professional, confident, slightly witty.
    3. NO FLUFF: Skip "I'd be happy to help". Just answer.
    4. GREETING: If user says "Hi/Hello", reply: "Hi! I know everything about Govardhan's work. What do you need?"
    5. DATA: Only use the data provided above.
    """
    
    # Cache this string for 15 minutes
    cache.set("ai_website_context", prompt, timeout=900)
    return prompt

# -------------------------------------------
# 3. ROBUST SENTENCE TRIMMER
# -------------------------------------------
def enforce_length(text, max_sentences=3):
    """
    Trims text intelligently. Avoids splitting on abbreviations like 'v1.0' or 'Node.js'.
    """
    # Regex splits by punctuation followed by a space or end of string
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) > max_sentences:
        return " ".join(sentences[:max_sentences])
    return text

# -------------------------------------------
# 4. SMART LINK ROUTING
# -------------------------------------------
def detect_link(reply):
    reply_lower = reply.lower()
    
    # Priority Order Matters!
    keyword_map = {
        "/projects": ["project", "app", "website", "case study", "built"],
        "/skills":   ["skill", "technology", "stack", "python", "react", "django"],
        "/blog":     ["blog", "article", "writing", "read"],
        "/contact":  ["contact", "email", "hire", "reach out", "message"],
    }

    for link, keywords in keyword_map.items():
        if any(k in reply_lower for k in keywords):
            return link
    return None

# -------------------------------------------
# 5. MAIN LOGIC
# -------------------------------------------
def get_smart_response(user_query):
    # 1. Fast Greeting Check (Save API Cost)
    clean_query = user_query.strip().lower()
    if clean_query in ["hi", "hello", "hey", "hola"]:
        return {
            "text": "Hi! I know everything about Govardhan's work. Ask me about his projects or skills.",
            "related_link": None
        }

    # 2. Safety Check
    if not client:
        return {"text": "AI brain missing (Check HF_TOKEN).", "related_link": "/contact"}

    try:
        # 3. Generate Response
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=[
                {"role": "system", "content": get_website_context()},
                {"role": "user", "content": user_query},
            ],
            temperature=0.6,    # Lower = More factual
            max_tokens=150,     # Hard limit prevents rambling
            top_p=0.9
        )

        ai_reply = response.choices[0].message.content.strip()
        
        # 4. Post-Processing
        final_text = enforce_length(ai_reply)
        link = detect_link(final_text)

        return {
            "text": final_text,
            "related_link": link
        }

    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "text": "I'm having a brief hiccup. Please ask again in a moment.",
            "related_link": "/contact"
        }