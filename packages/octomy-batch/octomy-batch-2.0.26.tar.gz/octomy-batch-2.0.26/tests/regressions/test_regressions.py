import logging

logger = logging.getLogger(__name__)


def _test_true():
	logger.info("Dummy regressions test")
	return True
