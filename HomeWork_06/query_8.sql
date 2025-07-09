-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
-- Замініть 'Ім`я Викладача' на реальне ім'я викладача
SELECT
  t.fullname AS teacher_name,
  ROUND(AVG(g.grade), 2) AS average_grade_by_teacher
FROM teachers AS t
JOIN subjects AS sb ON t.id = sb.teacher_id
JOIN grades AS g ON sb.id = g.subject_id
WHERE
  t.fullname = 'Варфоломій Єщенко' -- Змініть на потрібне ім'я викладача
GROUP BY
  t.fullname;
