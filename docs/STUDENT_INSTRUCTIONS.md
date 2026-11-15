# S6 ICT SBA — Task 2: Testing and Evaluation

## CampusConnect Phonebook

**Elective B1: Web Programming and Application**

| | |
|---|---|
| Student name | ______________________________ |
| Class / group | ______________________________ |
| Teacher | ______________________________ |
| Date issued | ______________________________ |
| Submission date | ______________________________ |

---

## 1. Scenario

Sunrise College is piloting **CampusConnect**, a small phonebook built by a
summer intern. Staff and students can sign in, search the campus directory and
add contact details. The school plans to launch it next term.

The IT panel has asked your team to act as independent testers. The prototype
has **not** been security reviewed and the intern has already left. Your job is
to:

1. plan a set of tests;
2. execute them and collect evidence;
3. report defects clearly and prioritise them; and
4. evaluate whether the application is fit for release.

You are **not** being asked to rewrite the application in this task. You are
being asked to find out what is wrong, prove it, explain the impact and
recommend what should happen next.

> The application is a **teaching prototype**. It contains weaknesses on
> purpose so that you have realistic things to find. All names, phone numbers
> and passwords are fictional.

---

## 2. Learning outcomes

This task draws on the Elective B1 content:

| B1 topic | What you will practise |
|---|---|
| Client–server communication | Testing HTTP requests and responses, GET vs POST, status codes |
| Web authoring and publishing | Inspecting HTML, CSS and JavaScript; responsive and accessible design |
| Server-side programming with PHP | Understanding how forms, sessions and server-side scripts behave |
| Database connection and SQL | Testing CRUD operations, search and data integrity |
| Cookies and sessions | Testing login state, cookie tampering and logout |
| Client-side and server-side validation | Comparing what the browser blocks with what the server accepts |
| Security awareness | Investigating SQL injection, cross-site scripting (XSS) and access control |
| Evaluation | Judging quality, risk and fitness for purpose |

**Curriculum reference:**
<https://spycit.notion.site/Elective-B1-Web-Programming-and-Application-c9960271cb1d43d1883b5bfaabdaef2e?pvs=74>

---

## 3. The system under test

CampusConnect has **three pages**:

| Page | URL | Purpose |
|---|---|---|
| Sign in / Register | `/index.php` | Create an account or sign in |
| Phonebook | `/board.php` | Search contacts, view the directory, add a contact |
| Admin console | `/admin.php` | Staff view of user accounts and contacts |

The teacher will give you the base URL, for example
`http://192.168.1.20:8080/`.

### Test accounts

Use only the student accounts provided by your teacher:

| Username | Password |
|---|---|
| `alice` | `alice1234` |
| `bob` | `bob1234` |
| `carol` | `carol1234` |

Do **not** use the teacher or administrator account. Part of the exercise is to
find out what happens when an ordinary user tries to reach areas they should
not be able to reach.

### Important: the database resets

The shared database is restored to its original state **every 5 minutes**.
Anything you add or change will disappear. This is deliberate so that every
class gets the same starting point.

- Take screenshots and copy HTTP requests **immediately** after a test.
- If a result disappears, repeat the test and capture the evidence faster.
- The reset is **not** a security control. Your report should not rely on it.

---

## 4. Your task

Work through the four parts below. Your teacher will tell you whether this is
individual or group work and the exact submission format.

### Part A — Test plan (before you test)

Write a short plan (about 1 page) containing:

- the scope: which pages, features and quality attributes you will test;
- what is **out of scope** (for example, attacking other systems or testing the
  school network);
- your test environment (browser, operating system, screen size);
- the test data you will use;
- a table of planned test cases.

Use this template:

| ID | Area | Objective | Preconditions | Steps | Expected result | Status | Evidence |
|---|---|---|---|---|---|---|---|
| T01 | Authentication | Valid student can sign in | Seeded account exists | 1. Open `/index.php` … | Redirected to phonebook | | |
| T02 | | | | | | | |

Aim for **at least 20 test cases**, including at least:

- 6 functional tests (sign in, register, search, add contact, admin access, logout);
- 5 input-validation or security tests;
- 3 authentication, session or access-control tests;
- 3 usability, accessibility or compatibility tests;
- 3 data-integrity, error-handling or robustness tests.

You may add more. A good test plan covers both **normal** and **abnormal** use.

### Part B — Test execution and evidence

Execute every planned test and record the **actual** result. For each test,
collect at least one piece of evidence:

