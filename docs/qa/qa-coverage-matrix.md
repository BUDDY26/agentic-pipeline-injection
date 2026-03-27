# QA Coverage Matrix

> Use this matrix on every project audit. Check each category before marking QA complete.

---

## 1. Routes / Pages

| Check | Example Issues |
|-------|----------------|
| Every defined route renders without error | 404 on valid route; blank page on load |
| Route parameters are handled | Crash on missing or invalid param |
| Protected routes enforce auth | Unauthenticated user reaches restricted page |
| 404 / fallback route exists | Unknown path shows white screen |

---

## 2. Navigation / Links

| Check | Example Issues |
|-------|----------------|
| All nav links resolve to the correct route | Link points to wrong page or dead route |
| Active state reflects current route | No visual indicator of current page |
| External links open in new tab | User navigates away unintentionally |
| Back / breadcrumb navigation works | Browser back breaks app state |

---

## 3. Interactive UI — Buttons & Forms

| Check | Example Issues |
|-------|----------------|
| Every button has a defined action | Button click does nothing |
| Forms validate input before submit | Invalid data accepted; no feedback shown |
| Submit triggers correct handler | Wrong endpoint called; silent failure |
| Disabled states are applied correctly | Button active when it should be locked |
| Duplicate submission is prevented | Double-click submits twice |

---

## 4. Data Rendering

| Check | Example Issues |
|-------|----------------|
| All data fields render with correct values | Field shows `undefined`, `null`, or raw key |
| Lists render all items | Items silently dropped; wrong count |
| Nested or relational data resolves | Child data missing; broken references |
| Data types are formatted correctly | Raw ISO date; unformatted currency |

---

## 5. Loading States

| Check | Example Issues |
|-------|----------------|
| Loading indicator shown during async ops | UI appears frozen with no feedback |
| Partial / skeleton UI used where appropriate | Layout shift on data arrival |
| Loading state clears after data resolves | Spinner persists after load completes |

---

## 6. Empty States

| Check | Example Issues |
|-------|----------------|
| Empty list shows a message, not blank space | Page appears broken with no content |
| Empty search / filter result is communicated | User cannot tell if query ran |
| Empty state offers a next action where relevant | Dead end with no way forward |

---

## 7. Error States

| Check | Example Issues |
|-------|----------------|
| Failed API calls surface user-facing message | Silent failure; stale data shown |
| Form errors are displayed inline | Error only in console; no UI feedback |
| Network / timeout errors are handled | App hangs or crashes on poor connection |
| Error state allows recovery (retry / redirect) | User is stuck with no path out |

---

## 8. Hardcoded vs Dynamic Values

| Check | Example Issues |
|-------|----------------|
| No hardcoded user names, IDs, or emails | Demo data leaks into production view |
| No hardcoded URLs or environment values | Points to localhost or staging in prod |
| Labels and copy come from config or props | Duplicate strings; untranslatable copy |
| Count / total values are computed, not fixed | Displays "5 items" regardless of actual count |
