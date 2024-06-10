-- Update status of all jobs with from_status to to_status
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
	, status = %(to_status)s
	, updated_at = now()
where
	status = %(from_status)s
;
