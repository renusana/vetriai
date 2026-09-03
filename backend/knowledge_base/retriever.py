import re

from .documents import DOCUMENTS


class KnowledgeRetriever:
    """
    Retrieves relevant documents from the knowledge base
    using keyword-based relevance scoring.
    """

    STOP_WORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "can",
        "do",
        "for",
        "from",
        "give",
        "how",
        "i",
        "in",
        "is",
        "it",
        "me",
        "of",
        "on",
        "or",
        "should",
        "the",
        "to",
        "what",
        "when",
        "who",
        "why",
        "with",
    }

    # Generic words that are too common to prove
    # that a document is actually relevant.

    GENERIC_WORDS = {
        "company",
        "employee",
        "employees",
        "policy",
        "request",
        "requests",
        "work",
        "leave",
        "manager",
        "information",
        "process",
        "days",
    }

    def __init__(self):
        self.documents = DOCUMENTS

    def _tokenize(self, text):
        """
        Convert text into meaningful lowercase words.
        """

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )

        return {word for word in words if len(word) > 2 and word not in self.STOP_WORDS}

    def _has_specific_match(self, query_words, document):
        """
        Check whether the document contains at least
        one specific (non-generic) query word.
        """

        specific_words = {
            word for word in query_words if word not in self.GENERIC_WORDS
        }

        if not specific_words:
            return False

        document_text = (
            f"{document['title']} " f"{document['category']} " f"{document['content']}"
        ).lower()

        document_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                document_text,
            )
        )

        return bool(specific_words.intersection(document_words))

    def search(self, query, top_k=3):
        """
        Search the knowledge base and rank documents
        based on relevance.
        """

        query_words = self._tokenize(query)

        if not query_words:
            return []

        results = []

        for document in self.documents:

            # Ignore documents that do not contain
            # any specific query word.
            if not self._has_specific_match(
                query_words,
                document,
            ):
                continue

            title = document["title"].lower()
            category = document["category"].lower()
            content = document["content"].lower()

            title_words = self._tokenize(title)
            category_words = self._tokenize(category)
            content_words = self._tokenize(content)

            score = 0

            for word in query_words:

                # Specific words receive higher importance.
                if word in self.GENERIC_WORDS:
                    weight = 1
                else:
                    weight = 4

                # Title matches are highly relevant.
                if word in title_words:
                    score += weight * 2

                # Category matches are also important.
                if word in category_words:
                    score += weight

                # Content matches.
                if word in content_words:
                    score += weight

            # Exact phrase match gets an additional score.
            query_text = query.lower().strip()

            if query_text and query_text in title:
                score += 5

            if query_text and query_text in content:
                score += 3

            if score > 0:
                results.append(
                    {
                        "document": document,
                        "score": score,
                    }
                )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results[:top_k]
