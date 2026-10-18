---
inclusion: fileMatch
fileMatchPattern: "app/**/*"
---

# Learning UI Steering

## Experience direction

Build an original learning workspace inspired by the effective interaction patterns of hands-on platforms such as KodeKloud: persistent curriculum context, concise lessons, immediate practice, side-by-side lab instructions, progressive hints, validation, and visible progress.

Do not copy KodeKloud branding, names, logos, source code, screenshots, illustrations, proprietary lesson text, exact color palette, or pixel-level trade dress. Use an original product identity and visual system.

## Information architecture

The primary navigation is:

- **Today:** due reviews, recommended lesson/lab, session target, and resume.
- **Learn:** domain-aligned curriculum and short lessons.
- **Grill:** adaptive one-question-at-a-time Socratic practice.
- **Labs:** AWS Console walkthroughs and validation.
- **Review:** spaced recall of misconceptions and weak objectives.
- **Mock:** timed exam-style sessions with delayed feedback.
- **Knowledge:** local source search with objective and service filters.
- **Progress:** domain mastery, confidence calibration, lab evidence, and readiness risks.

Keep the active exam code and blueprint version visible in settings or curriculum context.

## Course layout

Desktop course pages use:

1. A collapsible left curriculum rail showing domains, modules, lesson/lab status, and due-review badges.
2. A central lesson canvas with short sections, diagrams, examples, checks, and a clear next action.
3. A contextual utility area or drawer for notes, glossary, sources, and objective IDs.
4. A compact header showing location, progress, and resume state.

Avoid long undifferentiated pages. Break lessons into concept, decision, example, failure mode, recall check, and practice blocks.

## Lab layout

Desktop lab mode prioritizes a resizable split workspace:

- **Instruction pane:** objective, scenario, architecture, one active step, prediction prompt, hints, check action, reflection, and cleanup.
- **Workspace pane:** validator output, local terminal where appropriate, architecture/context, notes, and evidence status.
- **Curriculum rail:** collapsible to maximize lab area.

The AWS Console should open in a separate tab through an explicit button. Do not rely on iframe embedding. Preserve active step, notes, timer, and checkpoint state when focus leaves the app or the app reruns.

Every checkpoint uses one explicit status:

- Not started
- In progress
- Self-reported
- Verified
- Failed
- Cleaned up

Never display `Verified` based only on navigation or a button click. It requires successful validator evidence. Never display `Cleaned up` until absence or a terminal deletion state is confirmed.

## Hints and feedback

Use a progressive hint ladder:

1. Conceptual nudge.
2. Relevant AWS service or architecture area.
3. Procedural guidance.
4. Full solution and explanation.

Record hint usage. A full solution does not count as independent lab completion until the learner later repeats the objective without it.

Grill feedback order:

1. Correct, partially correct, incorrect, or grading uncertain.
2. The decisive requirement or missing concept.
3. Correct reasoning and architecture trade-off.
4. Why tempting alternatives fail.
5. Primary source reference.
6. One targeted follow-up or next action.

Mock mode must not reveal correctness or hints before submission.

## Visual system

- Define original semantic tokens for background, surface, text, border, accent, success, warning, danger, and focus.
- Favor a dense professional workspace over decorative dashboards.
- Use consistent 4/8px spacing increments and restrained corner radii.
- Use icons with text labels for non-obvious actions.
- Keep line lengths readable and code/log panes monospaced.
- Reserve bright accent colors for actions and status, not large decorative surfaces.
- Use subtle elevation and borders to communicate pane hierarchy.

## Accessibility and responsiveness

- Target WCAG 2.2 AA contrast.
- Support keyboard navigation and visible focus indicators wherever Streamlit allows.
- Do not communicate correctness or status by color alone; pair color with icon and text.
- Label form controls and announce validation feedback clearly.
- Respect reduced-motion preferences; animation is never required to understand state.
- On narrow screens, stack panes and keep the active task before supplemental context.

## Streamlit implementation rules

- Use shared components and theme tokens rather than page-specific styling.
- Keep custom CSS centralized and minimal; do not target unstable generated class names.
- Avoid unsafe HTML unless no native component can satisfy an essential requirement.
- Use stable widget keys and persist durable actions before showing success.
- Keep answer keys, grading rubrics, hidden mock state, and AWS credentials out of browser-visible state.
- Show loading, empty, error, stale-source, offline, and unavailable-AWS states deliberately.

## Progress design

Do not reduce readiness to a single completion percentage. Present:

- Accuracy and delayed recall by exam domain/task.
- Confidence versus observed correctness.
- Repeated misconceptions and due reviews.
- Independent versus hint-assisted lab completion.
- Verified cleanup status.
- Timed scenario speed and unanswered-question rate.
- Source freshness and uncovered blueprint tasks.

When an aggregate readiness score is shown, expose its inputs and label it as an internal estimate rather than an AWS score prediction.
