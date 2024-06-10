-- Create batch_status enum if it does not exist
do $$ begin
create type "batch_status" as enum (
	  'pending'
	, 'in-progress'
	, 'hung'
	, 'done'
	, 'failed'
);
exception
	when  duplicate_object then null;
end $$;
