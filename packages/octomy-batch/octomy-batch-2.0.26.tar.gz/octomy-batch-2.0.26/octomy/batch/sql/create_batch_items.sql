-- Create a table to keep track of batch items
create table if not exists "batch_items" (
	  id serial primary key
	, priority int not null default 50
	, ttl_seconds int
	, data text
	, result text
	, type varchar(255)
	, status batch_status
	, throttle_key varchar(63)
	, throttle_limit integer
	, throttle_period integer
	, source text
	, error text
	, worker_id varchar(63) default null
	, last_started_at timestamptz
	, last_finished_at timestamptz
	, created_at timestamptz not null default now()
	, updated_at timestamptz not null default now()
);
comment on column batch_items.id is 'Unique internal id for this batch item';
comment on column batch_items.priority is 'The batch item''s priority. Tasks with a higher number for priority will be picked first by executors. Tasks with the same number are equally important.';
comment on column batch_items.ttl_seconds is 'The batch item''s ttl (time to live) in seconds. When a job has spent more time in the state "in progress" than it''s TTL, it will be transitioned to the "hung" state indicating that it should be ignored until it has been expected by operator.';
comment on column batch_items.data is 'The batch item''s data. Depends entirely on the type. Could for example be the URL to scrape for a site_scrape item';
comment on column batch_items.result is 'The batch item''s result data. Depends entirely on the type. Could for example be the HTML scraped for the input URL for a site_scrape item';
comment on column batch_items.type is 'The batch item''s type such as order_scrape or site_scrape';
comment on column batch_items.status is 'The batch item''s status such as pending, in-progress or done';
comment on column batch_items.throttle_key is 'When set enables throttling between all items that have the same key';
comment on column batch_items.throttle_limit is 'When throttle_key is set, this specifies the number of items that can be processed over throttle_period';
comment on column batch_items.throttle_period is 'When throttle_key is set, this specifies the period over which throttle_limit items may be processed';
comment on column batch_items.source is 'The batch item''s source. Spesifically which component registered it.';
comment on column batch_items.error is 'The batch item''s error message. Should be None unless status is "failed", in which it case it should be a descriptive error message.';
comment on column batch_items.worker_id is 'The ID of the worker that last processed this item, or Null if it was not yet processed.';
comment on column batch_items.last_started_at is 'When the batch item last started (entered in_progress state)';
comment on column batch_items.last_finished_at is 'When the batch item last finished (exited in_progress state)';
comment on column batch_items.created_at is 'When the batch item was first created';
comment on column batch_items.updated_at is 'When the batch item was last updated';
