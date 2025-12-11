"""
FAQ/Knowledge Base helper functions with 90% word overlap search.
"""
import re
from .models import FAQEntry


def tokenize(text):
    """Split text into lowercase words, removing punctuation."""
    return set(re.findall(r'\b\w+\b', text.lower()))


def search_entries(query):
    """
    Search FAQ entries by 90% word overlap.
    Returns entries where ≥90% of query words appear in the question.
    """
    if not query or not query.strip():
        return FAQEntry.objects.none()
    
    query_words = tokenize(query)
    if not query_words:
        return FAQEntry.objects.none()
    
    threshold = 0.9
    results = []
    
    for entry in FAQEntry.objects.all():
        question_words = tokenize(entry.question)
        matches = query_words & question_words
        overlap = len(matches) / len(query_words) if query_words else 0
        
        if overlap >= threshold:
            results.append(entry)
    
    return results


def create_entry(question, answer, author=None):
    """Create a new FAQ entry."""
    return FAQEntry.objects.create(
        question=question,
        answer=answer,
        author=author
    )
