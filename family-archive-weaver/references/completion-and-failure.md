# Completion and failure handling

The parent skill reports a business result only after a delegated expert returns `completed`. All other states are states, not successes.

## Delegation states

- `completed`: the step's business result exists and is passed to the next step.
- `failed`: the step could not produce its result. Dependent steps are stopped. Independent earlier results (transcripts, extractions, albums already created) are preserved and reported as partial results.
- `cancelled`: the user ended the workflow. Nothing further runs; already-approved writes that finished stay finished and are reported.
- `waiting_user`: clarification is required from the user before the workflow can continue. Used for unresolved person-name collisions (step 5) and language choice if recordings are mixed-language. The question must quote the exact conflicting names.
- `waiting_approval`: a state-change requires user confirmation. Expected at the step 6 plan gate and inside child workflows whenever the catalog marks an action `gateway`, `workflow`, or `conditional` (create-album, save-text, mkdir, tag-add-file, batch-move). The skill never bypasses or pre-approves these.

## Empty results

- No recordings found (step 1): report "no recordings found in <folder>" and stop. Do not scan other folders, do not substitute documents or photos.
- No transcribable file (step 2): report per-file failures and stop.
- No persons extracted (step 3): the archive degrades to a transcript-only document; albums are skipped and the story document notes why.
- No people albums (step 4) or no photos in range (step 5): zeros are reported as zeros; era albums from time anchors remain if photos exist.

Never substitute similar or unrelated content for an empty result. Never invent NAS data.

## Partial results

Partial output is a first-class outcome: the completion report lists created albums (with UUIDs), the story document path, tagged files, moved files (if approved), and — verbatim — every unverified mention and failure. A run that produced one album and one story document from five recordings is reported exactly as that, not as full success.
