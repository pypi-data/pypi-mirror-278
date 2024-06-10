-- Update a batch item in the batch log, making sure to fail if the id and updated_at don't match, providing a guarantee of atomic operation
update
	batch_items as b
set
	last_started_at =
	  (case
		  when
			  b.status is distinct from %(in_progress_status)s
		  and
			  %(to_status)s = %(in_progress_status)s
		  then
			  now()
		  else
			  b.last_started_at
	  end)
  , last_finished_at =
	  (case
		  when
			  b.status = %(in_progress_status)s
		  and
			  %(from_status)s is distinct from %(in_progress_status)s
		  then
			  now()
		  else
			  b.last_finished_at
	  end)
	, worker_id = %(worker_id)s
	, status = %(to_status)s
	, updated_at = now()
where
	status = %(from_status)s
and
	id = (
		select
			id
		from
			batch_items
		where
			true
		and
			status = %(from_status)s
		order by
			  priority desc
			, updated_at asc
		limit
			1
	)
returning
	  id
	, priority
	, data
	, result
	, type
	, status
	, source
	, created_at
	, updated_at
;
