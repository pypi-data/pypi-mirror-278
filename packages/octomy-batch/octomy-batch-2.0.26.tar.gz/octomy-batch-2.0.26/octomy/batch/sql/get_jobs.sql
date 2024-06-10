-- Get batch items from batch log sorted by last active
select
	  id
	, priority
	, ttl_seconds
	, data
	, result
	, type
	, status
	, throttle_key
	, throttle_limit
	, throttle_period
	, source
	, error
	, updated_at - created_at as runtime
	, extract(epoch from (updated_at - created_at)) as runtime_ts
	, last_started_at
	, last_finished_at
	, updated_at
	, created_at
from
	batch_items
where
	true
and
	(%(id)s::int[] is null or id = any(%(id)s::int[]))
and
	(%(priority)s::int[] is null or priority = any(%(priority)s::int[]))
and
	(%(ttl_seconds)s::int[] is null or ttl_seconds = any(%(ttl_seconds)s::int[]))
and
	(%(type)s::varchar(255)[] is null or type = any(%(type)s::varchar(255)[]))
and
	(%(status)s::batch_status[] is null or status = any(%(status)s::batch_status[]))
and
	(%(throttle_key)s::varchar(63)[] is null or throttle_key = any(%(throttle_key)s::varchar(63)[]))
and
	(%(error)s::text[] is null or error = any(%(error)s::text[]))
and
	(%(source)s::text[] is null or source = any(%(source)s::text[]))
order by
	  updated_at desc
	, runtime asc
	, priority desc
limit
	%(limit)s
;
