-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
-- Замініть 'Назва Групи' та 'Назва Предмета' на реальні назви.
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
  gr.name = 'Назва Групи' -- Змініть на потрібну групу
  AND sb.name = 'Назва Предмета' -- Змініть на потрібний предмет
  AND g.grade_date = (
    SELECT MAX(g2.grade_date)
    FROM grades AS g2
    WHERE g2.student_id = s.id AND g2.subject_id = sb.id
  )
ORDER BY
  s.fullname;
