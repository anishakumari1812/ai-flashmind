"""
utils/llm.py – LLM integration for FlashMind AI.
Uses Groq API (FREE) — runs Llama 3 at ultra-fast speed.
Get free API key at: https://console.groq.com
"""

import os
import json
import re
from typing import List, Dict
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Prompt ─────────────────────────────────────────────────────────────────────
FLASHCARD_SYSTEM_PROMPT = """
You are FlashMind AI, an expert educational assistant that creates high-quality study flashcards.

Read the study material and generate between 5 and 10 flashcards.

STRICT RULES:
1. Return ONLY a valid JSON array — no markdown, no backticks, no explanation.
2. Each item must have exactly two keys: "question" and "answer".
3. Answers should be 1-3 sentences, clear and complete.
4. Focus on key concepts, definitions, dates, and important relationships.

Output format (follow exactly):
[
  {"question": "...", "answer": "..."},
  {"question": "...", "answer": "..."}
]
"""


def generate_flashcards(text: str) -> List[Dict[str, str]]:
    """Generate flashcards using Groq API (Free tier)."""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Groq API key not found. "
            "Get a FREE key at https://console.groq.com → API Keys. "
            "Then set GROQ_API_KEY in your .env file."
        )

    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError("Run: pip install groq")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Free, fast, very capable
        messages=[
            {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
            {"role": "user",   "content": f"Study material:\n\n{text}"},
        ],
        temperature=0.4,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()
    return _parse_flashcards(raw)


def _parse_flashcards(raw: str) -> List[Dict[str, str]]:
    """Safely parse JSON array from model response."""
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()

    match = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("The AI returned an unexpected format. Please try again.")

    if not isinstance(data, list):
        raise RuntimeError("Expected a JSON array of flashcards.")

    valid = [
        {
            "question": str(item["question"]).strip(),
            "answer":   str(item["answer"]).strip(),
        }
        for item in data
        if isinstance(item, dict) and "question" in item and "answer" in item
    ]

    if not valid:
        raise RuntimeError("No valid flashcards found in AI response.")

    return valid[:10]


def generate_flashcards_demo(text: str) -> List[Dict[str, str]]:
    """Sample flashcards shown when no API key is set."""
    return [
        {
            "question": "What is FlashMind AI?",
            "answer": "FlashMind AI converts your notes or PDFs into smart study flashcards using Groq + Llama 3 AI.",
        },
        {
            "question": "How do you enable AI flashcard generation?",
            "answer": "Get a free API key from https://console.groq.com and set GROQ_API_KEY in your .env file.",
        },
        {
            "question": "What input formats does FlashMind AI support?",
            "answer": "You can paste text directly or upload a PDF for automatic text extraction.",
        },
        {
            "question": "How many flashcards are generated per session?",
            "answer": "Between 5 and 10 flashcards focusing on the most important concepts.",
        },
        {
            "question": "Why use Groq for FlashMind AI?",
            "answer": "Groq is completely free with generous daily limits and runs Llama 3 at extremely fast speeds.",
        },
    ]


def generate_flashcards_safe(text: str) -> List[Dict[str, str]]:
    """Used by flashcards.py. Falls back to demo if no API key set."""
    if not os.getenv("GROQ_API_KEY"):
        return generate_flashcards_demo(text)
    return generate_flashcards(text)
"""
utils/llm.py – LLM integration for FlashMind AI.
Uses Groq API (FREE) — runs Llama 3 at ultra-fast speed.
"""

import os
import json
import re
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# ── Flashcard Prompt — min 15, max based on content ───────────────────────────
FLASHCARD_SYSTEM_PROMPT = """
You are FlashMind AI, an expert educational assistant that creates high-quality study flashcards.

Read the study material carefully and generate AT LEAST 15 flashcards.
If the content is rich, generate up to 30 flashcards to cover all key concepts.

STRICT RULES:
1. Return ONLY a valid JSON array — no markdown, no backticks, no explanation.
2. Each item must have exactly two keys: "question" and "answer".
3. Answers should be 1-3 sentences, clear and complete.
4. Cover key concepts, definitions, dates, processes, and important relationships.
5. Minimum 15 cards. More content = more cards (up to 30).

Output format (follow exactly):
[
  {"question": "...", "answer": "..."},
  {"question": "...", "answer": "..."}
]
"""

# ── Quiz Prompt — exactly 10 MCQ questions ────────────────────────────────────
QUIZ_SYSTEM_PROMPT = """
You are FlashMind AI. Generate exactly 10 multiple-choice quiz questions from the study material.

STRICT RULES:
1. Return ONLY a valid JSON array — no markdown, no backticks, no explanation.
2. Each item must have exactly these keys:
   - "question": the question text
   - "options": array of exactly 4 options (strings)
   - "answer": the correct option (must match one of the options exactly)
   - "explanation": 1-2 sentence explanation of why the answer is correct
3. Make options plausible and distinct.
4. Exactly 10 questions, no more, no less.

Output format:
[
  {
    "question": "...",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "A. ...",
    "explanation": "..."
  }
]
"""


def generate_flashcards(text: str) -> List[Dict[str, str]]:
    """Generate flashcards using Groq API."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Groq API key not found. "
            "Get a FREE key at https://console.groq.com → API Keys. "
            "Then set GROQ_API_KEY in your .env file."
        )
    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError("Run: pip install groq")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
            {"role": "user",   "content": f"Study material:\n\n{text}"},
        ],
        temperature=0.4,
        max_tokens=4000,
    )
    raw = response.choices[0].message.content.strip()
    return _parse_flashcards(raw)


def generate_quiz(text: str) -> List[Dict]:
    """Generate 10 MCQ quiz questions using Groq API."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return generate_quiz_demo(text)
    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError("Run: pip install groq")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": QUIZ_SYSTEM_PROMPT},
            {"role": "user",   "content": f"Study material:\n\n{text}"},
        ],
        temperature=0.4,
        max_tokens=3000,
    )
    raw = response.choices[0].message.content.strip()
    return _parse_quiz(raw)


