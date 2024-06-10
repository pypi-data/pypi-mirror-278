-- Update status of a batch item in the batch log, making sure to fail if the id and updated_at don't match, providing a guarantee of atomic operation
-- Returns updated_at, so caller can check if it was updated or not (compare it to argument)
update
	batch_items as b
set
	  error = %(error)s
	, updated_at = now()
	, result =
		(case
			when
				%(result)s::text is null
			then
				b.result
			else
				%(result)s::text
		end)
	, last_started_at =
		(case
			when
				b.status is distinct from %(in_progress_status)s
			and
				%(status)s = %(in_progress_status)s
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
				%(status)s is distinct from %(in_progress_status)s
			then
				now()
			else
				b.last_finished_at
		end)
	, status = %(status)s
where
	id = %(id)s
and
	updated_at = %(updated_at)s
returning
	  id
	, updated_at
;
