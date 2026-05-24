import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

from chart_engine import calculate_chart
from planet_strength_engine import enrich_planet_conditions
from aspect_engine import build_house_analysis_context
from yoga_engine import detect_yogas
from rag_engine import retrieve_knowledge

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later replace with your Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LiteReadingRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    dob: str
    time: str
    place: str
    question: str


@app.get("/")
def home():
    return {"status": "Astrea API is running"}


@app.post("/lite-reading")
def lite_reading(request: LiteReadingRequest):
    dob_obj = datetime.strptime(request.dob, "%Y-%m-%d").date()
    time_obj = datetime.strptime(request.time, "%H:%M").time()

    chart = calculate_chart(dob_obj, time_obj, request.place)
    chart = enrich_planet_conditions(chart)

    aspect_context = build_house_analysis_context(chart)
    detected_yogas = detect_yogas(chart)

    rag_query = f"""
    User question:
    {request.question}

    Ascendant:
    {chart["ascendant"]}

    Planet placements:
    {chart["planets"]}

    Detected yogas:
    {detected_yogas[:5]}

    Retrieve concise Vedic astrology rules for:
    - ascendant interpretation
    - planet in house interpretation
    - Rahu Ketu axis if relevant
    - yogas if relevant
    - direct answer to the user's question
    """

    knowledge, rag_sources = retrieve_knowledge(rag_query, n_results=5)

    prompt = f"""
You are Priyamvada's visitor-facing Vedic astrology assistant.

You are giving a short preview, not a full paid consultation.

VISITOR DETAILS:
Name: {request.name}
Question: {request.question}

CALCULATED CHART:
{chart}

ASPECT CONTEXT:
{aspect_context}

DETECTED YOGAS:
{detected_yogas[:5]}

RETRIEVED KNOWLEDGE:
{knowledge}

Write a short, premium, curiosity-building response.

Structure:

1. Your Chart Snapshot
Give 3 to 5 lines.

2. What Stands Out
Give 3 specific insights based on chart factors.

3. Answer to Your Question
Answer in 5 to 8 lines.

4. Why a Full Reading Would Help
Mention timing, dashas, yogas, transits, remedies and personal context.

5. Booking Invitation
End with a soft invitation to book a personal consultation with Priyamvada.

Rules:
- Do not give a full technical report.
- Do not show raw calculations.
- Do not be scary or fatalistic.
- Keep it warm, wise and premium.
- Do not use Markdown.
- Do not use ### headings.
- Do not use asterisks.
- Do not use bullet symbols.
- Use clean section titles in plain text.
- Keep the response elegant and readable for a website visitor.
Formatting rules:
- Do not use Markdown.
- Do not use ### headings.
- Do not use asterisks.
- Do not use bold formatting.
- Do not use bullet symbols.
- Use clean plain text section titles only.
- Keep paragraphs short and website-friendly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write short, engaging Vedic astrology preview readings for website visitors."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "ascendant": chart["ascendant"],
        "detected_yogas_count": len(detected_yogas)
    }