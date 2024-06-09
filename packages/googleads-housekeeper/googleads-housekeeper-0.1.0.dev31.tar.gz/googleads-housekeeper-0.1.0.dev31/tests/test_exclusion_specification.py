from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

import pytest
from gaarf.report import GaarfReport

from googleads_housekeeper.domain.core import exclusion_specification
from googleads_housekeeper.domain.core import rules_parser
from googleads_housekeeper.domain.external_parsers import website_parser
from googleads_housekeeper.domain.external_parsers import youtube_data_parser


@dataclass
class FakePlacement:
    campaign_id: int = 1
    campaign_name: str = '01_test_campaign'
    placement: str = 'example.com'
    clicks: int = 10
    ctr: float = 0.4
    placement_type: str = 'WEBSITE'
    extra_info: dict = field(
        default_factory=lambda: {
            'website_info':
                website_parser.WebsiteInfo(
                    placement='example.com', title='example')
        })


@pytest.fixture
def placement():
    return FakePlacement()


class TestAdsExclusionSpecificationEntry:

    @pytest.mark.parametrize('expression', ['single_name', 'single_name >'])
    def test_invalid_expression_length_raises_value_error(self, expression):
        with pytest.raises(ValueError, match='Incorrect expression *'):
            exclusion_specification.AdsExclusionSpecificationEntry(expression)

    def test_invalid_expression_operator_raises_value_error(self):
        with pytest.raises(ValueError, match='Incorrect operator *'):
            exclusion_specification.AdsExclusionSpecificationEntry('clicks ? 0')

    @pytest.fixture(params=[
        'clicks > 1', 'clicks = 10', 'ctr < 0.6', 'placement_type = WEBSITE',
        'placement_type contains WEB', 'campaign_name regexp ^01.+'
    ])
    def ads_exclusion_specification_success(self, request):
        return exclusion_specification.AdsExclusionSpecificationEntry(
            request.param)

    @pytest.fixture(params=[
        'clicks > 100', 'clicks != 10', 'ctr > 0.6',
        'placement_type = MOBILE_APPLICATION', 'placement_type contains MOBILE',
        'campaign_name regexp ^02.+'
    ])
    def ads_exclusion_specification_fail(self, request):
        return exclusion_specification.AdsExclusionSpecificationEntry(
            request.param)

    def test_placement_safisties_ads_exclusion_specification(
            self, placement, ads_exclusion_specification_success):
        result = ads_exclusion_specification_success.is_satisfied_by(placement)
        assert result

    def test_placement_does_not_satisfy_ads_exclusion_specification(
            self, placement, ads_exclusion_specification_fail):
        result = ads_exclusion_specification_fail.is_satisfied_by(placement)
        assert not result[0]

    def test_is_satisfied_by_raises_value_error_when_non_existing_entity_name_is_provided(
            self, placement):
        specification = exclusion_specification.AdsExclusionSpecificationEntry(
            'fake_name > 0')
        with pytest.raises(ValueError):
            specification.is_satisfied_by(placement)


class TestContentExclusionSpecifition:

    @pytest.fixture(params=[
        'title contains games', 'description contains fun',
        'keywords regexp free'
    ])
    def content_exclusion_specification_success(self, request):
        return exclusion_specification.ContentExclusionSpecificationEntry(
            expression=request.param)

    @pytest.fixture(params=[
        'title contains football', 'description contains gloomy',
        'keywords regexp paid'
    ])
    def content_exclusion_specification_failure(self, request):
        return exclusion_specification.ContentExclusionSpecificationEntry(
            expression=request.param)

    def test_website_satisfies_content_exclusion_specification(
            self, placement, content_exclusion_specification_success):
        result = content_exclusion_specification_success.is_satisfied_by(
            placement)
        assert result

    def test_website_does_not_satisfy_content_exclusion_specification(
            self, placement, content_exclusion_specification_failure):
        result = content_exclusion_specification_failure.is_satisfied_by(
            placement)
        assert not result[0]


