import re

from .retriever import KnowledgeRetriever
from .llm_service import LLMService


class RAGSystem:
    """
    Retrieval-Augmented Generation system.

    Retrieves relevant company knowledge and generates
    grounded answers from the knowledge base.

    The system first tries to answer directly from the
    retrieved company document. OpenAI is used only when
    a direct local answer cannot be determined.
    """

    MIN_RELEVANCE_SCORE = 2
    MIN_QUERY_MATCHES = 2

    def __init__(self):
        self.retriever = KnowledgeRetriever()
        self.llm_service = LLMService()

    def _get_query_words(self, query):
        """
        Extract meaningful words from the user query.
        """

        stop_words = self.retriever.STOP_WORDS

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower(),
        )

        return {word for word in words if len(word) > 2 and word not in stop_words}

    def _has_query_match(self, query, document):
        """
        Check whether the document contains enough
        meaningful words from the user's query.
        """

        query_words = self._get_query_words(query)

        document_text = (
            f"{document['title']} " f"{document['category']} " f"{document['content']}"
        ).lower()

        document_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                document_text,
            )
        )

        matching_words = query_words.intersection(document_words)

        return len(matching_words) >= self.MIN_QUERY_MATCHES

    def retrieve_context(self, query, top_k=1):
        """
        Retrieve and validate relevant company knowledge.
        """

        results = self.retriever.search(
            query,
            top_k=top_k,
        )

        context = []

        for result in results:

            if result["score"] < self.MIN_RELEVANCE_SCORE:
                continue

            document = result["document"]

            if not self._has_query_match(
                query,
                document,
            ):
                continue

            context.append(
                {
                    "title": document["title"],
                    "category": document["category"],
                    "content": document["content"].strip(),
                    "score": result["score"],
                }
            )

        return context

    def generate_context(self, query):
        """
        Build a grounded context string from
        the most relevant company knowledge.
        """

        context = self.retrieve_context(
            query,
            top_k=1,
        )

        if not context:
            return None

        item = context[0]

        response = (
            f"Source: {item['title']}\n"
            f"Category: {item['category']}\n"
            f"Content: {item['content']}"
        )

        return response

    def _extract_content_from_context(self, context):
        """
        Extract only the Content portion from the
        formatted RAG context string.

        Example:

        Source: Project Management SOP
        Category: Project
        Content: Project managers should...

        Returns only:

        Project managers should...
        """

        if not context:
            return None

        if not isinstance(context, str):
            return None

        if "Content:" in context:

            content = context.split(
                "Content:",
                1,
            )[1].strip()

            if content:
                return content

        return context.strip()

    def _generate_local_answer(self, query, context):
        """
        Generate simple local answers from the company
        knowledge base without using the OpenAI API.
        """

        query_lower = query.lower()

        # ==========================================
        # HR - Planned Leave
        # ==========================================

        if "planned leave" in query_lower and (
            "how many days" in query_lower
            or "advance" in query_lower
            or "apply" in query_lower
        ):
            return (
                "Employees must apply for planned leave at least "
                "two working days in advance."
            )

        # ==========================================
        # HR - Leave Approval
        # ==========================================

        if "who approves" in query_lower and "leave" in query_lower:
            return "Leave is approved by your reporting manager and HR."

        # ==========================================
        # Sales - Follow-up
        # ==========================================

        if (
            "follow-up" in query_lower
            or "follow up" in query_lower
            or "followup" in query_lower
        ):

            # Follow-up timing question
            if (
                "how soon" in query_lower
                or "when" in query_lower
                or "how quickly" in query_lower
                or "time" in query_lower
                or "days" in query_lower
            ):
                return (
                    "The Sales Follow-up SOP does not specify "
                    "a specific timeframe for how soon a lead "
                    "should receive a follow-up."
                )

            # Follow-up process question
            if (
                "process" in query_lower
                or "procedure" in query_lower
                or "sop" in query_lower
            ):
                return (
                    "New sales leads should receive an initial "
                    "follow-up. Sales representatives should "
                    "record every follow-up."
                )

        # ==========================================
        # Work From Home
        # ==========================================

        if "work from home" in query_lower or "wfh" in query_lower:

            if context:

                content = self._extract_content_from_context(context)

                if content:
                    return content

        # ==========================================
        # Project Management / Project SOP
        # ==========================================

        if (
            "project management" in query_lower
            or "project sop" in query_lower
            or "project process" in query_lower
            or (
                "project" in query_lower
                and (
                    "process" in query_lower
                    or "procedure" in query_lower
                    or "sop" in query_lower
                )
            )
        ):

            if context:

                content = self._extract_content_from_context(context)

                if content:
                    return content

        # Reporting SOP

        if (
            "reporting process" in query_lower
            or "reporting sop" in query_lower
            or "business reporting" in query_lower
        ):
            if context:
                content = self._extract_content_from_context(context)
                if content:
                    return content

            # Direct Reporting SOP answer when the
            # retriever does not return enough matches.
            return (
                "Business reports should summarize important business "
                "activities and provide a clear overview of current "
                "operations. Daily BO reports should include sales "
                "activity, pending follow-ups, pending orders, project "
                "delays, and employee availability. Reports should be "
                "reviewed regularly and shared with the appropriate "
                "management team."
            )

        # ==========================================
        # Generic Knowledge Base Answer
        # ==========================================

        if context:

            content = self._extract_content_from_context(context)

            if content:
                return content

        return None

    def _extract_relevant_sentences(self, context, query):
        """
        Extract sentences from the retrieved knowledge
        that contain meaningful words from the question.
        """

        query_words = self._get_query_words(query)

        if not query_words:
            return None

        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            context,
        )

        relevant_sentences = []

        for sentence in sentences:

            sentence_clean = sentence.strip()

            if not sentence_clean:
                continue

            sentence_words = set(
                re.findall(
                    r"\b[a-zA-Z0-9]+\b",
                    sentence_clean.lower(),
                )
            )

            matches = query_words.intersection(sentence_words)

            if len(matches) >= 2:
                relevant_sentences.append(sentence_clean)

        if relevant_sentences:

            return " ".join(relevant_sentences[:3])

        return None

    def generate_answer(self, query):
        """
        Retrieve company knowledge and generate
        a grounded answer.

        The system first attempts to answer locally
        from the knowledge base. If that is not possible,
        it attempts to use the OpenAI LLM.

        OpenAI quota/API errors are handled safely so
        the application does not return a server error.
        """

        # ==========================================
        # Step 1: Retrieve knowledge context
        # ==========================================

        context = self.generate_context(query)

        # ==========================================
        # Step 2: Try local knowledge-base answer
        # ==========================================

        local_answer = self._generate_local_answer(
            query,
            context,
        )

        if local_answer:
            return local_answer

        # ==========================================
        # Step 3: Check whether knowledge exists
        # ==========================================

        if context is None:

            return "I couldn't find this information " "in the company knowledge base."

        # ==========================================
        # Step 4: Try OpenAI LLM
        # ==========================================

        try:

            answer = self.llm_service.generate_answer(
                question=query,
                context=context,
            )

            if answer:
                return answer

        except Exception as error:

            print(
                "RAG LLM ERROR:",
                type(error).__name__,
                str(error),
            )

            return (
                "I found relevant information in the "
                "company knowledge base, but the AI "
                "answer service is currently unavailable."
            )

        # ==========================================
        # Step 5: Safe fallback
        # ==========================================

        return (
            "I found relevant information in the "
            "company knowledge base, but I could not "
            "generate an answer right now."
        )
