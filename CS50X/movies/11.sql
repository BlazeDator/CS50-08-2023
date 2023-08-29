SELECT title FROM movies,stars,ratings
WHERE movies.id = stars.movie_id
AND movies.id = ratings.movie_id
AND stars.person_id = (SELECT id FROM people WHERE name LIKE "Chadwick Boseman")
ORDER BY ratings.rating DESC LIMIT 5;