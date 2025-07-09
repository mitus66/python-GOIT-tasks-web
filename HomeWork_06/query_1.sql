-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT
  s.fullname,
  ROUND(AVG(g.grade), 2) AS average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
GROUP BY
  s.id
ORDER BY
  average_grade DESC
LIMIT 5;
