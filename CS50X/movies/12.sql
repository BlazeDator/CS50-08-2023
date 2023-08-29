SELECT movies.title FROM movies,stars,people
WHERE stars.movie_id = movies.id
AND stars.person_id = people.id
AND stars.person_id = (SELECT id FROM people WHERE name LIKE "Johnny Depp")
AND movies.title IN
(SELECT movies.title FROM movies,stars,people
WHERE stars.movie_id = movies.id
AND stars.person_id = people.id
AND stars.person_id = (SELECT id FROM people WHERE name LIKE "Helena Bonham Carter"));