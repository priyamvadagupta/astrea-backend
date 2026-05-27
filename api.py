import os

import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

import resend
from fastapi import HTTPException

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
from transit_engine import analyze_transits_for_native
from timing_engine import create_timing_windows

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

class BookingRequest(BaseModel):
    name: str
    email_or_whatsapp: str
    dob: str | None = None
    time: str | None = None
    place: str | None = None
    session_topic: str | None = None
    preferred_date_time: str | None = None
    intention: str | None = None


class LiteReadingRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    dob: str
    time: str
    place: str
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    question: str


@app.get("/")
def home():
    return {"status": "Astrea API is running"}


@app.post("/lite-reading")
def lite_reading(request: LiteReadingRequest):
    try:
        dob_obj = datetime.strptime(request.dob, "%Y-%m-%d").date()
        time_obj = datetime.strptime(request.time, "%H:%M").time()

        chart = calculate_chart(
            dob_obj,
            time_obj,
            request.place,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    chart = enrich_planet_conditions(chart)

    aspect_context = build_house_analysis_context(chart)
    detected_yogas = detect_yogas(chart)

    # Transit and timing analysis
    try:
        transit_analysis = analyze_transits_for_native(chart)
        timing_windows = create_timing_windows(transit_analysis)
    except Exception as e:
        print(f"Transit/timing analysis skipped due to error: {e}")
        transit_analysis = []
        timing_windows = []

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

Your role:
Use the chart, yogas, aspects, transits, timing windows, and retrieved knowledge internally.
Do not explain too many technical details to the visitor.
Give clear final outcomes, patterns, possibilities, and guidance in simple premium language.

VISITOR DETAILS:
Name: {request.name}
Question: {request.question}

CALCULATED CHART:
{chart}

ASPECT CONTEXT:
{aspect_context}

DETECTED YOGAS:
{detected_yogas[:5]}

TRANSIT ANALYSIS:
{transit_analysis}

TIMING WINDOWS:
{timing_windows}

RETRIEVED KNOWLEDGE:
{knowledge}

OUTCOME-STYLE RESPONSE INSTRUCTIONS:

Write like a warm, intuitive Vedic astrology guide.

Do not give a technical astrology lecture.
Do not overload the visitor with house numbers, lordships, aspects, degrees, Sanskrit terms, or raw calculations.

Use astrology logic internally, but present the answer as clear outcomes.

The visitor should feel:
- seen
- curious
- guided
- interested in booking a deeper consultation

For every answer, focus on:
- what may happen
- where it may happen
- what pattern to watch
- what may help the person
- broad timing, only if available

Use outcome-style language:
- Your chart suggests...
- There is a possibility that...
- One pattern that may show up is...
- This may unfold through...
- You may need to watch for...
- This area looks promising, but may need patience...
- If this resonates, a full reading can go deeper into timing and remedies.

DOMAIN-SPECIFIC HOOKS:

Use the visitor's question to identify the main life area. Then include 2 to 3 specific outcome-style hooks from that area when the chart context supports them.

Do not force every hook into every answer. Choose only what fits the visitor's question.

LOVE AND RELATIONSHIPS:
When the question is about love, dating, marriage, breakup, partner, or relationship future, include possible hooks such as:
- whether love may come through workplace, friends, online communication, travel, education, family circle, or foreign connection
- whether the connection looks straightforward, delayed, private, intense, karmic, or complicated
- whether family pressure, distance, secrecy, emotional confusion, or external influence may affect the relationship
- whether the person should move slowly, observe consistency, or avoid rushing attachment
- whether the timing looks immediate, delayed, or likely to improve over the next few months

Phrase carefully:
“There may be external influence or emotional confusion around this connection.”
Do not accuse anyone of cheating.

EDUCATION AND STUDIES:
When the question is about studies, exams, higher education, certifications, learning, research, or university plans, include possible hooks such as:
- whether higher studies look supportive
- whether success may come through structured learning, mentors, self-study, research, or certification
- whether foreign education, online learning, or specialized subjects may be beneficial
- whether the person may face delay, distraction, lack of confidence, or inconsistency
- whether the person should choose practical, analytical, spiritual, technical, creative, or communication-oriented subjects
- whether the next phase favors completing unfinished education or starting a new learning path

WORK, JOB AND CAREER:
When the question is about work, job, career growth, promotion, role change, leadership, office politics, or professional direction, include possible hooks such as:
- whether career growth may come through leadership, communication, analytics, technology, advisory work, management, teaching, consulting, or client-facing work
- whether workplace recognition may come slowly but steadily
- whether job change, role expansion, or responsibility increase may be indicated
- whether office politics, hidden competition, pressure from seniors, or unclear expectations may need caution
- whether growth may come through networking, visibility, skill-building, foreign clients, or digital platforms
- whether the person is better suited for stable employment, independent work, consulting, or a hybrid path

BUSINESS AND MONEY:
When the question is about business, entrepreneurship, income, financial growth, side income, clients, or investments, include possible hooks such as:
- whether business potential exists
- whether business should begin slowly as a side path or can become a major direction
- whether clients, consulting, digital offerings, teaching, advisory services, or international audiences may support growth
- whether partnerships should be handled carefully
- whether income may grow through networks, repeat clients, reputation, or niche expertise
- whether the person should avoid impulsive spending, unclear agreements, or over-expansion

HEALTH AND WELLBEING:
When the question is about health, body, energy, stress, sleep, emotional wellbeing, fertility, or recovery, be very careful.

Do not diagnose.
Do not predict disease.
Do not give medical advice.
Do not replace a doctor.

Use safe outcome-style hooks such as:
- whether the person may need better rest, routine, emotional grounding, or stress management
- whether energy may fluctuate due to pressure, overthinking, irregular routine, or emotional load
- whether the period calls for slowing down, nourishment, discipline, or professional medical support
- whether the person should avoid ignoring symptoms
- whether healing may require consistency rather than quick fixes

Always add:
“For health matters, please also follow qualified medical advice.”

FAMILY, HOME AND CHILDREN:
When the question is about family, parents, home, marriage family, children, pregnancy, childbirth, parenting, domestic peace, or family responsibilities, include possible hooks such as:
- whether family support, family pressure, or emotional responsibility may be a theme
- whether home life may require patience, boundaries, or mature communication
- whether children-related matters may involve delay, planning, medical support, or divine timing
- whether the person may feel pulled between personal desires and family expectations
- whether relocation, home environment, or family elders may influence the situation
- whether nurturing, patience, and emotional steadiness are important

For children or pregnancy questions:
Do not guarantee pregnancy or childbirth.
Do not give medical claims.
Use gentle wording:
“There may be potential, but this needs deeper chart timing and medical guidance.”
“Children-related themes require a full dasha, transit, and medical-context review.”

SPIRITUAL GROWTH AND LIFE PURPOSE:
When the question is about spiritual growth, purpose, healing, intuition, astrology, meditation, karma, inner peace, or meaning, include possible hooks such as:
- whether the person is moving through a karmic learning phase
- whether solitude, spiritual study, mantra, meditation, pilgrimage, service, or guidance from teachers may help
- whether the person may feel detached from old desires and drawn toward deeper meaning
- whether astrology, healing arts, counselling, teaching, research, or spiritual learning may become important
- whether the person’s intuition may strengthen after emotional difficulty
- whether the path requires surrender, discipline, service, or inner purification

TIMING HOOKS:
If timing_windows are available, include a broad timing hint:
- over the next few months
- gradually over the next 6 to 12 months
- after some delay
- during a period of transition
- when the person becomes more consistent or clear

Do not give exact dates in the free preview unless the data strongly supports it.

IF THE VISITOR ASKS A YES/NO QUESTION:
Give a direct answer first, but keep it nuanced.

Examples:
“Yes, there is potential, but it appears to grow better with patience and the right timing.”
“The chart shows possibility, but not in a rushed or straightforward way.”
“This looks possible, but the full timing needs deeper dasha and transit analysis.”

IF MENTIONING WHY:
Keep the why simple and non-technical.

Use phrases like:
- This comes from the relationship and timing patterns in your chart.
- Your chart shows a mix of attraction and caution around this area.
- The current timing suggests this theme may become more active gradually.
- Your chart shows potential, but the details need deeper dasha and transit analysis.

Do not explain detailed house/lord/aspect logic in the free preview.

STRUCTURE:

1. Your Chart Snapshot
Give 3 to 5 lines.
Make it outcome-focused, not technical.

2. What Stands Out
Give 3 specific insights as final outcomes or patterns.
Do not over-explain technical reasons.

3. Answer to Your Question
Answer in 5 to 8 lines.
Make this the strongest section.
Identify the visitor’s main life area and include 2 to 3 specific outcome hooks from the relevant category:
love, education, work, career, business, money, health, family, children, or spiritual growth.
Give final outcomes more than technical explanations.
Only mention hooks that fit the chart context.

4. Why a Full Reading Would Help
Mention that a full reading can go deeper into timing, dashas, yogas, transits, remedies, and personal context.
Do not make the free preview feel complete.

5. Booking Invitation
End with a soft invitation to book a personal consultation with Priyamvada.

RULES:
- Do not give a full technical report.
- Do not show raw calculations.
- Do not be scary or fatalistic.
- Do not guarantee future events.
- Do not accuse anyone of cheating.
- Do not diagnose health conditions.
- Do not give medical, legal, financial, or mental health advice.
- Keep it warm, wise, premium, and curiosity-building.
- Keep technical astrology terms minimal.
- Give final outcomes more than technical explanations.
- Choose hooks based on the visitor’s question category. Do not include irrelevant life areas.
- Do not use Markdown.
- Do not use ### headings.
- Do not use asterisks.
- Do not use bullet symbols.
- Do not use bold formatting.
- Use clean section titles in plain text.
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
        "detected_yogas_count": len(detected_yogas),
        "transit_analysis": transit_analysis,
        "timing_windows": timing_windows
    }

