-- Update status of all "in progress" jobs that already spent more than ttl time to "hung"
update
	batch_items
set
	  status = %(to_status)s
	, updated_at=  now()
	, last_finished_at = now()
where
	status = %(from_status)s
and
	ttl_seconds is not null
and
	ttl_seconds > 0
and
	extract('epoch' from ( now() - updated_at )) > ttl_seconds
;
