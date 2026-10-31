# Workflow steps

Per-step specification for `family-archive-weaver`. Every step below is executed by the delegated expert named in SKILL.md; the parent skill never calls `cli.invoke` and never bypasses approval. All capabilities come from capability catalog v2.0.0.

## Step 1 — Find recordings (file-agent)

- Input: the user's source folder path.
- Commands: `ug-filesystem find`, `ug-filesystem ls`.
- Recognized as recordings: audio files (e.g. voice memo, digitized tape, interview audio) and video files (e.g. camcorder, phone video) as classified by the file domain.
- Output: list of {filename, path, size, modified time}.
- Negative conditions: folder missing, unreadable, or empty of recordings -> return "no recordings found" and the skill reports this and stops. Subfolders are included; files in the NAS recycle bin are not.
- No file is opened, moved, renamed, or deleted in this step.

## Step 2 — Transcribe (knowledge-agent)

- Input: the file list from step 1 (verified results only).
- Command: `ug-knowledge audio-transcription`.
- Output per file: transcript text with timestamps where available, or a per-file failure reason.
- Per-file isolation: one failed transcription never stops the others; failures are carried forward, not retried silently.
- Negative conditions: inaudible passages are marked `[inaudible]`, never paraphrased or invented. A language that transcription does not support is a failure for that file, reported as such.
- If every file fails: report all failures, stop. Do not continue to extraction with an empty transcript set.

## Step 3 — Extract stories (document-agent)

- Input: successful transcripts from step 2.
- Command: `ug-document extract`.
- Extract: persons (with stated relationships), places, dates/years/eras, distinct stories (one-line summary each), recording language(s).
- Every extracted item must carry its source transcript and passage. Uncertainty in the transcript must be preserved as uncertainty in the extraction.
- Negative conditions: no invented names, dates, places, or events; no merging two similarly named persons into one; if a transcript contains none of the above (e.g. only ambient noise), report it as no-content and continue with the remaining transcripts.

## Step 4 — List people albums (photo-agent)

- Command: `ug-photo figure-albums`.
- Output: existing people album names + album UUIDs.
- Negative condition: no people albums on the NAS -> report and continue; album creation in step 7 is then skipped for persons and only era albums (from step 5 time anchors) remain possible.

## Step 5 — Verify persons against photos (photo-agent)

- Commands: `ug-photo search-picture` (per verified person, restricted to the user's date range if given), `ug-photo timeline` (time anchors).
- Matching rule: exact name match between extracted person and people album name. Near-matches (e.g. "Wati" vs "Wati Rahayu") are reported as unresolved and offered to the user as `waiting_user`; they are never auto-merged.
- Output: photo counts per person per year/era; zero counts are kept as zeros.
- Places are NOT matched to photos (the photo domain has no verified place entity to reconcile against); places appear only in the story document.

## Step 6 — Approval gate

- Present: albums to be created (with expected photo counts), story document target path and language, tags to apply, planned file moves (if any), and the complete list of unverified/unresolved mentions and transcription failures.
- `waiting_approval` until the user approves or edits the plan. User may remove any album or decline the optional move; declining the move never cancels albums or the story document.
- If the user cancels: report `cancelled`, keep transcripts (they are read-only results), change nothing.

## Step 7 — Create albums (photo-agent)

- Command: `ug-photo create-album-custom` (one per approved person or era).
- Only photos verified in step 5 are added. Album names follow the plan approved in step 6.
- Per-album isolation: a failed album creation is reported and the remaining albums continue.
- Output: real album UUIDs for created albums.

## Step 8 — Save story document (knowledge-agent)

- Command: `ug-knowledge save-text` into the archive folder.
- Content: one section per story (transcript excerpt + persons/places/dates + album UUID references), plus a final "Unverified and failed" section listing unresolved names, uncertain items, and transcription failures verbatim.
- Language: the recordings' language unless the user requested otherwise. If the user asked for a translated version, translation is a separate `ug-document translate` run proposed to the user first (`gateway` approval), saved as a second file; the original-language document is always produced first.
- Negative condition: nothing enters the document that is not in the transcripts, the extractions, or the album references.

## Step 9 — Tag and (optionally) move sources (file-agent)

- Commands: `ug-filemgr tag-add-file` ("family-archive" tag), `ug-filesystem mkdir` (archive folder, only if missing), `file-workflow batch-move` (only if the user approved moves in step 6).
- Moves place each source recording into a per-person subfolder of the archive folder. Originals are moved, never deleted; there is no delete path anywhere in this skill.
- Per-file results reported, including per-file failures; a failed move does not undo its tag and vice versa.

# Recovery and partial results

- The skill is restartable: source files are never modified until step 9, so re-running after any failure repeats cleanly.
- Partial archives are valid outcomes: e.g. 3 of 5 recordings transcribed, 2 of 4 persons verified -> the archive contains what succeeded, and the story document's final section states exactly what did not and why.
