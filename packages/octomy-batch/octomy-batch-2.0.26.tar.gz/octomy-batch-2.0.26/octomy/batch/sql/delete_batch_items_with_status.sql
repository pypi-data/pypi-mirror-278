-- Delete batch items with given status
delete from
	batch_items
where
	status = %(status)s
;
