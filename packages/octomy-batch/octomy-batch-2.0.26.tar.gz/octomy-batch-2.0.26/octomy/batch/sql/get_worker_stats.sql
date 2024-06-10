-- Get statistics for each worker (inferred)
select
	worker_id
	, count(*) as job_count
	, sum( extract('epoch' from (last_finished_at - last_started_at))*1000)::int / count(*) as ms_per_job
	, ((count(*) ) / max(extract('epoch' from(now()-last_started_at))/(60*60) ) )  as jobs_per_hour
	, min(last_started_at) as first_active
	, max(last_started_at) as current_job_started
	, max(last_finished_at) as last_job_finished
	, max(extract('epoch' from(now()-last_started_at)) *1000)::int as run_time
	, sum( extract('epoch' from (last_finished_at - last_started_at))*1000)::int as work_time
	, max(extract('epoch' from(now()-last_started_at))*1000)::int - sum( extract('epoch' from (last_finished_at - last_started_at) ) *1000)::int as idle_time
	, (max(last_started_at)  > max(last_finished_at))::boolean as is_active
from
	batch_items as b
where
	true
and
	worker_id is not null
and
	now() - last_finished_at < interval '2 hours'
group by
	worker_id
order by
	3 asc, 2 desc
limit
	%(limit)s
;
