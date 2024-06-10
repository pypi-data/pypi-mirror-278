-- Get distinct batch status with counts
select
	  count(*) as count
	, status as status
from
	batch_items
group by
	status
;
