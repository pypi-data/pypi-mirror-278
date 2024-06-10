-- Get progression stats with totals for the given statuses
select
	  'total' as type
	, count(*) as count
	, (min( extract('epoch' from last_finished_at - last_started_at)) *1000 )::int as min
	, (avg( extract('epoch' from last_finished_at - last_started_at))*1000 )::int as avg
	, (percentile_cont(0.5) within group (order by extract('epoch' from b2.last_finished_at - b2.last_started_at)::float )*1000 )::int as med
	, (max( extract('epoch' from last_finished_at - last_started_at))*1000 )::int as max
	, (min( ttl_seconds ))::int as min_ttl
	, (max( ttl_seconds ))::int as max_ttl
from
	batch_items as b2
where 
	status = any(%(statuses)s)
and
	last_started_at is not null
and 
	last_finished_at  is not null
and
	last_finished_at > last_started_at

union

select
	  type
	, count(*) as count
	, (min( extract('epoch' from last_finished_at - last_started_at)) *1000 )::int as min
	, (avg( extract('epoch' from last_finished_at - last_started_at))*1000 )::int as avg
	, (percentile_cont(0.5) within group (order by extract('epoch' from b.last_finished_at - b.last_started_at)::float )*1000 )::int as med
	, (max( extract('epoch' from last_finished_at - last_started_at))*1000 )::int as max
	, (min( ttl_seconds ))::int as min_ttl
	, (max( ttl_seconds ))::int as max_ttl
from
	batch_items as b
where
	status = any(%(statuses)s)
and
	last_started_at is not null
and 
	last_finished_at  is not null
and
	last_finished_at > last_started_at
group by
	type
order by
	type
;