- a screenshot showing the URL, page state and result;
- the exact HTTP request and response (DevTools → Network → right-click →
  **Copy as cURL**, or the request/status/response body);
- a short screen recording for multi-step behaviour;
- the exact input values you used.

Mark each test as **Pass**, **Fail** or **Blocked**. A test is not “Pass” just
because the page did not crash: it passes only if the actual result matches the
expected result.

#### Test ideas by area

Use these prompts to design your own cases. Do not simply copy them.

**Functional**

- Sign in with a valid account; sign out; try to use the browser Back button.
- Register a new account; check the password confirmation.
- Search by part of a name, a phone number and an email address.
- Add a contact; check that it appears in the list and survives a refresh.
- Try to reach the admin console as a student.
- Check what happens after the 5-minute reset.

**Input validation**

- Submit forms with empty fields, spaces only and very long values.
- Try boundary values for lengths and numeric fields.
- Enter an invalid phone number and an invalid email address.
- Try special characters: `'`, `"`, `<`, `>`, `&`, `--`, `%`, `_`.
- Remove or change HTML attributes with DevTools, then submit again.
- Send a request directly (for example with `curl`) that bypasses the form.

**Authentication, session and access control**

- Try a wrong password and a non-existent username. Compare the messages.
- Try SQL metacharacters in the username and password fields.
- Inspect cookies and local storage in DevTools. What does each value mean?
- Change a cookie value and reload the page.
- Open `/admin.php` directly without signing in.
- Sign in as a student, then try admin actions.

**Output handling**

- Enter HTML and JavaScript into text fields and see how it is displayed.
- Check whether the same input behaves differently in the search results, the
  contact table and the admin console.
- View the page source and inspect how your input was written into the HTML.

**Data storage and error handling**

- Look for places where passwords or personal data are displayed.
- Make a query fail and read the error message.
- Check whether the same error message reveals database or server details.
- Check whether duplicate usernames are handled cleanly.

**Configuration and files**

- Inspect the page source for comments, paths and version information.
- Try to discover files that should not be public. Think about common names
  such as configuration files, backups and key files.
- Check the HTTP response headers.

**Usability, accessibility and compatibility**

- Navigate the whole app using only the keyboard.
- Check labels, focus order, colour contrast and error messages.
- Test at phone, tablet and desktop widths.
- Test in at least two browsers (for example Chrome/Edge and Firefox).
- Check what happens when JavaScript is disabled.

**Performance and robustness**

- Refresh rapidly during a search.
- Submit a very long search term or a large number of requests (stay within
  the rules below).
- Check how the page behaves if the database is reset while you are using it.

### Part C — Defect reports

Write a separate defect report for **at least five** confirmed problems. Use
this template:

| Field | Content |
|---|---|
| **Defect ID** | D01 |
| **Title** | Short, specific summary |
| **Severity** | Critical / High / Medium / Low |
| **Location** | Page, feature, parameter or file |
| **Environment** | Browser, OS, screen size, account used |
| **Preconditions** | What must be true before reproducing |
| **Steps to reproduce** | Numbered, exact steps |
| **Expected result** | What should happen |
| **Actual result** | What actually happens |
| **Impact** | Who is affected and what can go wrong |
| **Evidence** | Screenshot / request / recording reference |
| **Recommendation** | A specific fix, not “improve security” |

#### Severity guide

| Severity | Meaning | Examples |
|---|---|---|
| **Critical** | Immediate, broad compromise; must be fixed before release | Authentication bypass, full database disclosure, remote code execution |
| **High** | Serious impact on users or data; fix urgently | Privilege escalation, stored XSS affecting many users, exposed secrets |
| **Medium** | Real weakness with limited or conditional impact | Reflected XSS, verbose error messages, missing server-side checks |
| **Low** | Minor quality or hardening issue | Cosmetic defect, missing cookie flag, unclear message |

Severity is not the same as likelihood. Explain both in your evaluation.

### Part D — Evaluation report

Write an evaluation of **about 1,000–1,500 words** (adjust to your teacher’s
instructions). Suggested structure:

1. **Executive summary** — Is CampusConnect ready to launch? Give a clear
   recommendation.
2. **Scope and method** — What you tested, how, and what you did not test.
3. **Results** — How many tests passed/failed; which areas are strongest and
   weakest.
4. **Defect analysis** — Group the defects by type and severity. Explain the
   risk using **likelihood × impact**.
