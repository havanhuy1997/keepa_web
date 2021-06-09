import utils.keepa as ut_keepa
import utils.dt as ut_dt
import utils.log as ut_log


def start_task(task):
    logger = ut_log.get_logger_for_task(task)
    try:
        search = ut_keepa.CategorySearch(task)
        search.get_all_asins()
    except Exception as e:
        logger.error(str(e))
    finally:
        task.ended = ut_dt.get_time_now()
        task.save()
