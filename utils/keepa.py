import copy
import time

from dashboard import models, tasks

import utils.net as ut_net
import utils.log as ut_log


class KeepaClient:
    API_URL = 'https://api.keepa.com'
    KEY = '8da4mst49dao49tl4775b781sd0o2p22u7i780iv82dd56qo0o8b72d4j4vepafe'
    US_DOMAIN = 1
    MIN_REQUIRED_TOKEN = 200
    WAIT_TOKEN_SECONDS = 60
    token_left = None

    def __init__(self, logger, domain=US_DOMAIN) -> None:
        self.token_left = self._number_token()
        self.logger = logger
        self.domain = domain

    def _request(self, url):
        while self.token_left < self.MIN_REQUIRED_TOKEN:
            self.logger.warn(f"Low token: {self.token_left}. Waiting for token to be restored")
            time.sleep(self.WAIT_TOKEN_SECONDS)
            self.token_left = self._number_token()
        r = ut_net.get_json(url)
        self.token_left = r["tokensLeft"]
        return r

    def _number_token(self):
        url = f"{self.API_URL}/query?key={self.KEY}"
        r = ut_net.get_json(url)
        return r["tokensLeft"]
    
    def product_finder(self, params):
        url = f"{self.API_URL}/query?key={self.KEY}&domain={self.domain}&selection={ut_net.quote_dict(params)}"
        return self._request(url)

    def request_product_with_asin(self, asin):
        url = f"{self.API_URL}/product?key={self.KEY}&domain={self.domain}&asin={asin}"
        data = self._request(url)
        products = data.get("products")
        if products:
            return products[0]
        return {}


class CategorySearch:
    ASIN_PER_PAGE = 10000
    STEP_RANGE = 1000
    FILTER_KEYS = ["current_LISTPRICE", "current_SALES"]
    NUMBER_PARTS_DEVIDED_BIG_RANGE = 3
    DELETED_KEYS = [
        'perPage', 'page', 'rootCategory', 'sort',
        'current_LISTPRICE_lte', 'current_LISTPRICE_gte',
        'current_SALES_lte', 'current_SALES_gte',
    ]

    def __init__(
        self,
        task,
        filters=[{"key": FILTER_KEYS[0], "min": 0, "max": STEP_RANGE}]
    ) -> None:
        """
        filters: [{key: current_LISTPRICE, min: 1000, max: 1200}, {key: current_LISTPRICE}]
        """
        self.asins = []
        self.logger = ut_log.get_logger_for_task(task)
        self.filters = filters
        self.keepa_client = KeepaClient(self.logger, domain=task.category.domain)
        self.task = task
        self.category_id = task.category.id
        self._first_run()
        self.main_filter_key = filters[-1]["key"]
    
    def _add_category_filter(self, filter):
        if self.task.category.filter:
            for k, v in self.task.category.filter:
                if k not in self.DELETED_KEYS:
                    filter[k] = v
        return filter

    def _get_dict_for_beginning_filters(self):
        d = {
            "sort": []
        }
        for fil in self.filters[0:-1]:
            key = fil["key"]
            d[f"{key}_lte"] = fil["max"]
            d[f"{key}_gte"] = fil["min"]
            d["sort"].append([key, "asc"])
        return d

    def _first_run(self) -> None:
        data = self.keepa_client.product_finder({
            "rootCategory": self.category_id,
            "perPage": self.ASIN_PER_PAGE,
            **self._add_category_filter(self._get_dict_for_beginning_filters()),
        })
        self.total_asins = data["totalResults"]
        # Save data for task in empty beginning filter 
        if len(self.filters) == 1:
            self.task.total_asins = self.total_asins
            self.task.save()
        self.logger.info(f"Total asin: {self.total_asins}")
        self._save_asins_from_data(data)

    def _save_asins_from_data(self, data: dict) -> None:
        if "asinList" not in data:
            raise Exception(f"Response does not have asins: {data}")
        new_asins = []
        for asin in data["asinList"]:
            if asin not in self.asins:
                self.asins.append(asin)
                new_asins.append(asin)
        for asin in new_asins:
            if not models.Product.objects.filter(asin=asin).first():
                self.logger.info(f"Getting data for asin {asin}")
                data = self.keepa_client.request_product_with_asin(asin)
                try:
                    product = models.Product(asin=asin, rootCategory=self.task.category)
                    product.set_data(data)
                    product.save()
                except Exception as e:
                    self.logger.warn(f"Fail to save {asin}: {str(e)}")

    def _query_with_range(self, range: tuple) -> int:
        self.logger.info(f"Getting asins with {self.main_filter_key}={range}")
        query = {
            "rootCategory": self.category_id,
            "perPage": self.ASIN_PER_PAGE,
            **self._get_dict_for_beginning_filters(),
            f"{self.main_filter_key}_lte": range[1],
            f"{self.main_filter_key}_gte": range[0],
        }
        query["sort"].append([self.main_filter_key, "asc"])
        query = self._add_category_filter(query)
        data = self.keepa_client.product_finder(query)
        self._save_asins_from_data(data)
        return len(data["asinList"])

    def _query_with_big_range(self, _range: tuple):
        self.logger.warn(f"Big range {self.main_filter_key}={_range}")
        delta = (_range[1] - _range[0]) / self.NUMBER_PARTS_DEVIDED_BIG_RANGE
        for i in range(self.NUMBER_PARTS_DEVIDED_BIG_RANGE):
            start = round(_range[0] + i * delta, 2)
            end = round(start + delta, 2)
            if self._query_with_range((start, end)) == self.ASIN_PER_PAGE:
                if start == end:
                    # Check if reached all filters
                    if len(self.filters) == len(self.FILTER_KEYS):
                        self.log("Reached max filter keys")
                    else:
                        # Add new filter
                        filters = copy.deepcopy(self.filters)
                        filters[-1]["min"] = start
                        filters[-1]["max"] = end
                        filters.append(
                            {"key": self.FILTER_KEYS[len(filters)], "min": 0, "max": self.STEP_RANGE}
                        )
                        category_search_with_begin_filters = CategorySearch(self.task, filters=filters)
                        category_search_with_begin_filters.get_all_asins()
                else:
                    self._query_with_big_range((start, end))

    def get_all_asins(self) -> None:
        start = self.filters[-1]["min"]
        end = self.filters[-1]["max"]
        while len(self.asins) < self.total_asins:
            if len(self.filters) == 1:
                self.task.min = start
                self.task.max = end
                self.task.save()
            total_result_for_this_range = self._query_with_range((start, end))
            if total_result_for_this_range == self.ASIN_PER_PAGE:
               self._query_with_big_range((start, end))
            else:
                start = end
                end = start + self.STEP_RANGE
