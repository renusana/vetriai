from django.conf import settings
from openai import OpenAI


class LLMService:
    """
    Service responsible for generating natural-language
    answers using an OpenAI LLM.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_answer(self, question, context):
        """
        Generate an answer using the user's question
        and retrieved company knowledge.
        """

        prompt = f"""
You are a helpful company AI assistant.

Answer the user's question using ONLY the company
knowledge provided below.

If the answer cannot be found in the provided
company knowledge, say that the information is
not available in the company knowledge base.

Company Knowledge:
{context}

User Question:
{question}

Provide a clear and concise answer.
"""

        response = self.client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )

        return response.output_text
