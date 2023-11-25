
from dataclasses import dataclass


@dataclass
class UserStatusDTO:
    username: str | None = None
    type : None | str = None
    hashtag : None | str | list[str] = None
    media : None | str = None
    caption : None | str = None
    like_count : None | str | int = None
    comment_count : None | str | int = None
    view_count : None | str | int = None
    retwitt_count : None | str | int = None
    links : None | str | list[str] = None


@dataclass
class UserInformation:
    username: str | None = None
    profile_pic_url: str | None = None
    media_count: str | None = None
    bio: str | None = None
    follower_count: str | None | int = None
    following_count: str | None | int = None
    status: list[UserStatusDTO] | None = None


@dataclass
class TwitteDTO:
    text : None | str = None
    imperation : None | str = None
    retwitte : None | str | int = None
    comments : None | str | int = None
    likes : None | str | int = None


@dataclass
class TwitterUserDTO:
    name: str | None = None
    bio : None | str = None
    following : None | str = None
    follower : None | str = None
    username : None | str = None


@dataclass
class TwitterMetaDTO:
    twitts: str | int | None = None
    retwitts: str | int | None = None
    last_twitte : any = None


@dataclass
class TwitteInformationDTO:
    twitts: list[TwitteDTO] | None = None
    meta: TwitterMetaDTO | None = None


@dataclass
class TwitterDataDTO:
    user: TwitterUserDTO | None = None
    timeline: TwitteInformationDTO | None = None