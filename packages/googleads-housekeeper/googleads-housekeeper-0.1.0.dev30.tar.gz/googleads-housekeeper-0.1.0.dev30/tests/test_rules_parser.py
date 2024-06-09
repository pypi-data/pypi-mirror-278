from __future__ import annotations

import pytest

from googleads_housekeeper.domain.core import rules_parser


class TestRulesParser:

    @pytest.fixture
    def raw_rules(self):
        return [
            'GOOGLE_ADS_INFO:clicks > 0,cost > 100',
            'GOOGLE_ADS_INFO:placement_type = MOBILE_APPLICATION,ctr = 0',
            'GOOGLE_ADS_INFO:conversions = 0,WEBSITE_INFO:title regexp game'
        ]

    @pytest.fixture
    def implicit_raw_rules(self):
        return [
            'clicks > 0,cost > 100',
            'placement_type = MOBILE_APPLICATION,ctr = 0',
            'conversions = 0,WEBSITE_INFO:title regexp game'
        ]

    @pytest.fixture
    def rules_expression(self):
        return (
            'GOOGLE_ADS_INFO:clicks > 0 AND GOOGLE_ADS_INFO:cost > 100'
            ' OR GOOGLE_ADS_INFO:placement_type = MOBILE_APPLICATION AND '
            'GOOGLE_ADS_INFO:ctr = 0 OR GOOGLE_ADS_INFO:conversions = 0 AND '
            'WEBSITE_INFO:title regexp game')

    @pytest.fixture
    def expected_rules(self):
        return [
            [
                rules_parser.Rule('GOOGLE_ADS_INFO', 'clicks > 0'),
                rules_parser.Rule('GOOGLE_ADS_INFO', 'cost > 100')
            ],
            [
                rules_parser.Rule('GOOGLE_ADS_INFO',
                                  'placement_type = MOBILE_APPLICATION'),
                rules_parser.Rule('GOOGLE_ADS_INFO', 'ctr = 0')
            ],
            [
                rules_parser.Rule('GOOGLE_ADS_INFO', 'conversions = 0'),
                rules_parser.Rule('WEBSITE_INFO', 'title regexp game')
            ],
        ]

    def test_parser_generate_rules_from_raw_rules_with_excplicit_types(
            self, raw_rules, expected_rules):
        rules = rules_parser.generate_rules(raw_rules)
        assert rules == expected_rules

    def test_parser_generate_rules_from_raw_rules_with_implicit_types(
            self, implicit_raw_rules, expected_rules):
        rules = rules_parser.generate_rules(implicit_raw_rules)
        assert rules == expected_rules

    def test_parser_generate_rules_from_expression(self, rules_expression,
                                                   expected_rules):
        rules = rules_parser.generate_rules(rules_expression)
        assert rules == expected_rules
