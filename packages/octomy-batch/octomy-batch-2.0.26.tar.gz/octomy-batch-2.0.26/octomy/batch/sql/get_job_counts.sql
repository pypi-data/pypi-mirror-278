-- Get distinct batch status+type with counts
select
	  type
	, status
	, count(*)
from
	batch_items
group by
	  type
	, status
order by
	  type
	, status
;