class TestYouTubeChannelExclusionSpecifition:

    @pytest.fixture
    def youtube_channel_placement(self):
        return FakePlacement(
            placement='1kdjf0skdjfw0dsdf', placement_type='YOUTUBE_CHANNEL')

    @pytest.fixture(params=[
        'title regexp garden*', 'description contains game', 'country = US',
        'viewCount > 10', 'subscriberCount > 1', 'videoCount > 1',
        'topicCategories contains game'
    ])
    def youtube_channel_exclusion_specification_success(self, request):
        return exclusion_specification.YouTubeChannelExclusionSpecificationEntry(
            expression=request.param)

    @pytest.fixture(params=[
        'title regexp football*', 'description contains tv', 'country = GB',
        'viewCount > 100000', 'subscriberCount > 100000', 'videoCount > 100000',
        'topicCategories contains football'
    ])
    def youtube_channel_exclusion_specification_failure(self, request):
        return exclusion_specification.YouTubeChannelExclusionSpecificationEntry(
            expression=request.param)

    def test_youtube_channel_satisfies_youtube_channel_exclusion_specification(
            self, youtube_channel_placement,
            youtube_channel_exclusion_specification_success):
        result = youtube_channel_exclusion_specification_success.is_satisfied_by(
            youtube_channel_placement)
        assert result

    def test_youtube_channel_does_not_satisfy_youtube_channel_exclusion_specification(
            self, youtube_channel_placement,
            youtube_channel_exclusion_specification_failure):
        result = youtube_channel_exclusion_specification_failure.is_satisfied_by(
            youtube_channel_placement)
        assert not result[0]


class TestYouTubeVideoExclusionSpecifition:

    @pytest.fixture
    def youtube_video_placement(self):
        return FakePlacement(placement='jojoh', placement_type='YOUTUBE_VIDEO')

    @pytest.fixture(params=[
        'title regexp garden*', 'description contains game',
        'defaultLanguage = en', 'defaultAudioLanguage = en', 'commentCount > 1',
        'favouriteCount > 1', 'likeCount > 1', 'viewCount > 10',
        'madeForKids = True', 'topicCategories contains game',
        'tags contains garden'
    ])
    def youtube_video_exclusion_specification_success(self, request):
        return exclusion_specification.YouTubeVideoExclusionSpecificationEntry(
            expression=request.param)

    @pytest.fixture(params=[
        'title regexp football*', 'description contains football',
        'defaultLanguage = es', 'defaultAudioLanguage = es',
        'commentCount > 10000', 'favouriteCount > 10000', 'likeCount > 10000',
        'viewCount > 1000000', 'madeForKids = False',
        'topicCategories contains football', 'tags contains football'
    ])
    def youtube_video_exclusion_specification_failure(self, request):
        return exclusion_specification.YouTubeVideoExclusionSpecificationEntry(
            expression=request.param)

    def test_youtube_video_satisfies_youtube_video_exclusion_specification(
            self, youtube_video_placement,
            youtube_video_exclusion_specification_success):
        result = youtube_video_exclusion_specification_success.is_satisfied_by(
            youtube_video_placement)
        assert result

    def test_youtube_video_does_not_satisfy_youtube_video_exclusion_specification(
            self, youtube_video_placement,
            youtube_video_exclusion_specification_failure):
        result = youtube_video_exclusion_specification_failure.is_satisfied_by(
            youtube_video_placement)
        assert not result[0]


