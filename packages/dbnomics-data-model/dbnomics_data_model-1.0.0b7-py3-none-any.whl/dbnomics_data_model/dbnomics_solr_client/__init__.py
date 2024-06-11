from more_itertools import one
from pysolr import Solr
from solrq import Q

from dbnomics_data_model.dbnomics_solr_client.constants import SERIES_TYPE
from dbnomics_data_model.dbnomics_solr_client.model.series_solr_doc import SeriesSolrDoc
from dbnomics_data_model.json_utils import parse_json_data
from dbnomics_data_model.model.identifiers.series_id import SeriesId


class DBnomicsSolrClient:
    def __init__(self, *, solr_client: Solr) -> None:
        self._solr_client = solr_client

    def find_series(self, series_id: SeriesId) -> SeriesSolrDoc | None:
        query = Q(id=str(series_id), type=SERIES_TYPE)
        results = self._solr_client.search(query)
        try:
            result = one(results)
        except ValueError:
            return None
        return parse_json_data(result, type_=SeriesSolrDoc)
