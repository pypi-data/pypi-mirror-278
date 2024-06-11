from dataclasses import dataclass
from typing import Optional

from superblocks_agent._constant import DEFAULT_AGENT_ENDPOINT
from superblocks_agent._util.doc import modify_pdoc


@dataclass(kw_only=True, eq=False)
class Config:
    """
    Client configuration.
    Any configuration set here will be overridden the configuration set in the client.

    Args:
        token: (str): The agent auth token.
        endpoint: (str): The endpoint of the execution engine. Defaults to `'agent.superblocks.com:8443'`
        authority (Optional[str]): The authority to use. Defaults to `None`.
        insecure (bool): Whether to use an insecure channel or not. Defaults to `False`.
    """

    token: str
    endpoint: str = DEFAULT_AGENT_ENDPOINT
    authority: Optional[str] = None
    insecure: bool = False


__pdoc__ = modify_pdoc(dataclass=Config)
