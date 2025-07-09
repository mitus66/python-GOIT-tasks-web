-- Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT
  ROUND(AVG(grade), 2) AS overall_average_grade
FROM grades;
