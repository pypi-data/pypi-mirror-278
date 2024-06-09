# movieback

A python library to manage your movies.

```python
>>> import movieback
>>> mdb = movieback.movieback("test.db", columns=[("title", "TEXT"), ("year", "INTEGER")])
>>> mdb.add_movie(title="Test movie", year=2010)
>>> mdb.add_movie(title="2nd video", year=2014)
>>> mdb.list_movies()
[(1, 'Test movie', 2010), (2, '2nd video', 2014)]
>>> mdb.search_movies("movie", column="title")
[(1, 'Test movie', 2010)]
>>> mdb.edit_movie(1, title="Test movie 2.0", year=2022)
>>> mdb.remove_movie(2)
```
