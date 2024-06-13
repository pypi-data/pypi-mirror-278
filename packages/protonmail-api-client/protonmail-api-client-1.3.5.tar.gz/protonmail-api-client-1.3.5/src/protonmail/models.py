"""Dataclasses."""
from dataclasses import dataclass, field, asdict


@dataclass
class UserMail:
    """User."""
    name: str = ''
    address: str = ''
    extra: dict = field(default_factory=dict)

    def __str__(self):
        return f"<UserMail [{self.address}]>"

    def to_dict(self) -> dict[str, any]:
        """
        Object to dict

        :returns: :py:obj:`dict`
        """
        return asdict(self)


@dataclass
class Attachment:
    """Attachment."""
    id: str = ''
    name: str = ''
    size: int = 0
    type: str = ''
    content: bytes = b''
    is_decrypted: bool = False
    is_inserted: bool = False
    key_packets: str = ''
    cid: str = ''
    extra: dict = field(default_factory=dict)

    def __str__(self):
        ellipsis_str = '...' if len(self.name) > 20 else ','
        cropped_name = self.name[:20]
        return f"<Attachment [{cropped_name}{ellipsis_str} {self.size} bytes]>"

    def to_dict(self) -> dict[str, any]:
        """
        Object to dict

        :returns: :py:obj:`dict`
        """
        return asdict(self)


@dataclass
class Message:
    """Message."""
    id: str = ''
    conversation_id: str = ''
    subject: str = ''
    unread: bool = False
    sender: UserMail = field(default_factory=UserMail)
    recipients: list[UserMail] = field(default_factory=list)
    time: int = 0
    size: int = 0
    body: str = ''
    type: str = ''
    labels: list[str] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    def __str__(self):
        ellipsis_str = '...' if len(self.subject) > 20 else ','
        cropped_subject = self.subject[:20]
        return f"<Message [{cropped_subject}{ellipsis_str} id: {self.id[:10]}...]>"

    def to_dict(self) -> dict[str, any]:
        """
        Object to dict

        :returns: :py:obj:`dict`
        """
        return asdict(self)


@dataclass
class Conversation:
    """Conversation."""
    id: str = ''
    subject: str = ''
    senders: list[UserMail] = field(default_factory=list)
    recipients: list[UserMail] = field(default_factory=list)
    num_messages: int = 0
    num_unread: int = 0
    size: int = 0
    time: int = 0
    labels: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    def __str__(self):
        ellipsis_str = '...' if len(self.subject) > 20 else ','
        cropped_subject = self.subject[:20]
        return f"<Conversation [{cropped_subject}{ellipsis_str} id: {self.id[:10]}...]>"

    def to_dict(self) -> dict[str, any]:
        """
        Object to dict

        :returns: :py:obj:`dict`
        """
        return asdict(self)
