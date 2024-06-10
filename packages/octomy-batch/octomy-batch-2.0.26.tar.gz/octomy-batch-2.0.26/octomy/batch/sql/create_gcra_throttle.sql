-- Inspired by https://dev.to/astagi/rate-limiting-using-python-and-redis-58gk
-- Create a function to keep track of throttling of batch items
-- NOTE: Throttling works by an algorithm called Generic Cell Rate Algoritm (GCRA for short).
--       The function is called for a key, and will return an integer number of milliseconds to wait for the key to become unlimited
--       The function can be called with do_book=true to actually perform booking if the key is unlimited
--       The parameters limit_count and period_millis are used to specify the limit where
--       limit_count is the number of actions allowed over the time interval of period_millis
-- function that returns the number of milliseconds to wait before the given throttle_key is available. If the value returned is <=0 that means you just got lucky and no throttle was necessary for that key at this point.
drop function if exists gcra_throttle (varchar, integer, integer, boolean);
create or replace function gcra_throttle (throttle_key varchar(63), limit_count integer, period_millis integer, do_book boolean) returns bigint as $$
declare
-- Holds current time in milliseconds since epoch at the entry of the function
now_millis bigint;
-- Holds our current value of TAT in milliseconds since epoch
tat_millis bigint;
-- Holds the return value for "how long should we wait before invoking our throttled action?" in milliseconds
left_millis bigint;
begin

-- Trivial reject: when throttle_key is not set we return 0 to signify no rate limiting needed
if (throttle_key = '') is not false then
return 0;
end if;

-- Get current time in milliseconds since epoch
select extract(epoch from now()) * 1000 into now_millis;

-- Make sure our working table is ready
create unlogged table if not exists throttle_tat(
key varchar(63) primary key,
millis bigint
);

-- Hold an exclusive lock on the table to avoid race conditions
lock table throttle_tat in exclusive mode;

-- Get stored value for tat, initializing it to 0 if it was not set 
select t.millis into tat_millis from throttle_tat t where t.key = $1;
if tat_millis is null then
tat_millis := now_millis;
insert into throttle_tat (key, millis) values ($1, tat_millis);
end if;

-- Calculate how many milliseconds we should wait before performing our action.
-- NOTE: Zero or negative values means we don't need to wait
left_millis := (tat_millis - now_millis)  -  (period_millis - (period_millis / limit_count));

-- We waited long enough, perform our booking if so desired
if do_book and left_millis <= 0 then
update throttle_tat t set millis = greatest(tat_millis, now_millis) + (period_millis / limit_count) where t.key = $1;
end if;
return left_millis;
end
$$ language plpgsql;
