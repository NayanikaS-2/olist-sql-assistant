from google import genai

client = genai.Client()
for m in client.models.list():
    actions = getattr(m, "supported_actions", None) or []
    if not actions or "generateContent" in actions:
        print(m.name.replace("models/", ""))