@app.post("/booking-request")
def booking_request(request: BookingRequest):
    resend_api_key = os.getenv("RESEND_API_KEY")
    receiver_email = os.getenv(
        "BOOKING_RECEIVER_EMAIL",
        "priyamvada.gupta@guidancebystars.com"
    )

    if not resend_api_key:
        raise HTTPException(
            status_code=500,
            detail="Email service is not configured. Missing RESEND_API_KEY."
        )

    resend.api_key = resend_api_key

    subject = f"New Astrea Booking Request from {request.name}"

    body = f"""
New consultation booking request received from the Astrea website.

Name:
{request.name}

Email or WhatsApp:
{request.email_or_whatsapp}

Date of Birth:
{request.dob or "Not provided"}

Time of Birth:
{request.time or "Not provided"}

Place of Birth:
{request.place or "Not provided"}

Area of Guidance:
{request.session_topic or "Not provided"}

Preferred Weekend Slot:
{request.preferred_date_time or "Not provided"}

Question / Intention:
{request.intention or "Not provided"}
"""

    try:
        resend.Emails.send({
            "from": "Astrea <bookings@guidancebystars.com>",
            "to": [receiver_email],
            "subject": subject,
            "text": body,
            "reply_to": request.email_or_whatsapp
        })

        return {
            "status": "success",
            "message": "Your consultation request has been received. Priyamvada will get back to you soon."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not send booking email: {str(e)}"
        )