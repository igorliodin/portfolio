# Movies

### Overview

This is a set of SQL queries to answer questions about a database of movies

### SQL Queries

The following tasks solved in the corresponding sql files:<br>
- **1.sql** - SQL query to list the titles of all movies released in 2008.
  - Outputs a table with a single column for the title of each movie.
- **2.sql** - SQL query to determine the birth year of Emma Stone.
  - Outputs a table with a single column and a single row (plus optional header) containing Emma Stone’s birth year. 
  - We assume that there is only one person in the database with the name Emma Stone.
- **3.sql** - SQL query to list the titles of all movies with a release date on or after 2018, in alphabetical order.
  - Outputs a table with a single column for the title of each movie. Movies released in 2018 are included, as well as movies with release dates in the future.
- **4.sql** - SQL query to determine the number of movies with an IMDb rating of 10.0.
  - Outputs a table with a single column and a single row (plus optional header) containing the number of movies with a 10.0 rating.
- **5.sql** - SQL query to list the titles and release years of all Harry Potter movies, in chronological order.
  - Outputs a table with two columns, one for the title of each movie and one for the release year of each movie.
  - We assume that the title of all Harry Potter movies will begin with the words “Harry Potter”, and that if a movie title begins with the words “Harry Potter”, it is a Harry Potter movie.
- **6.sql** - SQL query to determine the average rating of all movies released in 2012.
  - Outputs a table with a single column and a single row (plus optional header) containing the average rating.
- **7.sql** - SQL query to list all movies released in 2010 and their ratings, in descending order by rating. Movies with the same rating are ordered alphabetically by title.
  - Outputs a table with two columns, one for the title of each movie and one for the rating of each movie.
  - Movies that do not have ratings are not included in the result.
- **8.sql** - SQL query to list the names of all people who starred in Toy Story.
  - Outputs a table with a single column for the name of each person.
  - We assume that there is only one movie in the database with the title Toy Story.
- **9.sql** - SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.
  - Outputs a table with a single column for the name of each person.
  - People with the same birth year may be listed in any order.
  - Ignore people that have no birth year listed, so long as those who do have a birth year are listed in order.
  - If a person appeared in more than one movie in 2004, they should only appear in the results once.
- **10.sql** - SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.
  - Outputs a table with a single column for the name of each person.
- **11.sql** - SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.
  - Outputs a table with a single column for the title of each movie.
  - We assume that there is only one person in the database with the name Chadwick Boseman.
- **12.sql** - SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
  - Outputs a table with a single column for the title of each movie.
  - We assume that there is only one person in the database with the name Johnny Depp.
  - We assume that there is only one person in the database with the name Helena Bonham Carter.
- **13.sql** - SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
  - Outputs a table with a single column for the name of each person.
  - There may be multiple people named Kevin Bacon in the database. Only the Kevin Bacon born in 1958 is selected.
  - Kevin Bacon himself is not included in the resulting list.