def _parse_flashcards(raw: str) -> List[Dict[str, str]]:
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
    match = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("The AI returned an unexpected format. Please try again.")
    if not isinstance(data, list):
        raise RuntimeError("Expected a JSON array of flashcards.")
    valid = [
        {"question": str(item["question"]).strip(), "answer": str(item["answer"]).strip()}
        for item in data
        if isinstance(item, dict) and "question" in item and "answer" in item
    ]
    if not valid:
        raise RuntimeError("No valid flashcards found in AI response.")
    return valid  # No cap — return all generated cards


def _parse_quiz(raw: str) -> List[Dict]:
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
    match = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("Could not parse quiz. Please try again.")
    if not isinstance(data, list):
        raise RuntimeError("Expected a JSON array of questions.")
    valid = [
        q for q in data
        if isinstance(q, dict)
        and all(k in q for k in ["question", "options", "answer", "explanation"])
        and isinstance(q["options"], list) and len(q["options"]) == 4
    ]
    return valid[:10]


def generate_flashcards_demo(text: str) -> List[Dict[str, str]]:
    """15 sample cards shown when no API key is set."""
    return [
        {"question": "What is FlashMind AI?", "answer": "FlashMind AI converts your notes or PDFs into smart study flashcards using Groq + Llama 3 AI."},
        {"question": "How do you enable AI flashcard generation?", "answer": "Get a free API key from https://console.groq.com and set GROQ_API_KEY in your .env file."},
        {"question": "What input formats does FlashMind AI support?", "answer": "You can paste text directly or upload a PDF for automatic text extraction."},
        {"question": "How many flashcards are generated per session?", "answer": "At least 15 flashcards, up to 30 depending on the content length."},
        {"question": "Why use Groq for FlashMind AI?", "answer": "Groq is completely free with generous daily limits and runs Llama 3 at extremely fast speeds."},
        {"question": "What is a flashcard?", "answer": "A flashcard is a study tool with a question on one side and the answer on the other, used for active recall practice."},
        {"question": "What is active recall?", "answer": "Active recall is a learning technique where you test yourself on material rather than passively re-reading it."},
        {"question": "What is spaced repetition?", "answer": "Spaced repetition is a study method where you review material at increasing intervals to improve long-term retention."},
        {"question": "What model powers FlashMind AI?", "answer": "FlashMind AI uses Llama 3.3 70B, a powerful open-source model running on Groq's fast inference hardware."},
        {"question": "How does PDF extraction work?", "answer": "FlashMind AI reads your PDF, extracts all text content, and passes it to the AI for flashcard generation."},
        {"question": "What is the max text length processed?", "answer": "Up to 4,000 characters of text are processed per session to stay within API limits."},
        {"question": "Can I regenerate flashcards?", "answer": "Yes, use the Regenerate button to create a new set of flashcards from the same study material."},
        {"question": "What is the quiz feature?", "answer": "The quiz feature generates 10 multiple-choice questions from your study material to test your knowledge."},
        {"question": "What does the flip card UI do?", "answer": "The flip card shows the question first; clicking it flips to reveal the answer with a smooth animation."},
        {"question": "How do I navigate between flashcards?", "answer": "Use the Previous and Next buttons, or the card counter (e.g. 1/15) to jump between cards."},
    ]


