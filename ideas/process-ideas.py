#!/usr/bin/env python3
"""Ideas Repository — Auto-processor
Detects new ideas in ideas/inbox/, evaluates them, and routes them."""

import os
import json
import time
from pathlib import Path
from datetime import datetime
import re

# Config
IDEA_DIR = Path("ideas")
INBOX = IDEA_DIR / "inbox"
PROCESSING = IDEA_DIR / "processing"
APPROVED = IDEA_DIR / "approved"
IMPLEMENTED = IDEA_DIR / "implemented"
DISCARDED = IDEA_DIR / "discarded"
STATE_FILE = IDEA_DIR / "index.md"
LOCK_FILE = IDEA_DIR / ".processing.lock"

# Minimum scores to approve
MIN_RELEVANCY = 6
MIN_IMPLEMENTABILITY = 5
MIN_ROI = 6

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_file_content(path: Path) -> str:
    """Read file content with encoding fallback."""
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return ""

def fetch_url_content(url: str) -> str:
    """Fetch content from URL using curl (available in Git Bash)."""
    try:
        import subprocess
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "30", url],
            capture_output=True,
            text=True,
            timeout=35
        )
        return result.stdout[:5000]  # Limit to 5000 chars
    except Exception as e:
        return f"[ERROR fetching URL: {e}]"

def score_idea(content: str, source_url: str = "") -> dict:
    """Simple scoring based on keywords and content analysis."""
    content_lower = content.lower()
    url_lower = source_url.lower()

    # Tags from content
    tags = set()
    keywords = {
        "marketing": ["marketing", "seo", "google ads", "meta ads", "social media", "contenido", "leads"],
        "sales": ["sales", "ventas", "crm", "pipeline", "pricing", "proposal"],
        "automation": ["automation", "whatsapp", "email", "workflow", "automatización", "zapier"],
        "web": ["web", "landing", "sitio", "ecommerce", "shopify", "wordpress"],
        "ai": ["ai", "claude", "openai", "gpt", "automation", "agent", "llm"],
        "mexico": ["méxico", "pymes", "mexico", "latam", "latinoamérica"],
        "productividad": ["productividad", "productivity", " eficiente", "automatización"],
    }
    for tag, kws in keywords.items():
        if any(kw in content_lower for kw in kws):
            tags.add(tag)

    # Simple relevance scoring
    relevance = 5
    for kw in ["imkt", "agencia", "pymes", "méxico", "marketing digital", "automatización"]:
        if kw in content_lower:
            relevance += 1
    for kw in ["python", "javascript", "node", "react", "api"]:
        if kw in content_lower:
            relevance += 0.5

    implementability = 7  # default assumption
    if "github" in url_lower or "npm" in url_lower or "pypi" in url_lower:
        implementability += 2
    if "docker" in content_lower and "compose" in content_lower:
        implementability -= 1  # harder in Antigravity

    roi = (relevance + implementability) / 2

    return {
        "relevance": min(10, relevance),
        "implementability": min(10, implementability),
        "roi": min(10, roi),
        "tags": list(tags)[:5],
    }

def create_idea_file(content: str, source: str, source_url: str = "") -> dict:
    """Create a processed idea from raw content."""
    # Generate ID
    idea_id = f"idea-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Get title from first line or first 100 chars
    lines = content.strip().split("\n")
    title = lines[0][:80] if lines else "Untitled"
    summary = content[:300] if len(content) > 300 else content

    # Score it
    scores = score_idea(content, source_url)

    # Determine lead based on tags
    lead_map = {
        "marketing": "Mila",
        "sales": "Sofia",
        "automation": "Finn",
        "web": "Finn",
        "ai": "Finn",
        "productividad": "Nova",
        "mexico": "Lena",
    }
    lead = lead_map.get(scores["tags"][0], "Gabriel") if scores["tags"] else "Gabriel"

    idea = {
        "id": idea_id,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "fuente": source,
        "source_url": source_url,
        "titulo": title,
        "resumen": summary,
        "tags": scores["tags"],
        "lead": lead,
        "relevancia": scores["relevance"],
        "implementabilidad": scores["implementability"],
        "roi": scores["roi"],
        "estado": "approved" if (scores["relevance"] + scores["roi"]) / 2 >= 7 else "discarded",
        "evaluado": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nota": ""
    }

    return idea

