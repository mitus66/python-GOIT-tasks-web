-- Знайти середній бал у групах з певного предмета.
-- Замініть 'Назва Предмета' на реальну назву предмета, наприклад 'Фізика'
SELECT
  gr.name AS group_name,
  sb.name AS subject_name,
  ROUND(AVG(g.grade), 2) AS average_grade
FROM groups AS gr
JOIN students AS s ON gr.id = s.group_id
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sb ON g.subject_id = sb.id
WHERE
  sb.name = 'Фізика' -- Змініть на потрібний предмет
GROUP BY
  gr.name,
  sb.name
ORDER BY
  gr.name;
