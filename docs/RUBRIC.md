# Marking Rubric — S6 ICT SBA Task 2 (Testing and Evaluation)

**CampusConnect Phonebook · Elective B1: Web Programming and Application**

Total: **100 marks**. Scale to your school's SBA allocation (for example,
divide by 5 for a 20-mark task, or by 2 for a 50-mark task).

> Credit is awarded for the **quality of testing and reporting**, not simply
> for the number of vulnerabilities found. A student who tests systematically,
> documents evidence precisely and evaluates risk thoughtfully can score highly
> even if they do not find every planted weakness.

---

## 1. Criteria and weightings

| Criterion | Weight | What is being judged |
|---|---:|---|
| **C1. Test planning and coverage** | 15 | Scope, test design, coverage of normal and abnormal behaviour, traceability |
| **C2. Functional and usability testing** | 20 | Correct execution of functional, usability, accessibility and compatibility tests |
| **C3. Security and robustness testing** | 25 | Investigation of input handling, authentication, access control, output handling, configuration and error behaviour |
| **C4. Defect documentation and evidence** | 20 | Reproducibility, clarity, evidence quality, severity justification |
| **C5. Evaluation, prioritisation and recommendations** | 15 | Risk analysis, prioritisation, specific and feasible recommendations, fitness-for-purpose judgement |
| **C6. Professional conduct and reflection** | 5 | Authorisation, scope, safe handling of data, responsible disclosure, reflection |

---

## 2. Level descriptors

### C1. Test planning and coverage (15 marks)

| Level | Marks | Descriptor |
|---|---:|---|
| **Exemplary** | 13–15 | Clear, well-scoped plan with a rationale for what is in and out of scope. At least 20 well-chosen cases covering functional, validation, authentication, access control, usability, compatibility and robustness. Expected results are specific and traceable to requirements. Test data and environment are stated. |
| **Proficient** | 11–12 | Clear plan with at least 20 cases and good coverage. A few areas are thin (for example, accessibility or error handling), but the overall design is sound. Expected results are mostly specific. |
| **Developing** | 8–10 | Plan exists but coverage is uneven or mostly happy-path. Some cases lack expected results or preconditions. Fewer than 20 cases, or many cases duplicate each other. |
| **Emerging** | 0–7 | Little or no test plan; cases are vague, unrelated to the application, or cannot be executed. Major areas are missing. |

### C2. Functional and usability testing (20 marks)

| Level | Marks | Descriptor |
|---|---:|---|
| **Exemplary** | 17–20 | Functional tests are executed accurately and cover login, registration, search, add contact, admin access, logout and reset behaviour. Usability, accessibility and compatibility are tested with evidence (keyboard, labels, contrast, responsive widths, at least two browsers). Pass/fail judgements are correct and justified. |
| **Proficient** | 14–16 | Most core functions are tested correctly. Usability and compatibility are covered but with limited depth or evidence. A few pass/fail judgements are imprecise. |
| **Developing** | 10–13 | Only the main happy paths are tested. Little attention to accessibility, responsive behaviour or cross-browser issues. Some results are recorded without enough detail to verify. |
| **Emerging** | 0–9 | Functional testing is superficial, inaccurate or largely missing. No meaningful usability or compatibility evidence. |

### C3. Security and robustness testing (25 marks)

| Level | Marks | Descriptor |
|---|---:|---|
| **Exemplary** | 21–25 | Systematic investigation of input handling, authentication/session behaviour, access control, output handling, sensitive data, configuration and error messages. Uses safe, well-documented techniques (special characters, cookie inspection, direct requests, source/header inspection). Findings are confirmed with evidence and the underlying cause is explained. |
| **Proficient** | 18–20 | Covers most major risk areas and confirms several real issues. Some techniques are used without full follow-up, or one important area (for example, access control or configuration) is underexplored. |
| **Developing** | 13–17 | Tests a few obvious inputs or one security theme. Findings may be speculative, unreproducible or based only on a scan/alert. Limited investigation of authentication, access control or output handling. |
| **Emerging** | 0–12 | Little or no security testing; unsafe or out-of-scope behaviour; claims are unsupported or incorrect. |

### C4. Defect documentation and evidence (20 marks)

| Level | Marks | Descriptor |
|---|---:|---|
| **Exemplary** | 17–20 | At least five well-written defect reports. Each is reproducible from the steps alone, has expected vs actual results, a justified severity, clear impact, labelled evidence and a specific recommendation. Titles are concise and searchable. |
| **Proficient** | 14–16 | Defects are clear and mostly reproducible. Evidence is present and labelled. Severity is reasonable, though one or two justifications are thin. |
| **Developing** | 10–13 | Defect reports are present but missing key fields (steps, expected result, impact or evidence). Severity is inconsistent. Some reports combine several issues into one. |
| **Emerging** | 0–9 | Fewer than five usable reports, or reports are unreproducible, unsupported or not clearly defects. |

