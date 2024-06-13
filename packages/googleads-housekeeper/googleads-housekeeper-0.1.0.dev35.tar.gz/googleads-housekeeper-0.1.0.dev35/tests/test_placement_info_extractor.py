from __future__ import annotations

import gaarf
import pytest

from googleads_housekeeper.domain.external_parsers import website_parser
from googleads_housekeeper.domain.external_parsers import youtube_data_parser
from googleads_housekeeper.domain.placement_handler import placement_info_extractor


class TestPlacementInfoExtractor:

    @pytest.fixture
    def extractor(self, bus):
        return placement_info_extractor.PlacementInfoExtractor(bus.uow)

    def test_extract_placement_info_returns_website_info(self, extractor):
        gaarf_row = gaarf.report.GaarfRow(
            data=['example.com', 'WEBSITE'],
            column_names=['placement', 'placement_type'])
        expected_result = {
            'website_info':
                website_parser.WebsiteInfo(
                    placement='example.com',
                    title='fun games',
                    description='millions of fun games',
                    keywords='browser games, free games',
                    is_processed=True)
        }
        result = extractor.extract_placement_info(gaarf_row)
        assert result == expected_result

    def test_extract_placement_info_returns_youtube_channel_info(
            self, extractor):
        gaarf_row = gaarf.report.GaarfRow(
            data=['1kdjf0skdjfw0dsdf', 'YOUTUBE_CHANNEL'],
            column_names=['placement', 'placement_type'])
        expected_result = {
            'youtube_channel_info':
                youtube_data_parser.ChannelInfo(
                    placement='1kdjf0skdjfw0dsdf',
                    title='Gardening and Games',
                    description='Everything about Games and Gardens',
                    country='US',
                    viewCount=1000,
                    subscriberCount=100,
                    videoCount=10,
                    topicCategories='Gardening,Games',
                    is_processed=True)
        }
        result = extractor.extract_placement_info(gaarf_row)
        assert result == expected_result

    def test_extract_placement_info_returns_youtube_video_info(self, extractor):
        gaarf_row = gaarf.report.GaarfRow(
            data=['jojoh', 'YOUTUBE_VIDEO'],
            column_names=['placement', 'placement_type'])
        expected_result = {
            'youtube_video_info':
                youtube_data_parser.VideoInfo(
                    placement='jojoh',
                    title='Gardening and Games Vol. 2',
                    description=(
                        'The second volumes of the Gardening and Games series'),
                    defaultLanguage='en',
                    defaultAudioLanguage='en',
                    commentCount=10,
                    favouriteCount=10,
                    likeCount=10,
                    viewCount=1000,
                    madeForKids=True,
                    topicCategories='Gardening,Games',
                    tags='#multiplayer,#mro,#garden',
                    is_processed=True)
        }
        result = extractor.extract_placement_info(gaarf_row)
        assert result == expected_result

    def test_extract_placement_info_returns_emtpy_info(self, extractor):
        gaarf_row = gaarf.report.GaarfRow(
            data=['test-app', 'MOBILE_APPLICATION'],
            column_names=['placement', 'placement_type'])
        expected_result = {}
        result = extractor.extract_placement_info(gaarf_row)
        assert result == expected_result