5. **Recommendations** — Separate “must fix before launch”, “should fix soon”
   and “nice to have”. Make each recommendation specific and feasible.
6. **Evaluation against quality attributes** — functionality, security,
   usability, accessibility, compatibility, performance and maintainability.
7. **Limitations** — What your testing could not prove (for example, you did
   not run a full penetration test, or you only tested two browsers).
8. **Ethical and legal reflection** — Why authorisation, scope and responsible
   disclosure matter.
9. **Conclusion**.

A strong evaluation does **not** just list bugs. It explains which bugs matter
most, why, and what the school should do next.

---

## 5. Rules and ethics

You have permission to test **only** the CampusConnect instance provided by
your teacher.

- **Stay in scope.** Do not test the school network, the teacher's computer,
  other students' devices, or any other website.
- **Use fictional data.** Never enter real personal data, real passwords or
  real phone numbers.
- **Do not cause damage.** No denial-of-service, no flooding, no deleting other
  people's work, no brute-force beyond a few attempts.
- **Respect the shared instance.** Other classes may be using it. Keep tests
  small and repeatable.
- **Capture, do not exploit.** If you find a way to see data you should not
  see, take enough evidence to prove it. Do not download, keep or share the
  data.
- **Report privately.** Give your findings to your teacher. Do not post
  exploits, screenshots or working payloads on social media or public sites.
- **Stop and ask.** If you accidentally reach something that looks like a real
  system or real personal data, stop immediately and tell your teacher.
- **Legal awareness.** Unauthorised access to computer systems is a criminal
  offence in Hong Kong. Your permission is limited to this training instance
  and this task.

Marks are available for professional conduct, not just for finding bugs.

---

## 6. What to submit

| Item | Notes |
|---|---|
| Test plan | Before testing; includes scope and test case table |
| Test log | At least 20 executed cases with actual results and evidence |
| Defect reports | At least 5, using the template |
| Evaluation report | About 1,000–1,500 words |
| Evidence appendix | Screenshots, HTTP requests, recordings, clearly labelled |
| Presentation / viva | If required by your teacher (5–8 minutes) |
| Declaration | Individual/group contribution statement, if required |

Label every screenshot with the test or defect ID (for example `T07-login.png`
or `D02-search.png`). Unlabelled evidence is difficult to mark.

---

## 7. How you will be marked

The task is marked out of **100**, then scaled to your school's SBA allocation.
The criteria are:

| Criterion | Weight |
|---|---|
| Test planning and coverage | 15 |
| Functional and usability testing | 20 |
| Security and robustness testing | 25 |
| Defect documentation and evidence | 20 |
| Evaluation, prioritisation and recommendations | 15 |
| Professional conduct and reflection | 5 |

See [`RUBRIC.md`](RUBRIC.md) for the full descriptors.

---

## Appendix A — Test case template

| Field | Content |
|---|---|
| Test ID | T01 |
| Area | Authentication |
| Objective | Verify that a valid student can sign in |
| Preconditions | Seeded account `alice` exists; signed out |
| Test data | `alice` / `alice1234` |
| Steps | 1. Open `/index.php` … 2. Enter … 3. Click … |
| Expected | Redirect to `/board.php`; username shown |
| Actual | |
| Status | Pass / Fail / Blocked |
| Evidence | `T01-login.png` |

## Appendix B — Glossary

| Term | Meaning |
|---|---|
| **Client-side** | Code that runs in the browser (HTML, CSS, JavaScript) |
| **Server-side** | Code that runs on the web server (PHP, SQL) |
| **GET / POST** | HTTP methods; GET puts data in the URL, POST puts it in the request body |
| **Cookie** | A small key–value item stored by the browser and sent with requests |
| **Session** | Server-side state linked to a session identifier (usually a cookie) |
| **Authentication** | Proving who you are |
| **Authorisation** | Deciding what an authenticated user may do |
| **SQL injection** | Inserting SQL syntax through input so that the database executes unintended commands |
| **XSS** | Cross-site scripting; injecting script into a page viewed by another user |
| **CSRF** | Cross-site request forgery; making a logged-in user perform an unwanted action |
| **Prepared statement** | A parameterised SQL query that keeps data separate from SQL code |
| **Hashing** | A one-way transformation used to store passwords safely |
| **Server-side validation** | Validation performed on the server, which cannot be bypassed by the browser |
| **Responsive design** | Layout that adapts to different screen sizes |
| **SSR** | Server-side rendering; the server sends ready-to-display HTML |
