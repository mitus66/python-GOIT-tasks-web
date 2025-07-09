-- Знайти оцінки студентів у окремій групі з певного предмета.
-- Замініть 'Назва Групи' та 'Назва Предмета'
SELECT
  s.fullname AS student_name,
  gr.name AS group_name,
  sb.name AS subject_name,
  g.grade,
  g.grade_date
FROM students AS s
JOIN groups AS gr ON s.group_id = gr.id
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sb ON g.subject_id = sb.id
WHERE
  gr.name = 'Group B' -- Змініть на потрібну групу
  AND sb.name = 'Хімія' -- Змініть на потрібний предмет
ORDER BY
  s.fullname,
  g.grade_date;
