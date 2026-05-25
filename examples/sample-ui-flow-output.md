# Sample UI Understanding Report

## A. Source Summary

- Video path: `demo-checkout-flow.mp4`
- Video duration: `00:18`
- Frame extraction settings: `--fps 1`
- Contact sheet: `contact-sheet.jpg`
- Review date: 2026-05-25
- Evidence sources: timestamps and extracted frames

## B. Product / Function Goal

- Confirmed goal: demonstrate a mobile checkout flow from product browsing to completion
- Evidence: `00:00-00:18`, frames `frame_0001.jpg` through `frame_0018.jpg`
- Confidence: medium
- Notes: exact product copy is not fully legible

## C. Screen Inventory

| Screen | Evidence | Confidence | Notes |
|---|---|---|---|
| Product list | `00:00-00:04`, `frame_0001.jpg` | high | Visible card list and search area |
| Product detail | `00:04-00:09`, `frame_0005.jpg` | high | Detail view with main call to action |
| Cart | `00:09-00:14`, `frame_0010.jpg` | high | Cart row and checkout action |
| Success | `00:14-00:18`, `frame_0015.jpg` | medium | Exact success copy is unclear |

## D. Timeline of Interactions

| Step | Time / Frame | Screen | User Action | System Response | Evidence | Confidence | Notes |
|---|---|---|---|---|---|---|---|
| 1 | `00:00-00:04` / `frame_0001.jpg` | Product list | Taps a product card | Navigates to product detail | Timestamp and frame | high | Product text is partially unclear |
| 2 | `00:04-00:09` / `frame_0005.jpg` | Product detail | Taps primary call to action | Cart state appears to update | Timestamp and frame | medium | Button label is unable to confirm |
| 3 | `00:09-00:14` / `frame_0010.jpg` | Cart | Taps checkout action | Navigates to completion flow | Timestamp and frame | high | Payment subflow is not shown |
| 4 | `00:14-00:18` / `frame_0015.jpg` | Success | No visible action | Success state remains visible | Timestamp and frame | medium | Exact headline is unclear |

## E. UI Element Inventory

| Screen | Element | Type | Visible Label / Text | Evidence | Confidence | Notes |
|---|---|---|---|---|---|---|
| Product list | Search field | Input | Text includes `Search` | `frame_0001.jpg` | medium | Full placeholder unable to confirm |
| Product detail | Primary call to action | Button | unable to confirm | `frame_0005.jpg` | low | Add-to-cart intent inferred from response |
| Cart | Checkout action | Button | checkout-related label | `frame_0010.jpg` | medium | Exact text unclear |

## F. State and Interaction Rules

| Rule | Evidence | Confidence | Notes |
|---|---|---|---|
| Product card opens detail screen | `00:00-00:04` | high | Direct transition visible |
| Detail action changes cart state | `00:04-00:09` | medium | Cart badge appears to update |

## G. Form and Data Requirements

| Field / Data | Required? | Evidence | Confidence | Notes |
|---|---|---|---|---|
| Product title | yes | visible product cards | medium | exact values unclear |
| Payment fields | unable to confirm | not shown | low | payment screen is not visible |

## H. Inferred Data / API Needs

| Inferred Need | Evidence | Confidence | Notes |
|---|---|---|---|
| Product list data | visible product cards | medium | schema unable to confirm |
| Cart mutation | visible cart state change | medium | API shape unable to confirm |

## I. Visual and Layout Notes

- Layout: mobile, vertical flow, bottom navigation visible in early screens
- Typography: unable to confirm exact type scale
- Color: primary action color visible, exact token unable to confirm
- Spacing: card spacing appears consistent
- Motion: push-style screen transition appears likely
- Evidence: frames `frame_0001.jpg`, `frame_0005.jpg`, and `frame_0010.jpg`
- Confidence: medium

## J. Unclear or Unconfirmed Details

| Detail | Reason | Evidence | Confidence | Follow-up Needed |
|---|---|---|---|---|
| Exact primary action copy | text too small | `frame_0005.jpg` | low | confirm from source product |
| Payment fields | screen not shown | `00:09-00:14` jump | low | provide additional recording |
| Exact success headline | blurred | `frame_0015.jpg` | low | confirm from screenshot |

## K. Implementation Notes

- Implement only the visible list, detail, cart, and success screens.
- Keep unresolved labels as TODO items.
- Do not invent payment screens or API schemas.

## L. Optional Implementation Agent Prompt

Use `templates/implementation-agent-prompt-output.md` with this report.

Preserve every `unable to confirm` and `unclear` item as a TODO.
