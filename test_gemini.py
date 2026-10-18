from google import genai

client = genai.Client()
r = client.models.generate_content(model="gemini-flash-lite-latest", contents="Say hello in 3 words")
print(r.text)