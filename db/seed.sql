PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  username   TEXT NOT NULL UNIQUE,
  password   TEXT NOT NULL,
  role       TEXT NOT NULL DEFAULT 'student',
  created_at TEXT NOT NULL
);

CREATE TABLE contacts (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  phone      TEXT NOT NULL,
  email      TEXT NOT NULL DEFAULT '',
  notes      TEXT NOT NULL DEFAULT '',
  created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
  created_at TEXT NOT NULL
);

INSERT INTO users (username, password, role, created_at) VALUES
  ('admin', 'Admin@2026', 'admin',   '2026-09-01 09:00:00'),
  ('mchan', 'teach1234', 'teacher', '2026-09-01 09:05:00'),
  ('alice', 'alice1234', 'student', '2026-09-02 10:15:00'),
  ('bob',   'bob1234',   'student', '2026-09-02 10:20:00'),
  ('carol', 'carol1234', 'student', '2026-09-03 11:30:00');

INSERT INTO contacts (name, phone, email, notes, created_by, created_at) VALUES
  ('Chan Tai Man',     '9123 4567', 'chan.taiman@sunrise.edu.hk', 'F.6A class representative',                 3, '2026-09-05 09:10:00'),
  ('Lee Siu Ming',     '9234 5678', 'lee.siuming@sunrise.edu.hk', 'F.6B class representative',                 4, '2026-09-05 09:20:00'),
  ('Wong Ka Yan',      '9345 6789', 'wong.kayan@sunrise.edu.hk',  'F.5C class representative',                 5, '2026-09-06 10:05:00'),
  ('Miss Chan',        '9876 5432', 'mchan@sunrise.edu.hk',        'Staff Room 2 · Chemistry',                  2, '2026-09-06 11:00:00'),
  ('Mr Lau',           '9765 4321', 'lau.km@sunrise.edu.hk',       'Physics Laboratory, Room 208',              2, '2026-09-07 08:45:00'),
  ('IT Help Desk',     '2345 6789', 'ithelp@sunrise.edu.hk',       'Room 101 · staff and student support',       1, '2026-09-07 09:15:00'),
  ('Library Counter',  '3456 7890', 'library@sunrise.edu.hk',      'Open <em>Mon–Fri</em>, 08:00–17:00',          2, '2026-09-08 10:30:00'),
  ('School Nurse',     '4567 8901', 'nurse@sunrise.edu.hk',        'Medical room, next to the gym',              2, '2026-09-08 11:10:00'),
  ('Sports Office',    '5678 9012', 'sports@sunrise.edu.hk',       'After-school team enquiries',                2, '2026-09-09 14:00:00'),
  ('Alumni Association','6789 0123','alumni@sunrise.edu.hk',       'Please call before visiting',                1, '2026-09-10 09:00:00'),
  ('Chan Siu Ling',    '6123 4567', 'chan.siuling@sunrise.edu.hk', 'F.4A class representative',                 3, '2026-09-11 13:25:00'),
  ('David Ng',         '6987 6543', 'ng.ting@sunrise.edu.hk',      'F.6C class representative',                 4, '2026-09-12 15:40:00');
