# family-archive-weaver

Everyone has a box (or a NAS folder) of old family recordings nobody ever opens, because listening and organizing is real work. This skill turns that folder into something the family actually browses.

Say something like:

> "Turn my parents' old recordings into a family archive."

The NAS then does the whole job by itself, in four passes:

1. **It listens.** Every voice memo, digitized tape, and camcorder clip in the folder is transcribed on the device. Inaudible stays `[inaudible]` — nothing is invented.
2. **It reads the stories out.** Who is talking, who they mention, the places, the years, and each distinct story — extracted with the passage it came from.
3. **It checks the photo shelf.** Only people the photo library actually knows (existing people albums) get matched. Exact names only; "maybe that's the same Wati" becomes a question to you, never a guess.
4. **It weaves and waits.** Before anything is written, you see the full plan: albums to create, the story document, tags, and every uncertain mention. Approve it (or trim it), and the archive appears — era albums with the photos, and next to the recordings a readable story document: each story with its own words, who was there, when, and which album holds the pictures.

Uncertain things are not hidden: they land in a final "Unverified" section of the document, quoted exactly.

**For who:** families digitizing tapes and voice memos; anyone whose photo library is fine but whose family *stories* live in audio nobody revisits.

**Safety:** your recordings and photos never leave the NAS. Nothing is deleted, ever — the only moves are the ones you approve, and originals are preserved. High-risk actions (creating albums, saving the document, tagging, moving) each ask first.

## Track

Bring Memories to Life — UGREEN Hackathon 2026 on AI NAS.

## Built with

UGOS expert agents (file-agent, knowledge-agent, document-agent, photo-agent) and capability catalog v2.0.0 commands: `ug-filesystem`, `ug-knowledge`, `ug-document`, `ug-photo`, `ug-filemgr`, `file-workflow`. Pure markdown orchestration — no scripts, no external services, no third-party runtimes.

## Disclosure

- Third-party components: none. The skill package is standard UTF-8 Markdown (SKILL.md plus the two linked reference files) with zero external binaries, scripts, or runtime dependencies.
- AI tools used during development: an AI coding assistant (Claude) was used to draft and structure the skill text against the official UGOS Skill Creation Tool (uliya-skill-kit v0.7.3) and its capability catalog; the assistant also ran the official static checker. All capability mappings were verified against the catalog data shipped with that kit.
