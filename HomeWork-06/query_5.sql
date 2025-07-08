-- Знайти які курси читає певний викладач.
-- Замініть 'Ім`я Викладача' на реальне ім'я викладача
SELECT
  t.fullname AS teacher_name,
  sb.name AS subject_name
FROM teachers AS t
JOIN subjects AS sb ON t.id = sb.teacher_id
WHERE
  t.fullname = 'Варфоломій Єщенко' -- Змініть на потрібне ім'я викладача
ORDER BY
  subject_name;
