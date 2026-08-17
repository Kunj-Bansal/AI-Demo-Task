import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

def build_architecture_pdf(output_filename="architecture.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY = colors.HexColor("#2B6CB0") # Slate Blue
    TEXT_DARK = colors.HexColor("#2D3748") # Charcoal Text
    BG_LIGHT = colors.HexColor("#F7FAFC")  # Off-white

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    story = []

    # Document Header
    story.append(Paragraph("GraphOne / FrontierAtlas — System Architecture Document", title_style))
    story.append(Paragraph("Production-Grade Data Pipeline & LLM Intelligence Orchestration Engine", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # Section 1
    story.append(Paragraph("1. Massive Scale Strategy (500,000+ Entities Ingestion)", h1_style))
    story.append(Paragraph(
        "To scale entity ingestion across hundreds of thousands of records without operational bottlenecks, the pipeline decouples link discovery from page processing using a distributed asynchronous architecture.",
        body_style
    ))
    story.append(Paragraph("• <b>Distributed Worker Pools:</b> Async event loops using Python <code>asyncio</code> and <code>aiohttp</code> paired with dynamic worker pools (Celery/Redis) scale horizontally without changing core logic.", bullet_style))
    story.append(Paragraph("• <b>Anti-Bot Evasion Engine:</b> High-value targets (Cloudflare/DataDome protected) are managed via Playwright Async running stealth drivers and dynamic proxy rotation (BrightData/ScraperAPI).", bullet_style))
    story.append(Paragraph("• <b>Concurrency Throttling:</b> Semaphore-bounded request queues maintain optimal target throughput without causing IP bans[cite: 1].", bullet_style))

    # Section 2
    story.append(Paragraph("2. Resilient Multi-Tier LLM Engine (413 & 429 Mitigation)", h1_style))
    story.append(Paragraph(
        "Large Language Model calls are managed through a robust execution layer designed for max data density and automated fault handling.",
        body_style
    ))
    story.append(Paragraph("• <b>DOM Stripping & Content Truncation (HTTP 413 Prevention):</b> Raw HTML payloads are pre-processed using <code>trafilatura</code>/<code>BeautifulSoup</code> to remove scripts, styles, headers, and navigation footers, maximizing token efficiency[cite: 1].", bullet_style))
    story.append(Paragraph("• <b>Multi-Tier Fallback Cascade:</b> API calls systematically cascade across model tiers: <b>Gemini Flash</b> (Primary) → <b>Groq Llama 3</b> (Secondary) → <b>DeepSeek</b> (Tertiary)[cite: 1].", bullet_style))
    story.append(Paragraph("• <b>Exponential Backoff with Jitter (HTTP 429 Rate Limits):</b> Rate-limit exceptions trigger dynamic sleep backoffs calculated as: <i>Wait Time = 2<sup>retry_count</sup> + uniform(0, 1)</i>[cite: 1].", bullet_style))

    # Section 3
    story.append(Paragraph("3. Freshness Tracking & Entity Resolution Strategy", h1_style))
    story.append(Paragraph(
        "Ensures absolute data accuracy and strict 24-hour publication freshness across news and job market channels.",
        body_style
    ))
    story.append(Paragraph("• <b>Distributed Deduplication:</b> SHA-256 content/URL hashing stored in a Redis Bloom Filter guarantees O(1) duplicate checks across crawling instances[cite: 1].", bullet_style))
    story.append(Paragraph("• <b>Timestamp Normalization:</b> Dynamic time strings (e.g., '2 hours ago', meta tags) are parsed into standardized ISO-8601 UTC format, automatically discarding records older than 24 hours[cite: 1].", bullet_style))
    story.append(Paragraph("• <b>Deterministic Entity Resolution:</b> Extracted strings undergo legal suffix stripping, normalization, and fuzzy matching (Token Sort Ratio ≥ 85%) against a canonical seed database[cite: 1].", bullet_style))

    # Section 4
    story.append(Paragraph("4. System Storage & Database Architecture Choice", h1_style))
    story.append(Paragraph(
        "The storage architecture divides operational transactions from analytical graph queries to maximize throughput.",
        body_style
    ))

    # Data Storage Table
    table_data = [
        [Paragraph("<b>Storage Layer</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Architectural Justification</b>", body_style)],
        [Paragraph("Relational DB", body_style), Paragraph("PostgreSQL", body_style), Paragraph("Stores schema-validated JSONB entity records (Startups, Products, Papers, Jobs)[cite: 1].", body_style)],
        [Paragraph("Graph Database", body_style), Paragraph("Neo4j", body_style), Paragraph("Maps multi-dimensional relations (Founders → Startups → Products → Papers)[cite: 1].", body_style)],
        [Paragraph("Vector Store", body_style), Paragraph("Pinecone / Qdrant", body_style), Paragraph("Enables semantic vector search over paper abstracts and startup profiles.", body_style)],
        [Paragraph("In-Memory Cache", body_style), Paragraph("Redis", body_style), Paragraph("Manages distributed task queuing, rate limit counters, and deduplication states[cite: 1].", body_style)]
    ]

    storage_table = Table(table_data, colWidths=[1.3*inch, 1.4*inch, 4.3*inch])
    storage_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(storage_table)

    # Build PDF
    doc.build(story)
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    build_architecture_pdf()