class TestExclusionSpecificationEntry:

    @pytest.fixture
    def rules(self):
        return rules_parser.generate_rules(raw_rules=[
            ('GOOGLE_ADS_INFO:clicks > 1, '
             'GOOGLE_ADS_INFO:conversion_name regexp test_conversion'),
            'YOUTUBE_VIDEO_INFO:likeCount > 1',
        ])

    @pytest.fixture
    def ads_specification_entry(self):
        return exclusion_specification.AdsExclusionSpecificationEntry(
            expression='clicks > 1')

    @pytest.fixture
    def ads_specification_entry_conversion_split(self):
        return exclusion_specification.AdsExclusionSpecificationEntry(
            expression='conversion_name regexp test_conversion')

    @pytest.fixture
    def non_ads_specification_entry(self):
        return exclusion_specification.YouTubeVideoExclusionSpecificationEntry(
            expression='likeCount > 1')

    @pytest.fixture
    def sample_exclusion_specification(
            self, ads_specification_entry, non_ads_specification_entry,
            ads_specification_entry_conversion_split):
        return exclusion_specification.ExclusionSpecification(specifications=[[
            ads_specification_entry, ads_specification_entry_conversion_split
        ], [non_ads_specification_entry]])

    @pytest.fixture
    def placements(self):
        return GaarfReport(
            results=[
                [
                    'youtube_video', 'YOUTUBE_VIDEO', 10, 'test_conversion', 0,
                    {
                        'youtube_video_info':
                            youtube_data_parser.VideoInfo(
                                placement='youtube_video', likeCount=10)
                    }
                ],
                ['website', 'WEBSITE', 0, 'real_conversion', 0, {}],
            ],
            column_names=[
                'placement', 'placement_type', 'clicks', 'conversion_name',
                'conversions_', 'extra_info'
            ])

    def test_true_exclusion_specification(self, sample_exclusion_specification):
        assert bool(sample_exclusion_specification) is True

    def test_placement_satisfies_ads_exclusion_specifications_list(
            self, ads_specification_entry):
        """
        If placement satisfies all exclusion specifications in the list,
        it satisfies the whole list.
        """
        specification = exclusion_specification.ExclusionSpecification(
            specifications=[[ads_specification_entry]])
        sample_placement = FakePlacement(clicks=10)
        result = specification.satisfies(sample_placement)
        assert result == ([[
            'GOOGLE_ADS_INFO:clicks > 1',
        ]], {})

    def test_placement_does_not_satisfy_ads_exclusion_specifications_list(
            self, ads_specification_entry):
        """
        If placement does not satisfy at least one exclusion specifications in
        the list, it does not satisfy the whole list.
        """
        specification = exclusion_specification.ExclusionSpecification(
            specifications=[[ads_specification_entry]])
        sample_placement = FakePlacement(clicks=0)
        result = specification.satisfies(sample_placement)
        assert result == ([], {})

    def test_get_correct_ads_entries(self, sample_exclusion_specification,
                                     ads_specification_entry,
                                     ads_specification_entry_conversion_split):
        expected_exclusion_specifications = (
            exclusion_specification.ExclusionSpecification(specifications=[[
                ads_specification_entry,
                ads_specification_entry_conversion_split
            ]]))
        ads_specs = sample_exclusion_specification.ads_specs_entries
        assert ads_specs == expected_exclusion_specifications

    def test_get_correct_non_ads_entries(self, sample_exclusion_specification,
                                         non_ads_specification_entry):
        expected_exclusion_specifications = (
            exclusion_specification.ExclusionSpecification(
                specifications=[[non_ads_specification_entry]]))
        non_ads_specs = sample_exclusion_specification.non_ads_specs_entries
        assert non_ads_specs == expected_exclusion_specifications

    def test_parser_generate_rules_explicit_types(
            self, rules, sample_exclusion_specification):
        specification = exclusion_specification.ExclusionSpecification.from_rules(
            rules)
        assert specification == sample_exclusion_specification

    def test_generate_runtime_options(self, sample_exclusion_specification,
                                      ads_specification_entry_conversion_split):
        runtime_options = sample_exclusion_specification.define_runtime_options(
        )
        assert runtime_options == exclusion_specification.RuntimeOptions(
            is_conversion_query=True,
            conversion_name='test_conversion',
            conversion_rules=[ads_specification_entry_conversion_split])

    def test_apply_specifications(self, sample_exclusion_specification,
                                  placements):
        expected_result = GaarfReport(
            results=[
                [
                    'youtube_video', 'YOUTUBE_VIDEO', 10, 'test_conversion', 0,
                    {
                        'youtube_video_info':
                            youtube_data_parser.VideoInfo(
                                placement='youtube_video', likeCount=10)
                    }
                ],
            ],
            column_names=[
                'placement', 'placement_type', 'clicks', 'conversion_name',
                'conversions_', 'extra_info'
            ])
        result = sample_exclusion_specification.apply_specifications(placements)
        assert result['placement'] == expected_result['placement']
