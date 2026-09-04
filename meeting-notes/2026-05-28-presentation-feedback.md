---
title: Meeting — presentation feedback
status: final
owner: Luca Martinet
created: 2026-05-28
updated: 2026-09-04
tags: [meeting, presentation, feedback]
---

# Meeting — presentation feedback

**Date:** 2026-05-28
**Attendees:** Luca Martinet, Noé Kurata

## Summary

Feedback on the project presentation. The recurring theme: establish the vision
in the first few minutes, keep one idea per slide, define technical terms before
using them, and prove feasibility through the live demo rather than explaining it
on slides. Concrete asks include benchmark comparisons against competitors,
performance charts, and splitting CI, data flow and roadmap onto separate slides.

## Overall Presentation

- Establish a clear vision of the project within the first few minutes.
- Be more direct and concise throughout the presentation.
- Keep slides focused on a single idea/topic.
- Reduce technical jargon and explain concepts for non-technical audiences.
- Define any technical terms before using them.
- Make a promise early in the presentation and demonstrate later how the project fulfils it.
- Explain the large differences between protection levels and justify them.

## Slide Structure

- One main message per slide.
- Remove notes underneath tables.
- Consider removing the image from the competitors section if it is not directly relevant.

## Product & Value Proposition

### Slide 5

- Simplify the content.
- Focus on what users can do with the product.
- Avoid implementation or technical details.

## Technical Content

- Demonstrate that the system handles errors correctly.
- Simplify the Data Flow explanation.
- Data Flow slide is currently too technical.
- Replace the term "Poisoning" with a more neutral or accessible term if possible.

## Testing & Validation

- Follow the beta testing plan exactly as specified.
- Show benchmark comparisons against competing solutions.
- Include performance charts/graphs.
- Demonstrate feasibility through the live demo rather than explaining everything on slides.
- Show the tester during the live demonstration.

## Project Organisation

Separate the following into individual slides:

### CI / Code Quality

**Keywords:**

- Code Quality
- Automation
- Testing
- Continuous Integration

### Data Flow

- Simplified explanation.
- Focus on user value rather than implementation.

### Milestones / Roadmap

- Clear project progression.
- Key deliverables.
- Future development.

## Visual Improvements

### AI Growth / Industry Need Graphic

Create a chart showing the growth of AI systems using copyrighted music or training on music datasets.

| Year        | Number of AI Music Models | Challenge                                    |
| ----------- | ------------------------- | -------------------------------------------- |
| Early Years | 1                         | Easy to monitor                              |
| Later Years | Several                   | More difficult to track                      |
| Today       | 40+                       | Manual rights management becomes impractical |

**Key message:**

> As AI adoption grows exponentially, creators need automated ownership, rights management, and metadata tracking.

**Purpose:**

- Demonstrate why the problem is growing.
- Show why the solution becomes more valuable over time.

## Unclear Feedback Item

### "Registre publique, process et perdus paraport au son"

Possible interpretation:

- Look into existing public music rights registries.
- Explain how the solution relates to or complements existing registries.
- Investigate whether public registries could be used as a source of truth for ownership, rights management, and AI training permissions.

## Related

- [`2026-04-12-meeting-pedago.md`](2026-04-12-meeting-pedago.md) — the deliverables this presentation covered
