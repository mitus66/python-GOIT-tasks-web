-- Знайти список студентів у певній групі.
-- Замініть 'Назва Групи' на реальну назву групи, наприклад 'Group A'
SELECT
  s.fullname AS student_name,
  gr.name AS group_name
FROM students AS s
JOIN groups AS gr ON s.group_id = gr.id
WHERE
  gr.name = 'Group A' -- Змініть на потрібну групу
ORDER BY
  student_name;
