
--
--  Usage:
--
--     sqlite3 ./databases/jumpack_20260427_014822.db  -i  statistics.sql
--

-- Set the column delimiter to space
.separator " "

select "Maximum charging current ", max(current_a), "A"
	from readings ;

select "Minimum charging current ", min(current_a), "A"
	from readings 
	where current_a > 0.25 ;

select "Maximum dark     current ", max(current_a), "A"
	from readings 
	where current_a < 0.10 ;

select "Charging began at    ", substr(timestamp,1,19)
	from readings
	where current_a > 0.25
	order by id
	limit 1;

select "Charging finished at ", substr(timestamp,1,19)
	from readings
	where current_a < 0.10
	order by id desc
	limit 1;

