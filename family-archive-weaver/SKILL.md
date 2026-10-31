---
name: family-archive-weaver
description: Weaves a family archive out of old voice recordings stored on UGREEN AI NAS - transcripts, extracted people places dates and stories, era albums built from photo-library matches, and a readable story document saved beside the recordings, with every uncertain mention flagged instead of guessed. Use when the user says something like "turn my parents' old recordings into a family archive".
---

# Goal

Turn a folder of family audio or video recordings into a structured, readable family archive on the NAS: every story in the recordings is transcribed, the people, places, and dates mentioned are verified against the photo library, albums are created from verified matches only, and a story document (transcript excerpts, album references, clearly flagged unverified mentions) is saved beside the source files.

Scope: user-authorized home recordings (voice memos, digitized tapes, camcorder audio, phone videos) and the user's own photo library. Nothing is deleted. Writes and moves happen only after user approval.

# Required input

Collect from the user before starting; do not pre-collect parameters owned by child experts:

1. The source folder containing the recordings (an existing NAS path the user authorizes).
2. Optional: the date range of the recordings (for example 1990s tapes), and known family names to prefer during matching.
3. Optional: the target folder name for the archive output (default: FamilyArchive beside the source).

# Generation-time capability evidence

Each CLI below is mapped to its single registered expert from capability catalog v2.0.0; that expert performs every use of the CLI in this skill:

- `ug-filesystem` → `file-agent`
- `ug-knowledge` → `knowledge-agent`
- `ug-document` → `document-agent`
- `ug-photo` → `photo-agent`
- `ug-filemgr` → `file-agent`
- `file-workflow` → `file-agent`

# Orchestration

Delegate in this order. Each delegation is self-contained and consumes only the real results of upstream steps; a dependent step stops when its upstream result is unavailable. The full per-step specification, including inputs, constraints, negative conditions, output requirements, and edge-case handling, is in [references/workflow-steps.md](references/workflow-steps.md). State handling rules are in [references/completion-and-failure.md](references/completion-and-failure.md). A conversational user guide is in [references/readme.md](references/readme.md).

1. `delegate --target file-agent --instruction 'List every audio and video file in the source folder stated by the user, including subfolders, using ug-filesystem find and ls. Return filename, path, size, and modified time for each file. Do not open, move, or modify anything. If the folder does not exist or contains no audio or video files, return that result and nothing else.'`
2. `delegate --target knowledge-agent --instruction 'Transcribe each recording in the file list returned by the recording-search step, using ug-knowledge audio-transcription. Work file by file; for every file return the transcript text, or the failure reason if a file cannot be transcribed. Do not guess or fill in inaudible passages; mark them as inaudible. Do not modify or move the source files.'`
3. `delegate --target document-agent --instruction 'From each transcript produced by the transcription step, extract using ug-document extract: persons mentioned or speaking, with any stated relationship such as grandmother or uncle; places; dates, years, and eras; distinct stories or events, each with a one-line summary and the persons, places, and dates it involves; and the language of the recording. For each extracted item record which transcript and passage it came from. Items the transcripts state uncertainly must be marked uncertain. Do not invent names, dates, or events that the transcripts do not contain.'`
4. `delegate --target photo-agent --instruction 'List the existing people albums on this NAS using ug-photo figure-albums, returning each album name and album UUID. Report only what exists; if there are no people albums, return that result.'`
5. `delegate --target photo-agent --instruction 'For each person extracted by the story-extraction step whose name exactly matches a people album listed by the album-listing step: find photos of that person using ug-photo search-picture, restricted to the date range stated by the user if any, and read time anchors using ug-photo timeline. Return photo counts per person per year or era. Names that almost match an album name are not merged; report them as unresolved. If a matched person has no photos in range, return zero and continue.'`
6. Approval gate: present the archive plan to the user and wait: albums that will be created (person or era, expected photo count), the story document that will be saved and where, the tags that will be applied to source files, and every unverified or unresolved mention. Proceed only on explicit user approval of the plan; the user may remove items from the plan.
7. `delegate --target photo-agent --instruction 'Create the approved albums using ug-photo create-album-custom, one per approved person or era, populated with the verified photos found by the photo-verification step only. Return each created album UUID. Do not add photos of unresolved persons. If an album cannot be created, return the failure and continue with the remaining albums.'`
8. `delegate --target knowledge-agent --instruction 'Save the story document using ug-knowledge save-text to the archive folder agreed in the approval gate: one section per story from the story-extraction step with its transcript excerpt, the persons, places, and dates involved, references to the album UUIDs returned by the album-creation step, and a final section listing unverified mentions and transcription failures verbatim. Write the document in the language of the recordings unless the user asked for a translation. Do not include any name, date, or event that is not in the transcripts or the album references.'`
9. `delegate --target file-agent --instruction 'Apply the tag family-archive to each processed source recording using ug-filemgr tag-add-file, and create the archive folder with ug-filesystem mkdir if it does not exist. If the user approved moving the sources in the approval gate, move them into per-person subfolders using file-workflow batch-move. Return the tag and move results per file, including any per-file failures.'`

# Completion and failure

Handle every delegation state explicitly as specified in [references/completion-and-failure.md](references/completion-and-failure.md). Summary: report a business result only after the delegated expert returns completed. waiting_approval is expected at the approval gate and whenever a child workflow requires confirmation for a state-change; waiting_user is used for unresolved name collisions. A failed or cancelled step stops dependent steps; already-produced results (transcripts, extracted stories, albums) are preserved and reported as partial results. Empty results are reported as empty and the skill stops at the step that found nothing; nothing similar is ever substituted.
