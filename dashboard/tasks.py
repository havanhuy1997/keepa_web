from dashboard import models
import utils.keepa as ut_keepa
import utils.dt as ut_dt


def fetch_data_for_category(category):
    task = models.Task.objects.create(category=category, started=ut_dt.get_time_now())
    search = ut_keepa.CategorySearch(task)
    try:
        search.get_all_asins()
    except Exception as e:
        search.logger.error(str(e))
    finally:
        task.ended = ut_dt.get_time_now()
        task.save()
