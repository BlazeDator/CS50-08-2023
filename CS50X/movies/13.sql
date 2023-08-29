SELECT people.name FROM movies,stars,people
WHERE stars.movie_id = movies.id
AND stars.person_id = people.id
AND movies.title IN
(SELECT movies.title FROM movies,stars,people
WHERE stars.movie_id = movies.id
AND stars.person_id = people.id
AND stars.person_id = (SELECT id FROM people WHERE name LIKE "Kevin Bacon")
AND people.birth = 1958)
AND people.name NOT LIKE "Kevin Bacon";