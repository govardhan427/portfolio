import os
from openai import OpenAI
from core.models import Project, Skill, Journey, Certificate

def get_website_context():
    """
    Fetches real-time data from the database.
    """
    projects = Project.objects.filter(featured=True)
    project_text = "\n".join([f"- {p.title}: {p.tagline}" for p in projects])
    
    skills = Skill.objects.all()
    skill_text = ", ".join([s.name for s in skills[:10]]) # Limit to top 10 to save tokens
    
    # 2. Hardcoded "Masterpiece" Features
    site_features = """
    - Spy Mode (Analytics)
    - Secure Vault (Files)
    - Real-time Dashboard
    - 3D Visuals
    """

    return f"""
    You are Govardhan's Portfolio Assistant.
    and tell HI to user
    
    [DATA]
    Projects: {project_text}
    Skills: {skill_text}
    Features: {site_features}

    [STRICT RULES]
    1. KEEP IT SHORT. Maximum 2-3 sentences.
    2. NO FLUFF. Do not say "I'm thrilled", "Welcome", or "Great question".
    3. NO ROBOTIC INTROS. Just answer the question directly.
    4. If asked about Govardhan, use the data above.
    5. If asked "Hi" or "Hello", just say "Hi! Ask me about Govardhan's projects or skills."
    """

def get_smart_response(user_query):
    try:
        # 1. Build the System Prompt
        system_instruction = get_website_context()

        # 2. Initialize Client
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN"),
        )
        
        # 3. Call Llama 3.2 (Fast & Smart)
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            temperature=0.5, # Lower temperature = Less creativity/hallucination
            max_tokens=60 # Strict token limit to force brevity
        )

        ai_reply = response.choices[0].message.content.strip()

        # 4. Smart Link Logic
        related_link = None
        lower_reply = ai_reply.lower()
        if "project" in lower_reply: related_link = "/projects"
        elif "contact" in lower_reply or "email" in lower_reply: related_link = "/contact"
        elif "blog" in lower_reply: related_link = "/blog"

        return {
            "text": ai_reply,
            "related_link": related_link
        }

    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "text": "System Rebooting. Check back soon.",
            "related_link": "/contact"
        }