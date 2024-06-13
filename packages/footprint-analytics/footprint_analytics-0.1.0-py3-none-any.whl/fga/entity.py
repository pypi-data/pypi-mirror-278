from fga.event import BaseEvent
import pydash


class UserEvent:

    @staticmethod
    def __mapping__(event: BaseEvent):
        user_event = {"event_id": event.event_id, "user_id": event.user_id, "project_id": None, "timestamp": event.time,
                      "device_id": event.device_id or pydash.get(event, "event_properties.device_id"),
                      "region": event.region or pydash.get(event, "event_properties.region"),
                      "event_device": event.platform or pydash.get(event, "event_properties.platform"), "event_source": "web2",
                      "event_type": event.event_type, "extra_data": event}
        return user_event


class User:

    @staticmethod
    def __mapping__(event: BaseEvent):
        user = {
            "user_id": event.user_id,
            "project_id": None,
            "sign_up_device": pydash.get(event, "user_properties.sign_up_device"),
            "account_type": None,
            "idfa": event.idfa or event.idfv or pydash.get(event, "user_properties.idfa"),
            "udid": event.android_id or pydash.get(event, "user_properties.android_id"),
            "country": event.country or pydash.get(event, "user_properties.country"),
            "email": pydash.get(event, "user_properties.email"),
            "ip": event.ip or pydash.get(event, "user_properties.ip"),
            "twitter": pydash.get(event, "user_properties.twitter"),
            "discord": pydash.get(event, "user_properties.discord"),
            "sign_up_at": pydash.get(event, "user_properties.sign_up_at") or event.time,
            "extra_data": event
        }
        return user
