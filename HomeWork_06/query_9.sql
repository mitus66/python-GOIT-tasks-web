-- Знайти список курсів, які відвідує студент.
-- Замініть 'Ім`я Студента' на реальне ім'я студента
SELECT
  s.fullname AS student_name,
  sb.name AS subject_name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sb ON g.subject_id = sb.id
WHERE
  s.fullname = 'Ільєнко Ада Мартинівна' -- Змініть на потрібне ім'я студента
GROUP BY
  s.fullname,
  sb.name
ORDER BY
  subject_name;
