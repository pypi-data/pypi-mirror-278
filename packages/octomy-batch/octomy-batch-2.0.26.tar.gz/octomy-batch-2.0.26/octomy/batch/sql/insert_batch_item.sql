-- Insert a new batch item into log
insert into batch_items
	(
	  priority
	, ttl_seconds
	, data
	, result
	, type
	, status
	, throttle_key
	, throttle_limit
	, throttle_period
	, source
	)
values
	(
	  %(priority)s
	, %(ttl_seconds)s
	, %(data)s
	, %(result)s
	, %(type)s
	, %(status)s
	, %(throttle_key)s
	, %(throttle_limit)s
	, %(throttle_period)s
	, %(source)s
	)
on
	conflict(id)
do
	update
set
	  priority = %(priority)s
	, ttl_seconds = %(ttl_seconds)s
	, data = %(data)s
	, result = %(result)s
	, type = %(type)s
	, status = %(status)s
	, throttle_key = %(throttle_key)s
	, throttle_limit = %(throttle_limit)s
	, throttle_period = %(throttle_period)s
	, source = %(source)s
	, updated_at = now()
returning
	id
;