### C5. Evaluation, prioritisation and recommendations (15 marks)

| Level | Marks | Descriptor |
|---|---:|---|
| **Exemplary** | 13–15 | Clear, evidence-based judgement on fitness for release. Risks are prioritised using likelihood and impact. Recommendations are specific, feasible and separated into must-fix/should-fix/nice-to-have. Evaluation addresses the quality attributes and acknowledges testing limitations. |
| **Proficient** | 11–12 | Sound evaluation with a clear recommendation and reasonable prioritisation. Recommendations are mostly specific. Some quality attributes or limitations are mentioned only briefly. |
| **Developing** | 8–10 | Evaluation is largely descriptive. Prioritisation is unclear or based only on severity labels. Recommendations are generic (“improve security”, “add validation”). |
| **Emerging** | 0–7 | Little evaluation beyond a list of bugs; no clear recommendation, prioritisation or reflection on limitations. |

### C6. Professional conduct and reflection (5 marks)

| Level | Marks | Descriptor |
|---|---:|---|
| **Exemplary** | 5 | Works strictly within the authorised scope. Uses fictional data, protects evidence, reports privately and reflects thoughtfully on ethical and legal responsibilities. Contributes constructively to group work. |
| **Proficient** | 4 | Follows the rules with minor lapses. Reflection shows awareness of responsible testing. |
| **Developing** | 3 | Needs reminders about scope, data handling or disclosure. Reflection is superficial. |
| **Emerging** | 0–2 | Tests outside scope, uses real data, shares exploits irresponsibly, or shows no meaningful reflection. |

---

## 3. Score sheet

| Student / group | C1 /15 | C2 /20 | C3 /25 | C4 /20 | C5 /15 | C6 /5 | **Total /100** | Scaled mark |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| | | | | | | | | |

Teacher comments:

_______________________________________________________________________________

_______________________________________________________________________________

---

## 4. Minimum evidence requirements

These are guardrails, not automatic zeroes. Apply professional judgement and
record any adjustment.

| Requirement | Effect if missing |
|---|---|
| A test plan with scope and expected results | C1 capped at 7/15 |
| At least 20 executed test cases | C2 and C3 capped at 50% |
| At least 5 defect reports | C4 capped at 9/20 |
| Evidence (screenshot, request/response or recording) for each reported defect | That defect cannot earn C4 credit |
| A final recommendation on release readiness | C5 capped at 7/15 |
| Signed declaration / contribution statement (if required) | Result withheld until submitted |

**Academic integrity:** fabricated screenshots, copied reports or exploits
against systems outside the authorised scope are treated as a serious
assessment matter. Credit is withdrawn for the affected criterion and the
school's academic integrity procedure applies.

---

## 5. Coverage checklist (teacher use)

Use this to check whether the cohort, as a whole, has covered the main areas.
It is **not** a list of required answers, and students are not expected to find
every item.

| Area | Suggested evidence of coverage |
|---|---|
| Authentication | Valid/invalid login, logout, session behaviour |
| Input validation | Empty, boundary, long, malformed and special-character input |
| SQL injection | Login and/or search input tested safely; cause explained |
| Output handling | Reflected and/or stored script/HTML input tested |
| Access control | Student attempts to reach or use admin functions |
| Session/cookies | Cookie inspection and tampering |
| Sensitive data | Passwords or personal data exposed in UI, DB or files |
| Configuration | Public files, comments, headers, version/path disclosure |
| Error handling | Database/server error messages observed |
| CSRF / unsafe methods | Destructive action triggered by a crafted request |
| Usability | Keyboard, labels, focus, contrast, error clarity |
| Accessibility | Semantic structure, labels, alt text, zoom/reflow |
| Compatibility | At least two browsers and two screen sizes |
| Robustness | Reset during use, rapid refresh, large input |
| Evaluation | Risk-based prioritisation and feasible recommendations |

---

## 6. Group-work guidance

If the task is completed in groups:

- Each member must be able to explain **any** test or defect in the viva.
- The submission must identify individual contributions (for example, a short
  contribution table).
- The group mark may be adjusted individually by up to ±20% based on the viva,
  contribution evidence and observation of the testing process.
- A group may divide test areas, but the final evaluation and recommendations
  should be a shared, coherent piece of work.

---

## 7. Viva / moderation prompts

Use a short viva to confirm ownership and depth of understanding:

- “Show me the evidence for this defect and reproduce it.”
- “Why is this a security issue rather than just a bug?”
- “What would happen if the database were not reset every 5 minutes?”
- “Why did this input change the meaning of the SQL query?”
- “Why is escaping the output necessary even if the input was validated?”
- “How would you prioritise these three fixes if you had one day?”
- “Which of your tests was the weakest, and how would you improve it?”
- “What did you not have time to test?”

---

*Your teacher holds a separate answer key with the planted weaknesses and
suggested fixes. It will be released after the task is completed.*
