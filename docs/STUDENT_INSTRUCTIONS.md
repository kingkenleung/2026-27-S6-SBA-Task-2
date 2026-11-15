# S6 ICT SBA — Task 2: Testing and Evaluation

## CampusConnect Phonebook

**Elective B1: Web Programming and Application**

**Time:** about 10 hours · **Marks:** 15

| | |
|---|---|
| **Live app** | **http://34.92.173.24:8080/** |
| **Source code** | **https://github.com/kingkenleung/2026-27-S6-SBA-Task-2** |
| Student name | ______________________________ |
| Class / group | ______________________________ |
| Teacher | ______________________________ |
| Date issued | ______________________________ |
| Submission date | ______________________________ |

---

## 1. Scenario

Sunrise College is piloting **CampusConnect**, a phonebook built by a summer intern. It is live and has not been security reviewed. You are the testers: test it, report defects, suggest improvements and decide whether it is ready for release. You are **not** rewriting the app.

You can use the app **at home or at school**. All records are fictional. You may inspect the source code on GitHub, but every finding must be confirmed in the running app.

## 2. The app

| Page | Address | Purpose |
|---|---|---|
| Sign in / Register | `/index.php` | Create an account or sign in |
| Phonebook | `/board.php` | Search, view and add contacts |
| Admin console | `/admin.php` | Staff view of users and contacts |

Student accounts: `alice` / `alice1234`, `bob` / `bob1234`, `carol` / `carol1234`. Do not use the administrator account.

The database resets every 5 minutes. Changes are temporary, so take screenshots and copy HTTP requests immediately.

## 3. What to do (about 10 hours)

| Stage | Time |
|---|---|
| Explore the app and read this brief | 1 h |
| Write 15 test plans | 2 h |
| Run the tests and collect evidence | 3 h |
| Write defect reports and suggestions | 2 h |
| Write the evaluation | 1.5 h |
| Final check and submit | 0.5 h |

1. **Test plan — 15 test cases.** Choose 15 tests covering the B1 topics: pages and forms, search, login and cookies, validation, database, security and usability. For each, write the ID, what you will test, the steps and the expected result.
2. **Test log — 15 entries.** Run every test. Record the actual result and evidence (screenshot or HTTP request). Mark each test **Pass** or **Fail**.
3. **Defects and suggestions.** Report the main defects you find (aim for **3–5**). For each, give steps to reproduce, evidence and a suggested fix.
4. **Evaluation — about 400–600 words.** Summarise the results, explain the main risks, prioritise the fixes, comment on the high-level design and give a clear release recommendation.
5. **Submit** your 15 plans, 15 logs, defect reports and suggestions, evaluation and evidence.

## 4. Test ideas — you decide

Do not wait for a list of bugs. Use the B1 topics and the source code to design your own tests. Think about:

- Pages and forms
- Input and validation
- Login and session
- Output and data
- Design and usability

Strong answers explain **why** each test matters and follow up on unexpected results. Weaker answers only test the happy path.

## 5. Sample test plan, log and suggestion

| ID | Plan | Log and evidence | Result | Suggestion |
|---|---|---|---|---|
| T02 | Search for a contact using a single quote (`'`). Expected: no error, zero or matching results. | The page showed “Database error: SQLSTATE…” (screenshot `T02.png`). | Fail | Use a prepared statement with bound parameters and show a generic error to the user. |

Use this format for all 15 cases. For a passed test, the suggestion can be “No change needed” or a small improvement.

## 6. Defect report and suggestions

Use this compact format for each defect:

| Field | Content |
|---|---|
| ID | D01 |
| What is wrong | A short, specific description |
| Steps to reproduce | 1. … 2. … 3. … |
| Evidence | Screenshot or HTTP request |
| Suggested fix | A specific change, not “improve security” |

You may also suggest **high-level design** improvements, not just code fixes. Examples:

- the app is reached by a raw public IP with no registered domain or HTTPS;
- the web server, PHP and database share one small VM;
- there is no backup, monitoring or audit log;
- staff and student roles are not clearly separated.

## 7. What to submit

- 15 test plans and 15 test logs (one row per test: plan, actual result, evidence, Pass/Fail).
- Defect reports for the main defects (aim for 3–5), each with a suggested fix.
- A short evaluation (about 400–600 words): results, risks, priorities, high-level design and release recommendation.
- Evidence: labelled screenshots or HTTP requests, attached or linked from your logs.

## 8. Marking (15 marks)

| Criterion | Marks |
|---|---|
| Test plan and coverage (15 cases) | 3 |
| Test log, execution and evidence | 5 |
| Defect reports and suggestions | 4 |
| Evaluation, high-level design and release recommendation | 3 |
| **Total** | **15** |

Your teacher will use the detailed rubric. Credit is for systematic testing and clear evidence, not for finding every bug.

## 9. Rules

- Test only <http://34.92.173.24:8080/>.
- Use fictional data; never enter real personal data.
- Do not attack the school network or other systems.
- Do not flood the app or delete other people's work.
- Report privately; do not post exploits publicly.
- If you find something serious, stop and tell your teacher.
- Unauthorised access to computer systems is a criminal offence in Hong Kong.
