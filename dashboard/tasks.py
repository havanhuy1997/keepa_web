import utils.keepa as ut_keepa
import utils.dt as ut_dt
import utils.log as ut_log


def start_task(task):
    logger = ut_log.get_logger_for_task(task)
    try:
        if task.min and task.max:
            filters =  [{"key": ut_keepa.CategorySearch.FILTER_KEYS[0], "min": task.min, "max": task.max}]
            search = ut_keepa.CategorySearch(task, filters=filters)
        else:
            search = ut_keepa.CategorySearch(task)
        search.get_all_asins()
    except Exception as e:
        logger.error(str(e))
    finally:
        task.ended = ut_dt.get_time_now()
        task.save()
