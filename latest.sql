--
-- Usage:   sqlite3  charging.db  < latest.sql
--

-- Print the most recent record
select printf("On %s, at %s, the curent was %12.8f A", 
		substr(timestamp,1,10), substr(timestamp,12,8), current_a)
	from readings
	order by timestamp desc
	limit 1;


