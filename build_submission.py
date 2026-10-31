#!/usr/bin/env python3
"""Build UGREEN Round 1 proposal PDF + verify limits, then package the skill ZIP."""
import re, zipfile, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(BASE, 'family-archive-weaver')
OUT_PDF = os.path.join(BASE, 'UGREEN_Round1_Proposal.pdf')
OUT_ZIP = os.path.join(BASE, 'family-archive-weaver-pretest-skill.zip')

QA = [
 ("1. What does your Skill do?",
  "It turns a folder of family voice recordings into a woven archive: on-device transcripts, extracted people, places, dates and stories, era albums built only from photo-library-verified matches, and a readable story document saved beside the recordings."),
 ("2. Who is your target user, and what is their problem?",
  "Families digitizing tapes and voice memos. Their photo library is organized, but the family stories live in audio nobody revisits, because listening, noting who said what, and matching photos is hours of work."),
 ("3. What is your solution?",
  "A delegation-only Uliya skill: transcribe every recording, extract each story with its people, places and dates, verify people against existing NAS people albums (exact matches only; near-matches become user questions), then create era albums and save a story document that quotes the recordings and flags every unverified mention instead of guessing."),
 ("4. What is the main user flow?",
  "The user says \"turn my parents' old recordings into a family archive\" and points at a folder. Find recordings, transcribe each, extract stories, list people albums, verify matches, show the approval gate with the full plan, create albums, save the story document, tag sources, and optionally move them after approval."),
 ("5. How is your idea different from existing tools or common AI solutions?",
  "Cloud memory services sell writing prompts and subscriptions; photo apps auto-album by date and face but never read audio. No shipped tool ingests local recordings and reconciles spoken stories against a local photo library. The NAS is the only private place where both halves already live."),
 ("6. Which UGREEN AI NAS features does your Skill use, and at which step?",
  "Files: finding recordings, tagging, optional move (steps 1, 9). Knowledge: on-device transcription and saving the story document (steps 2, 8). Documents: structured extraction from transcripts (step 3). Albums: people albums, picture search, timeline, album creation (steps 4, 5, 7)."),
 ("7. What is your technical approach?",
  "Pure-markdown orchestration per the Uliya standard: SKILL.md delegates only to file-agent, knowledge-agent, document-agent and photo-agent, passing verified upstream results only. No scripts, no direct CLI calls, no external services. State-change actions (albums, save, tag, move) each require user approval; empty results stop the flow; partial results are preserved and reported."),
 ("8. What have you built so far? What is not built yet? What still needs testing on a NAS?",
  "Built: the complete Round 1 package (SKILL.md plus two linked references), which passes the official check-skill.mjs static check with zero errors and zero warnings. Nothing code-wise remains for Round 1: the standard requires no executable code. Untested on a real NAS: transcription quality on old tape audio, people-album name matching, and album creation timing - planned for finalist testing day."),
 ("9. How will you test your Skill if you become a Finalist? Name two core test cases and one edge case.",
  "Core 1: five recordings plus existing people albums; verify albums are created only for exact-name matches and the story document quotes transcripts with album references. Core 2: recordings mentioning an unknown person; verify no album is created, the mention lands in the Unverified section, and the flow still completes. Edge: one corrupt, untranscribable file among valid ones; verify the per-file failure is recorded, others process, and the archive is reported as partial."),
 ("10. What are the known limits, risks, or outside dependencies?",
  "No third-party components and no network dependencies. Risks: on-device transcription accuracy on noisy tapes (handled with inaudible markers, never paraphrased); same-name collisions (handled with a user question, never auto-merged); translation offered only as a separate approved step. Limits: places are not matched to photos because the photo domain exposes no verified place entity; albums use existing people albums only."),
]

def wc(t):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\"-]*", t))

total = sum(wc(a) for _, a in QA)
print('substantive word count:', total)
assert total <= 500, 'OVER 500 WORDS'

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

styles = getSampleStyleSheet()
q_style = ParagraphStyle('q', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12.5, spaceBefore=7, textColor='#0b3d2e')
a_style = ParagraphStyle('a', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13, spaceBefore=2)
t_style = ParagraphStyle('t', parent=styles['Title'], fontSize=15, leading=19, spaceAfter=2)
s_style = ParagraphStyle('s', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11, spaceAfter=6, textColor='#555555')

doc = SimpleDocTemplate(OUT_PDF, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm, title='family-archive-weaver - Round 1 Project Proposal')
story = [
    Paragraph('family-archive-weaver', t_style),
    Paragraph('Round 1 Project Proposal - UGREEN Hackathon 2026 on AI NAS - Track: Bring Memories to Life - Entrant: solo developer', s_style),
]
for q, a in QA:
    story.append(Paragraph(q, q_style))
    story.append(Paragraph(a, a_style))
doc.build(story)
sz = os.path.getsize(OUT_PDF)
print('PDF bytes:', sz, '(limit 1 MB)')
assert sz < 1024*1024

# ZIP the skill package (nested folder at zip root)
if os.path.exists(OUT_ZIP):
    os.remove(OUT_ZIP)
with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(SKILL_DIR):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, BASE))
    z.write(OUT_PDF, os.path.join('family-archive-weaver', '..', os.path.basename(OUT_PDF)).replace('/..','')) if False else None

with zipfile.ZipFile(OUT_ZIP) as z:
    names = z.namelist()
    total_unc = sum(i.file_size for i in z.infolist())
    print('zip entries:', len(names))
    for n in names:
        print('  ', n)
    print('zip bytes:', os.path.getsize(OUT_ZIP), '| uncompressed:', total_unc, '(limits: 10 MB / 10 MB / 100 files / 1 MB per file)')
    for i in z.infolist():
        assert i.file_size <= 1024*1024, f'file too big: {i.filename}'
    assert len(names) <= 100 and total_unc <= 10*1024*1024 and os.path.getsize(OUT_ZIP) <= 10*1024*1024
print('ALL LIMITS OK')
