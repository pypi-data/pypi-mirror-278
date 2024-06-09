from __future__ import annotations

from datetime import datetime

import pytest

from googleads_housekeeper import bootstrap
from googleads_housekeeper.adapters import notifications
from googleads_housekeeper.adapters import publisher
from googleads_housekeeper.domain import commands
from googleads_housekeeper.domain import external_parsers
from googleads_housekeeper.services import unit_of_work


class FakeGoogleAdsApiClient:
    ...


class FakeNotifications(notifications.BaseNotifications):

    def __init__(self):
        self.sent = defaultdict(list)  # type: Dict[str, List[str]]

    def publish(self, topic, event):
        self.sent[destination].append(message)


class FakePublisher(publisher.BasePublisher):

    def __init__(self):
        self.events = []  # type: Dict[str, List[str]]

    def publish(self, topic, event):
        self.events.append(event)


@pytest.fixture(scope='session')
def in_memory_sqlite_db():
    return 'sqlite:///:memory:'


@pytest.fixture(scope='session')
def fake_publisher():
    return FakePublisher()


@pytest.fixture(scope='session')
def bus(fake_publisher, in_memory_sqlite_db):
    bus = bootstrap.bootstrap(
        start_orm=True,
        ads_api_client=FakeGoogleAdsApiClient(),
        uow=unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_db),
        publish_service=fake_publisher)
    new_website_info = external_parsers.website_parser.WebsiteInfo(
        placement='example.com',
        title='fun games',
        description='millions of fun games',
        keywords='browser games, free games',
        is_processed=True,
        last_processed_time=datetime.now())
    new_channel_info = external_parsers.youtube_data_parser.ChannelInfo(
        placement='1kdjf0skdjfw0dsdf',
        title='Gardening and Games',
        description='Everything about Games and Gardens',
        country='US',
        viewCount=1000,
        subscriberCount=100,
        videoCount=10,
        topicCategories='Gardening,Games',
        last_processed_time=datetime.now(),
        is_processed=True)
    new_video_info = external_parsers.youtube_data_parser.VideoInfo(
        placement='jojoh',
        title='Gardening and Games Vol. 2',
        description='The second volumes of the Gardening and Games series',
        defaultLanguage='en',
        defaultAudioLanguage='en',
        commentCount=10,
        favouriteCount=10,
        likeCount=10,
        viewCount=1000,
        madeForKids=True,
        topicCategories='Gardening,Games',
        tags='#multiplayer,#mro,#garden',
        last_processed_time=datetime.now(),
        is_processed=True)

    bus.handle(commands.SaveChannelInfo(new_channel_info))
    bus.handle(commands.SaveVideoInfo(new_video_info))
    bus.handle(commands.SaveWebsiteInfo(new_website_info))
    return bus
