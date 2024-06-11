from requests import Session

import dixa.api.v1 as v1


class DixaAPIv1Helper:
    def __init__(
        self,
        session: Session,
        debug: bool = False,
    ):
        kwargs = {"session": session, "debug": debug}

        self.Agent = v1.AgentResource(**kwargs)
        self.Analytics = v1.AnalyticsResource(**kwargs)
        self.ContactEndpoint = v1.ContactEndpointResource(**kwargs)
        self.Conversation = v1.ConversationResource(**kwargs)
        self.EndUser = v1.EndUserResource(**kwargs)
        self.Queue = v1.QueueResource(**kwargs)
        self.Tag = v1.TagResource(**kwargs)
        self.Team = v1.TeamResource(**kwargs)
        self.Webhook = v1.WebhookResource(**kwargs)


class DixaAPI(object):
    def __init__(self, access_token: str, debug=False):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authroization": access_token,
        }
        self.session = Session()
        self.session.headers.update(self.headers)

        self.debug = debug

        kwargs = {
            "session": self.session,
            "debug": debug,
        }

        self.v1 = DixaAPIv1Helper(**kwargs)


__all__ = ["DixaAPI"]
