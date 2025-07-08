-- Знайти студента із найвищим середнім балом з певного предмета.
-- Замініть 'Назва Предмета' на реальну назву предмета, наприклад 'Математика'
SELECT
  s.fullname,
  sb.name AS subject_name,
  ROUND(AVG(g.grade), 2) AS average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sb ON g.subject_id = sb.id
WHERE
  sb.name = 'Математика' -- Змініть на потрібний предмет
GROUP BY
  s.id,
  sb.name
ORDER BY
  average_grade DESC
LIMIT 1;
