// Copyright 2024 Autoware Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "lanelet2_map_validator/validators/intersection/intersection_area_validity.hpp"
#include "map_validation_tester.hpp"

#include <gtest/gtest.h>
#include <lanelet2_core/LaneletMap.h>

#include <map>
#include <string>

class TestIntersectionAreaValidity : public MapValidationTester
{
protected:
  const std::string test_target_ =
    std::string(lanelet::autoware::validation::IntersectionAreaValidityValidator::name());
};

TEST_F(TestIntersectionAreaValidity, ValidatorAvailability)  // NOLINT for gtest
{
  std::string expected_validator_name =
    lanelet::autoware::validation::IntersectionAreaValidityValidator::name();

  lanelet::validation::Strings validators =
    lanelet::validation::availabeChecks(expected_validator_name);  // cspell:disable-line

  const uint32_t expected_validator_num = 1;
  EXPECT_EQ(expected_validator_num, validators.size());
  EXPECT_EQ(expected_validator_name, validators[0]);
}

TEST_F(TestIntersectionAreaValidity, CheckWrongOrientation)  // NOLINT for gtest
{
  load_target_map("intersection/intersection_area_with_wrong_orientation.osm");

  lanelet::autoware::validation::IntersectionAreaValidityValidator checker;
  const auto & issues = checker(*map_);

  EXPECT_EQ(issues.size(), 0);
}

TEST_F(TestIntersectionAreaValidity, CheckSelfIntersection)  // NOLINT for gtest
{
  load_target_map("intersection/intersection_area_with_self_intersection.osm");

  lanelet::autoware::validation::IntersectionAreaValidityValidator checker;
  const auto & issues = checker(*map_);

  std::map<std::string, std::string> reason_map;
  reason_map["boost_geometry_message"] =
    "Geometry has invalid self-intersections. A "
    "self-intersection point was found at (3757.52, 73751.8); method: i; operations: u/i; segment "
    "IDs {source, multi, ring, segment}: {0, -1, -1, 21}/{0, -1, -1, 23}";
  const auto expected_issue =
    construct_issue_from_code(issue_code(test_target_, 1), 10803, reason_map);
}

TEST_F(TestIntersectionAreaValidity, ValidIntersectionArea)  // NOLINT for gtest
{
  load_target_map("intersection/basic_intersection_area.osm");

  lanelet::autoware::validation::IntersectionAreaValidityValidator checker;
  const auto & issues = checker(*map_);

  EXPECT_EQ(issues.size(), 0);
}

TEST_F(TestIntersectionAreaValidity, SampleMap)  // NOLINT for gtest
{
  load_target_map("sample_map.osm");

  lanelet::autoware::validation::IntersectionAreaValidityValidator checker;
  const auto & issues = checker(*map_);

  EXPECT_EQ(issues.size(), 0);
}
