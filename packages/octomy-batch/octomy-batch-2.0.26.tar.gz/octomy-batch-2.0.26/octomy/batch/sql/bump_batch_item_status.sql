-- Simplified version of bump_batch_item where status is updated, no questions asked
update
	batch_items as b
set
	  last_started_at =
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
	, updated_at = now()
where
	id = %(id)s
;
