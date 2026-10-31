# family-archive-weaver

**UGREEN AI NAS Hackathon 2026 entry — Track: Bring Memories to Life**

Everyone has a folder of old family recordings nobody ever opens, because listening and organizing is real work. This skill turns that folder into something the family actually browses: transcripts, extracted people, places, dates and stories, era albums built only from photo-library-verified matches, and a readable story document saved beside the recordings — with every uncertain mention flagged instead of guessed.

Say something like:

> "Turn my parents' old recordings into a family archive."

## How it works — four passes

1. **It listens.** Every voice memo, digitized tape, and camcorder clip in the folder is transcribed on the device. Inaudible stays `[inaudible]` — nothing is invented.
2. **It reads the stories out.** Who is talking, who they mention, the places, the years, and each distinct story — extracted with the passage it came from.
3. **It checks the photo shelf.** Only people the photo library actually knows (existing people albums) get matched. Exact names only; "maybe that's the same Wati" becomes a question to you, never a guess.
4. **It weaves and waits.** Before anything is written, you see the full plan: albums to create, the story document, tags, and every uncertain mention. Approve it (or trim it), and the archive appears — era albums with the photos, and next to the recordings a readable story document: each story with its own words, who was there, when, and which album holds the pictures.

Uncertain things are not hidden: they land in a final "Unverified" section of the document, quoted exactly.

## Safety

- Your recordings and photos never leave the NAS.
- Nothing is deleted, ever — the only moves are the ones you approve, and originals are preserved.
- Every state-changing action (creating albums, saving the document, tagging, moving) asks first through an approval gate.
- Exact-name matching only; near-matches become user questions, never auto-merges.

## Repository layout

| Path | What it is |
|---|---|
| `family-archive-weaver/` | The skill package: `SKILL.md` plus the linked references (per-step workflow, state handling, user guide) |
| `family-archive-weaver-pretest-skill.zip` | The packaged submission, exactly as uploaded for Round 1 |
| `build_submission.py` | Builds the Round 1 proposal PDF and packages the skill ZIP |
| `UGREEN_Round1_Proposal.pdf` | The proposal answering the official Round 1 questionnaire |

## How it's built

Pure-markdown orchestration per the Uliya standard: `SKILL.md` delegates only to UGOS expert agents (`file-agent`, `knowledge-agent`, `document-agent`, `photo-agent`) using capability catalog v2.0.0 commands (`ug-filesystem`, `ug-knowledge`, `ug-document`, `ug-photo`, `ug-filemgr`, `file-workflow`), passing verified upstream results only. No scripts, no direct CLI calls, no external services.

The Round 1 package passes the official `check-skill.mjs` static check with zero errors and zero warnings. Untested on a real NAS (planned for finalist testing day): transcription quality on old tape audio, people-album name matching, and album creation timing.

## Disclosure

- **Third-party components:** none. The skill package is standard UTF-8 Markdown with zero external binaries, scripts, or runtime dependencies.
- **AI tools used during development:** an AI coding assistant (Claude) was used to draft and structure the skill text against the official UGOS Skill Creation Tool (uliya-skill-kit v0.7.3) and its capability catalog; the assistant also ran the official static checker. All capability mappings were verified against the catalog data shipped with that kit.

## License

[MIT](LICENSE)
