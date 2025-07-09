-- Список курсів, які певному студенту читає певний викладач.
-- Замініть 'Ім`я Студента' та 'Ім`я Викладача' на реальні імена.
SELECT
  s.fullname AS student_name,
  t.fullname AS teacher_name,
  sb.name AS subject_name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sb ON g.subject_id = sb.id
JOIN teachers AS t ON sb.teacher_id = t.id
WHERE
  s.fullname = 'Ім`я Студента' -- Змініть на потрібне ім'я студента
  AND t.fullname = 'Варфоломій Єщенко' -- Змініть на потрібне ім'я викладача
GROUP BY
  s.fullname,
  t.fullname,
  sb.name
ORDER BY
  subject_name;
