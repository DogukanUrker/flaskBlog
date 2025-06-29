"""
This module contains the function to calculate the estimated reading time in minutes for a given post content.
"""

from re import sub  # Importing sub function from re module


# Calculate the estimated reading time in minutes for a given post content.
def calculateReadTime(content):
    """Calculate the estimated reading time in minutes for a given post content."""
    # Remove HTML tags if any
    cleanText = sub(r"<[^>]+>", "", content)

    # Count words (average reading speed is ~200 words per minute)
    wordCount = len(cleanText.split())
    readingTime = max(1, round(wordCount / 200))

    return readingTime
