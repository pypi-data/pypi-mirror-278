from typing import Dict, List, Optional, Any
from vizportal.req_options import FilterClauseBuilder, SortBuilder


class PayloadBuilder:
    """Builds a payload for a request to the Vizportal API.

    ...

    Attributes
    ----------
    _payload : Dict[str, Union[str, Dict[str, Union[int, Dict[str, int]], List[str]]]]
        Protected internal instance of the payload.

    Properties
    ----------
    payload : Dict[str, Union[str, Dict[str, Union[int, Dict[str, int]], List[str]]]]
        The payload to be sent to the server.

    Methods
    -------
    add_method(method: str)
        Adds a method to the payload.
    add_filter(filter_clause_builder: FilterClauseBuilder)
        Adds a filter to the payload.
    add_order(order_clause_builder: SortBuilder)
        Adds an order to the payload.
    add_page(start_index: int, max_items: int)
        Adds a page to the payload.
    add_stat_fields(stat_fields: List[str])
        Adds stat fields to the payload.
    """

    def __init__(
        self, dict_payload: Optional[Dict[str, Any]] = None
    ):
        self._payload: Dict[str, Any] = self._compose_payload_from_dict(dict_payload)

    def __repr__(self) -> str:
        return f"Payload: {self.payload}"

    @property
    def payload(
        self,
    ) -> Dict[str, Any]:
        if not self._payload["method"]:
            raise ValueError("No method specified for payload.")

        if not self._payload["params"].get("page"):
            self.add_page()

        return self._payload

    def _compose_payload_from_dict(
        self, dict_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        "Composes a payload from a dictionary if it is passed in explicitly"
        if isinstance(dict_payload, dict) and dict_payload:
            return dict_payload
        else:
            return {"method": "", "params": {}}

    def add_method(self, method: str):
        self._payload["method"] = method

    def add_filter(self, filter_clause_builder: FilterClauseBuilder):
        self._payload["params"]["filter"] = filter_clause_builder.clauses

    def add_key_value_param(self, key: str, value: str):
        self._payload["params"][key] = value

    def add_order(self, order_clause_builder: SortBuilder):
        self._payload["params"]["order"] = order_clause_builder.sorts

    def add_page(self, start_index: int = 0, max_items: int = 100):
        if start_index < 0 or max_items < 0:
            raise ValueError(
                "Start index and max items must be greater than or equal to 0."
            )
        self._payload["params"]["page"] = {
            "startIndex": start_index,
            "maxItems": max_items,
        }

    def add_stat_fields(self, stat_fields: List[str]):
        self._payload["params"]["statFields"] = stat_fields
