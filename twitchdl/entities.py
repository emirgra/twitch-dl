from dataclasses import dataclass
from typing import Any, Generic, List, Literal, Mapping, Optional, TypeVar, TypedDict


T = TypeVar("T")

@dataclass
class Page(Generic[T]):
    page_no: int
    has_next: bool
    items: List[T]

    @property
    def size(self):
        return len(self.items)


@dataclass
class DownloadOptions:
    auth_token: Optional[str]
    chapter: Optional[int]
    concat: bool
    dry_run: bool
    end: Optional[int]
    format: str
    keep: bool
    no_join: bool
    overwrite: bool
    skip_existing: bool
    output: str
    quality: Optional[str]
    rate_limit: Optional[int]
    start: Optional[int]
    max_workers: int
    cache_dir: str


ClipsPeriod = Literal["last_day", "last_week", "last_month", "all_time"]
VideosSort = Literal["views", "time"]
VideosType = Literal["archive", "highlight", "upload"]


class AccessToken(TypedDict):
    signature: str
    value: str


class User(TypedDict):
    id: str
    login: str
    displayName: str


class Game(TypedDict):
    id: str
    name: str


class VideoQuality(TypedDict):
    frameRate: str
    quality: str
    sourceURL: str


class ClipAccessToken(TypedDict):
    id: str
    playbackAccessToken: AccessToken
    videoQualities: List[VideoQuality]


class Clip(TypedDict):
    id: str
    slug: str
    title: str
    createdAt: str
    viewCount: int
    durationSeconds: int
    url: str
    videoQualities: Optional[List[VideoQuality]]
    game: Game
    broadcaster: User


class Video(TypedDict):
    id: str
    title: str
    description: str
    createdAt: str
    # null in rare cases
    publishedAt: Optional[str]
    recordedAt: str
    updatedAt: str
    broadcastType: str
    lengthSeconds: int
    status: str
    viewCount: int
    seekPreviewsURL: str
    game: Optional["Game"]
    owner: User
    creator: User


class Chapter(TypedDict):
    id: str
    durationMilliseconds: int
    positionMilliseconds: int
    type: str
    description: str
    subDescription: str
    thumbnailURL: str
    game: Game


# Type for annotating decoded JSON
# TODO: make data classes for common structs
Data = Mapping[str, Any]


class Commenter(TypedDict):
    id: str
    login: str
    displayName: str


Emote = TypedDict(
    "Emote",
    {
        "id": str,
        "emoteID": str,
        "from": int,
    },
)


class Message_Fragment(TypedDict):
    emote: Optional[Emote]
    text: str


class Message_Badge(TypedDict):
    id: str
    setID: str
    version: str


class Message(TypedDict):
    fragments: List[Message_Fragment]
    userBadges: List[Message_Badge]
    userColor: str


class Comment(TypedDict):
    id: str
    commenter: Optional[Commenter]
    contentOffsetSeconds: int
    createdAt: str
    message: Message


class Badge(TypedDict):
    id: str
    setID: str
    version: str
    title: str
    image1x: str
    image2x: str
    image4x: str
    clickAction: str
    clickURL: str


class VideoComments_Owner(TypedDict):
    id: str
    login: str
    broadcastBadges: List[Badge]


class VideoComments_Video(TypedDict):
    id: str
    broadcastType: str
    lengthSeconds: int
    owner: VideoComments_Owner


class VideoComments(TypedDict):
    video: VideoComments_Video
    badges: List[Badge]
