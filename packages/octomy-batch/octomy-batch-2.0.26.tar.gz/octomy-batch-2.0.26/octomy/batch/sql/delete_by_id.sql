-- Delete single item by id
delete from
	batch_items
where
	id = %(id)s
;
