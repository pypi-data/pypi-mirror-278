from unittest import TestCase
from unittest.mock import patch
from vizportal import VizportalRequestOptions, FilterClauseBuilder
from vizportal import PayloadBuilder
from vizportal import VizportalPager
from vizportal import Endpoints
import tableauserverclient as TSC

# create a test for getting workbooks
class TestGetWorkbooks(TestCase):
    # create a mock server
    @patch('tableauserverclient.server.Server')
    def test_get_workbooks(self, mock_server):
        # create a mock auth
        mock_auth = TSC.TableauAuth()
        # create a mock payload builder
        mock_payload = PayloadBuilder()
        # create a mock workbook endpoint
        mock_workbook_endpoint = Endpoints.Get.Workbooks
        # add the mock method
        mock_payload.add_method(mock_workbook_endpoint)
        # add the mock page
        mock_payload.add_page(0, 5)
        # create a mock filter clause builder
        mock_filter = FilterClauseBuilder()
        # add the mock clause
        mock_filter.addClause(VizportalRequestOptions.Operator.Equals, VizportalRequestOptions.Field.WorkbookConnFilter, "allExtracts")
        # add the mock filter
        mock_payload.add_filter(mock_filter)
        # build the mock payload
        mock_payload = mock_payload.build()
        # create a mock results
        mock_results = VizportalPager(mock_server, mock_payload).get_results()
        # assert the mock payload
        self.assertEqual(mock_payload, mock_payload)
        # assert the mock results
        self.assertEqual(mock_results, mock_results)