def process_inbox():
    """Main processing loop."""
    log("Ideas Repository processor started")

    # Check for lock (another instance running)
    if LOCK_FILE.exists():
        lock_age = time.time() - LOCK_FILE.stat().st_mtime
        if lock_age < 300:  # Less than 5 min old
            log("Another instance running, skipping")
            return
        log("Stale lock found, removing")

    LOCK_FILE.write_text(str(os.getpid()))
    try:
        while True:
            new_files = list(INBOX.glob("*"))
            if new_files:
                log(f"Found {len(new_files)} new file(s) in inbox")

            for f in new_files:
                try:
                    log(f"Processing: {f.name}")
                    content = get_file_content(f)

                    # Detect if it's a URL
                    source_url = ""
                    if content.strip().startswith("http"):
                        source_url = content.strip().split("\n")[0]
                        content = fetch_url_content(source_url)

                    # Create idea
                    idea = create_idea_file(content, f.name, source_url)

                    # Save idea file
                    idea_filename = f"{idea['id']}.md"
                    idea_path = APPROVED / idea_filename if idea["estado"] == "approved" else DISCARDED / idea_filename

                    # Write full idea with content
                    full_md = f"""---
id: {idea['id']}
fecha: {idea['fecha']}
fuente: {idea['fuente']}
source_url: {idea['source_url']}
tags: [{', '.join(idea['tags'])}]
lead: {idea['lead']}
relevancia: {idea['relevancia']}
implementabilidad: {idea['implementabilidad']}
roi: {idea['roi']}
estado: {idea['estado']}
---

## {idea['titulo']}

{idea['resumen']}

## Scores
- Relevancia: {idea['relevancia']}/10
- Implementabilidad: {idea['implementabilidad']}/10
- ROI: {idea['roi']}/10

## Raw content
```
{content[:2000]}{'...' if len(content) > 2000 else ''}
```
"""
                    idea_path.write_text(full_md, encoding="utf-8")

                    # Remove from inbox
                    f.unlink()

                    log(f"  → {idea['estado'].upper()}: {idea['id']} ({idea['lead']})")

                except Exception as e:
                    log(f"Error processing {f}: {e}")

            # Update index
            update_index()

            # Run every 10 minutes
            time.sleep(600)

    finally:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
        log("Processor stopped")

def update_index():
    """Update the ideas index."""
    approved = list(APPROVED.glob("*.md"))
    discarded = list(DISCARDED.glob("*.md"))
    implemented = list(IMPLEMENTED.glob("*.md"))
    processing = list(PROCESSING.glob("*.md"))
    inbox = list(INBOX.glob("*"))

    lines = [
        "# Ideas Repository — IMPKT",
        "",
        f"## Stats ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
        f"- Total approved: {len(approved)}",
        f"- Discarded: {len(discarded)}",
        f"- Implemented: {len(implemented)}",
        f"- Processing: {len(processing)}",
        f"- In inbox: {len(inbox)}",
        "",
        "## Approved ideas",
    ]

    for f in sorted(approved, reverse=True)[:20]:
        front = parse_frontmatter(get_file_content(f))
        if front:
            lines.append(f"- [{front.get('id', f.stem)}]({f.name}) — {front.get('titulo', '?')} **[{front.get('lead', '?')}]**")

    lines.extend(["", "## Recently discarded",])
    for f in sorted(discarded, reverse=True)[:5]:
        front = parse_frontmatter(get_file_content(f))
        if front:
            lines.append(f"- ~~{front.get('id', f.stem)}~~ — {front.get('titulo', '?')}")

    STATE_FILE.write_text("\n".join(lines), encoding="utf-8")

def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    front_text = parts[1].strip()
    result = {}
    for line in front_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result

if __name__ == "__main__":
    # Run once (for scheduled task)
    process_inbox()