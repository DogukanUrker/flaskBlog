"""
This module contains the function to calculate the estimated reading time in minutes for a given post content.
"""

from re import sub


def calculateReadTime(content):
    """Calculate the estimated reading time in minutes for a given post content."""

    cleanText = sub(r"<[^>]+>", "", content)

    wordCount = len(cleanText.split())
    readingTime = max(1, round(wordCount / 200))

    return readingTime