def generate_quiz_demo(text: str) -> List[Dict]:
    """10 sample quiz questions shown when no API key is set."""
    return [
        {"question": "What does FlashMind AI use to generate flashcards?", "options": ["A. OpenAI GPT-4", "B. Groq + Llama 3", "C. Google Gemini", "D. Anthropic Claude"], "answer": "B. Groq + Llama 3", "explanation": "FlashMind AI uses the Groq API running Llama 3.3 70B for fast, free flashcard generation."},
        {"question": "What is the minimum number of flashcards generated?", "options": ["A. 5", "B. 10", "C. 15", "D. 20"], "answer": "C. 15", "explanation": "FlashMind AI generates a minimum of 15 flashcards per session, up to 30 based on content."},
        {"question": "Which file format can be uploaded to FlashMind AI?", "options": ["A. DOCX", "B. PPTX", "C. PDF", "D. TXT"], "answer": "C. PDF", "explanation": "FlashMind AI supports PDF uploads for automatic text extraction and flashcard generation."},
        {"question": "What learning technique do flashcards support?", "options": ["A. Passive reading", "B. Active recall", "C. Mind mapping", "D. Note-taking"], "answer": "B. Active recall", "explanation": "Flashcards are a classic active recall tool, which is proven to improve long-term memory retention."},
        {"question": "Where do you get a free Groq API key?", "options": ["A. openai.com", "B. huggingface.co", "C. console.groq.com", "D. anthropic.com"], "answer": "C. console.groq.com", "explanation": "Free Groq API keys are available at console.groq.com under the API Keys section."},
        {"question": "How many quiz questions are generated per deck?", "options": ["A. 5", "B. 8", "C. 10", "D. 15"], "answer": "C. 10", "explanation": "FlashMind AI generates exactly 10 multiple-choice quiz questions for every deck."},
        {"question": "What happens when you click a flip card?", "options": ["A. It deletes the card", "B. It shows the next card", "C. It flips to reveal the answer", "D. It marks the card as learned"], "answer": "C. It flips to reveal the answer", "explanation": "Clicking the flip card triggers an animation that reveals the answer on the back of the card."},
        {"question": "What is spaced repetition?", "options": ["A. Reading notes multiple times", "B. Reviewing at increasing intervals", "C. Studying for long hours", "D. Writing summaries"], "answer": "B. Reviewing at increasing intervals", "explanation": "Spaced repetition involves reviewing material at increasing time intervals for optimal long-term retention."},
        {"question": "What is the max text processed per session?", "options": ["A. 1,000 chars", "B. 2,000 chars", "C. 4,000 chars", "D. 10,000 chars"], "answer": "C. 4,000 chars", "explanation": "FlashMind AI processes up to 4,000 characters of text per session to stay within API limits."},
        {"question": "Which model runs on Groq for FlashMind AI?", "options": ["A. GPT-3.5", "B. Llama 3.3 70B", "C. Mistral 7B", "D. Falcon 40B"], "answer": "B. Llama 3.3 70B", "explanation": "FlashMind AI uses Llama 3.3 70B, a highly capable open-source model, running on Groq's fast inference platform."},
    ]


def generate_flashcards_safe(text: str) -> List[Dict[str, str]]:
    """Used by flashcards.py. Falls back to demo if no API key set."""
    if not os.getenv("GROQ_API_KEY"):
        return generate_flashcards_demo(text)
    return generate_flashcards(text)


def generate_quiz_safe(text: str) -> List[Dict]:
    """Used by flashcards.py. Falls back to demo if no API key set."""
    if not os.getenv("GROQ_API_KEY"):
        return generate_quiz_demo(text)
    return generate_quiz(text)