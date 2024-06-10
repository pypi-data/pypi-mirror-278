from typing import Dict, Any, Optional, Callable, List

from filum_utils.clients.notification import RoutePath, PublisherType
from filum_utils.config import config
from filum_utils.enums import ParentType, BaseStatus, ObjectType
from filum_utils.errors import BaseError
from filum_utils.services.file import FileService
from filum_utils.services.subscription import SubscriptionService
from filum_utils.types.action import Action
from filum_utils.types.campaign import Campaign
from filum_utils.types.common import CallableResponse, TriggerFunctionResponse
from filum_utils.types.organization import Organization
from filum_utils.types.subscription import Subscription, SubscriptionData

Event = Optional[Dict[str, Any]]
User = Optional[Dict[str, Any]]


class CampaignSubscriptionService(SubscriptionService):
    def __init__(
        self,
        campaign: Campaign,
        subscription: Subscription,
        action: Action,
        organization: Organization
    ):
        super().__init__(subscription, organization)

        self.campaign = campaign
        self.action = action

    @property
    def parent(self):
        return self.campaign

    @property
    def member_account_id(self):
        account = self.campaign["account"] or {}
        return account.get("id")

    @property
    def run_type(self) -> Optional[str]:
        return self.campaign.get("run_type")

    @property
    def _parent_type(self) -> str:
        return ParentType.CAMPAIGN

    @property
    def _object_type(self) -> str:
        return ObjectType.ACTION

    @property
    def _object_id(self) -> int:
        return self.action["id"]

    @property
    def _notification_route(self) -> Dict[str, Any]:
        return {
            "path": RoutePath.CAMPAIGNS_DETAIL,
            "params": {
                "campaignId": self.campaign["id"]
            }
        }

    @property
    def _notification_publisher_type(self) -> str:
        return PublisherType.VoC

    def handle_real_time_trigger(
        self,
        process_real_time_fn: Callable[
            [Action, Campaign, Organization, Event, SubscriptionData, Any],
            CallableResponse
        ],
        event: [Dict[str, Any]],
        **kwargs,
    ) -> TriggerFunctionResponse:
        result = self._handle_trigger(
            process_real_time_fn,
            event,
            **kwargs
        )

        return {
            "is_finished": True,
            "success_count": result.get("success_count"),
            "error_message": None,
        }

    def handle_segment_manual_trigger(
        self,
        process_segment_manual_fn: Callable[
            [Action, Campaign, Organization, List[User], SubscriptionData, Any],
            CallableResponse
        ],
        properties: List[str],
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        **kwargs,
    ) -> TriggerFunctionResponse:
        current_index = self.subscription_data.get("last_current_index") or 0
        if current_index and current_index != last_current_index:
            raise BaseError(
                message="Last current index not matched",
                data={
                    "Campaign ID": self.campaign["id"],
                    "Current Index": current_index,
                    "Last Current Index": last_current_index
                }
            )

        trigger_data = self.subscription_data.get("trigger_data")
        segment_id = trigger_data.get("segment_id")
        if not segment_id:
            raise BaseError(
                message="Missing segment id",
                data={
                    "Campaign ID": self.campaign["id"],
                }
            )

        users = self.filum_client.get_user_csv_reader(
            properties=properties,
            object_ids=[segment_id],
            object_type="segment",
            organization=self.organization,
            offset=last_current_index,
            limit=config.SEGMENT_RECORD_LIMIT
        )

        result = self._handle_trigger(
            process_fn=process_segment_manual_fn,
            data=users,
            **kwargs,
        )

        success_count = result.get("success_count") or 0
        total_success_count = last_success_count + success_count

        is_finished = True
        error_message = None

        total_users = len(users) if users else 0
        if total_users >= config.SEGMENT_RECORD_LIMIT:
            is_finished = False
            error_message = self._handle_publish_subscription(
                last_current_index=total_users + last_current_index,
                last_success_count=total_success_count,
            )
        else:
            error_message = self._handle_trigger_function_with_try_except(
                "Update Campaign Status",
                self._handle_trigger_completed,
                fn_params={
                    "channel_name": channel_name,
                    "success_count": total_success_count
                }
            )

        return {
            "is_finished": is_finished,
            "success_count": success_count,
            "error_message": error_message
        }

    def handle_file_manual_trigger(
        self,
        process_file_manual_fn: Callable,
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        **kwargs,
    ):
        current_index = self.subscription_data.get("last_current_index") or 0
        if current_index and current_index != last_current_index:
            raise BaseError(
                message="Last current index not matched",
                data={
                    "Campaign ID": self.campaign["id"],
                    "Current Index": current_index,
                    "Last Current Index": last_current_index
                }
            )

        trigger_data = self.subscription_data.get("trigger_data")
        file_name = trigger_data.get("file_name")
        if not file_name:
            raise BaseError(
                message="Missing file",
                data={
                    "Campaign ID": self.campaign["id"],
                }
            )

        file_content_bytes = self.filum_client.get_uploaded_file(file_name)
        users = FileService.get_rows(
            file_name,
            file_content_bytes,
            current_index=last_current_index,
            limit=config.FILE_RECORD_LIMIT,
        )

        result = self._handle_trigger(
            process_fn=process_file_manual_fn,
            data=users,
            **kwargs,
        )

        success_count = result.get("success_count") or 0
        total_success_count = last_success_count + success_count
        is_finished = True
        error_message = None

        total_users = len(users) if users else 0
        if total_users >= config.FILE_RECORD_LIMIT:
            is_finished = False
            error_message = self._handle_publish_subscription(
                last_current_index=total_users + last_current_index,
                last_success_count=total_success_count,
            )
        else:
            error_message = self._handle_trigger_function_with_try_except(
                "Update Campaign Status",
                self._handle_trigger_completed,
                fn_params={
                    "channel_name": channel_name,
                    "success_count": total_success_count
                }
            )

        return {
            "is_finished": is_finished,
            "success_count": success_count,
            "error_message": error_message,
        }

    def handle_object_manual_trigger(
        self,
        process_object_manual_fn: Callable,
        **kwargs,
    ):
        ...

    def update_status(self, updated_status: str):
        self.filum_client.update_campaign_subscription_status(
            campaign_id=self.campaign.get("id"),
            subscription_id=self.subscription.get("id"),
            updated_status=updated_status,
        )

    def _handle_trigger(
        self,
        process_fn: Callable,
        data: Any,
        **kwargs,
    ):
        params = {
            "action": self.action,
            "campaign": self.campaign,
            "data": data,
            "subscription_data": self.subscription_data,
            "organization": self.organization,
            **kwargs
        }

        return process_fn(**params)

    def _handle_trigger_completed(
        self,
        channel_name: Optional[str],
        success_count: int
    ):
        self.update_status(BaseStatus.COMPLETED)
        if channel_name:
            self._notify(
                publisher_type=f"{self._notification_publisher_type}",
                title=f"{self.parent.get('name')} has been distributed successfully to your recipients",
                subtitle=f"{success_count} survey(s) sent via {channel_name}",
            )

    def _handle_publish_subscription(
        self,
        last_current_index: int,
        last_success_count: int
    ):
        update_subscript_data_error_message = self._handle_trigger_function_with_try_except(
            "Update Subscription Data",
            self.update_subscription_data,
            fn_params={
                "updated_data": {"last_current_index": last_current_index}
            }
        ) or ""
        publish_subscription_error_message = self._handle_trigger_function_with_try_except(
            "Publish Subscription",
            self.subscription_client.publish,
            fn_params={
                "request_data": {
                    "last_current_index": last_current_index,
                    "last_success_count": last_success_count,
                }
            }
        ) or ""
        error_message = None
        if update_subscript_data_error_message or publish_subscription_error_message:
            error_message = (
                f"{update_subscript_data_error_message} {publish_subscription_error_message}"
            )

        return error_message

    @staticmethod
    def _handle_trigger_function_with_try_except(
        fn_name: str,
        fn: Callable,
        fn_params: Dict[str, Any] = None
    ) -> str:
        error_message = None
        try:
            fn_params = fn_params if fn_params else {}
            fn(**fn_params)
        except BaseError as e:
            error_message = e.message
        except Exception:
            error_message = "Implementation Error"

        if error_message:
            error_message = f"{fn_name}: {error_message}"

        return error_message
