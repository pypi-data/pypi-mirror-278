-- Get distinct batch types with counts
select
	  count(*) as count
	, type as name
from
	batch_items
group by
	type
;
