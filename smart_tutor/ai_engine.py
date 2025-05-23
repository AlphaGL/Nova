from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generateChatResponse(prompt):
    messages = [
        {"role": "system", "content": "Your name is Karabo. You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message.content.replace('\n', '<br>')
    except Exception as e:
        print("OpenAI API error:", e)
        answer = 'Oops! You beat the AI. Try a different question. If the problem persists, come back later.'
    return answer



# key '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'