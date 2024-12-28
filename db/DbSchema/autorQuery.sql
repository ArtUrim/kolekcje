SELECT 
    b.title,
    GROUP_CONCAT(a.name) as authors,
    p.name as publisher,
    b.release_date,
    s.name as series_name
FROM Books b
LEFT JOIN bookAuthors ba ON b.id = ba.book_id
LEFT JOIN Authors a ON ba.author_id = a.id
LEFT JOIN publisher p ON b.publisher_id = p.id
LEFT JOIN series s ON b.series_id = s.id
WHERE a.name = "Joseph Sheridan Le Fanu"
GROUP BY b.id, b.title, p.name, b.release_date, s.name;
