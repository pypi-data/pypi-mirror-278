import logging
import octomy.batch
import octomy.db
import pytest
import os
import pathlib


logger = logging.getLogger(__name__)

here = os.path.dirname(__file__)
data_dir = os.path.join(here, "data")

@pytest.mark.asyncio
async def test_batch_processor():
	config = {
		  'db-hostname':       os.environ.get("TEST_DB_HOSTNAME")
		, 'db-port':           os.environ.get("TEST_DB_PORT")
		, 'db-database':       os.environ.get("TEST_DB_DATABASE")
		, 'db-username':       os.environ.get("TEST_DB_USERNAME")
		, 'db-password':       os.environ.get("TEST_DB_PASSWORD")
		, 'batch-filter-root': f"{data_dir}/filters"
	}
	dbc, err = octomy.db.get_database(config, )
	assert dbc, err
	assert not err, err
	bp = octomy.batch.Processor(config, dbc, do_debug = False)
	await dbc.state(do_online = True)
	await bp.create_tables()
	await bp.state(do_online = True, show_full=False)
	await bp.state(do_online = True, show_full=True)

