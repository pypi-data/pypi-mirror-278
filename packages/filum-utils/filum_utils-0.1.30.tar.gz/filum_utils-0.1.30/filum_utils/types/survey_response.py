from typing import TypedDict, Union, Dict, Any


class CreateSurveyResponse(TypedDict, total=False):
    identifier: str
    anonymous_id: str
    send_timestamp: str
    transaction_id: Union[str, None]
    user_phone: Union[str, None]
    user_email: Union[str, None]
    user_name: Union[str, None]
    user_id: Union[str, None]
    source: Union[str, None]
    triggered_source: Union[str, None]
    sending_failed_reason: Union[str, None]
    distribution_id: Union[str, None]
    trigger_data: Union[Dict[str, Any], None]
    send_cost: Union[float, None]
