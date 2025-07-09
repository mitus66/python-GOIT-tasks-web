-- Середній бал, який певний викладач ставить певному студентові.
-- Замініть 'Ім`я Студента' та 'Ім`я Викладача' на реальні імена.
SELECT
  s.fullname AS student_name,
  t.fullname AS teacher_name,
  ROUND(AVG(g.grade), 2) AS average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sb ON g.subject_id = sb.id
JOIN teachers AS t ON sb.teacher_id = t.id
WHERE
  s.fullname = 'Ім`я Студента' -- Змініть на потрібне ім'я студента
  AND t.fullname = 'Ім`я Викладача' -- Змініть на потрібне ім'я викладача
GROUP BY
  s.fullname,
  t.fullname;
