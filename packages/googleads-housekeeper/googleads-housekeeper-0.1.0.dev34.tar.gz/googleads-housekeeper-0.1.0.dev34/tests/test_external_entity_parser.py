# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for external entity parser."""
from __future__ import annotations

from gaarf.report import GaarfReport

from googleads_housekeeper.domain.core import exclusion_specification
from googleads_housekeeper.domain.external_parsers import (
    external_entity_parser)
from googleads_housekeeper.domain.external_parsers import website_parser


def test_external_entity_parser(mocker, bus):
    external_parser = external_entity_parser.ExternalEntitiesParser(bus.uow)
    specification_entry = (
        exclusion_specification.ContentExclusionSpecificationEntry(
            'placement regexp example'))
    specification = exclusion_specification.ExclusionSpecification(
        specifications=[[specification_entry]])
    report = GaarfReport(
        results=[['parsed-example.com', 'WEBSITE']],
        column_names=['placement', 'placement_type'])
    mocker.patch(
        'googleads_housekeeper.domain.external_parsers.website_parser.'
        'WebSiteParser.parse',
        return_value=[
            website_parser.WebsiteInfo(
                placement='parsed-example.com',
                title='example title',
                description='example description',
                keywords='example keywords',
                is_processed=True)
        ])

    external_parser.parse_specification_chain(
        entities=report, specification=specification.parsable_spec_entries)
    with bus.uow as uow:
        assert uow.website_info.get_by_conditions(
            {'placement': 'parsed-example.com'})
