# How to contribute to autoware_lanelet2_map_validator

Your contribution is welcome to achieve a broad view of validation for lanelet2 maps.
This document gives you the instructions on how to add a validator to `autoware_lanelet2_map_validator`.
Please take a look at the [Design Concept](#design-concept) and follow the [Contribution Guide](#contribution-guide).

## Design Concept

The main goal of `autoware_lanelet2_map_validator` is to validate whether the lanelet2 map matches the vector map requirements for Autoware.
`autoware_lanelet2_map_validator` achieves this by running a list of small validators.
In other words, each vector map requirement will be validated by one or more validators.
It is recommended to keep validators small and they don't have to be unique to a specific requirement so that we can broaden the expression of map requirements. (It doesn't mean that a validator should output only one kind of error!)

The list of small validators will be defined as a JSON file (see [`autoware_requirement_set.json`](https://github.com/tier4/autoware_lanelet2_map_validator/blob/main/autoware_lanelet2_map_validator/autoware_requirement_set.json) for an example), and the output will also be a JSON file that appends validation results to a copy of the input. See [How to use `autoware_lanelet2_map_validator`](../../README.md#how-to-use) for further information about how the input and output are processed.

![autoware_lanelet2_map_validator_input_and_output](../media/autoware_lanelet2_map_validator_io.svg)

Please note that the validators are categorized according to [the vector map requirements written in the Autoware Documentation](https://autowarefoundation.github.io/autoware-documentation/main/design/autoware-architecture/map/map-requirements/vector-map-requirements-overview/). If there are any suggestions for new categories please let the pull request (PR) reviewers know. The available categories as of now are

- Lane
- Stop line
- Intersection
- Traffic light
- Crosswalk
- Area
- Others

## Version Control

`autoware_lanelet2_map_validator` began version control on January, 2025 in order to clarify the linkage to versioned map requirements and specifications.
The version of `autoware_lanelet2_map_validator` starts from `1.0.0` having the major, minor, and patch version.
See the following sections for further explanations of each version.
Note that the version of `autoware_lanelet2_map_validator` is stated in the `package.xml` and it is separated to that of `autoware_requirement_set.json`.
Therefore, the version written in `autoware_requirement_set.json` is **NOT** linked to the version of `autoware_lanelet2_map_validator`.
The version of `autoware_requirement_set.json` refers to the version of [map requirements and specifications for Autoware](https://autowarefoundation.github.io/autoware-documentation/main/design/autoware-architecture/map/map-requirements/vector-map-requirements-overview/) (... which is not having its version controlled so yes leave it alone for now).

### Major version

The major version increases with the following changes.

- Destructive changes that backward compatibility cannot be maintained.
- The format of inputs and outputs drastically changes.
- The entire code structure drastically changes.

The major version is NOT intended to be updated frequently.

### Minor version

The minor version increases with the following changes.

- Addition of new validators.
- Modification of existing validators due to updates of map requirements or other reasons.
  - Even if the validation result changes, it will not be taken as the lost of backward compatibility if it only affects a few validators.
- Modification to the entire validation process that doesn't affect backward compatibility.

This minor version is intended to be updated frequently as pull requests increase.

### Patch version

The patch version increases with the following changes.

- Bug fixes
- Refactors that don't change the features.

## Contribution Guide

This section is aimed at contributors who want to add their own validators. If you want to change the core process of `autoware_lanelet2_map_validator`, please open a PR and discuss it with the maintainers.

### 1. Implement your validator

<!--- cSpell:disable --->

`autoware_lanelet2_map_validator` is based on the [Lanelet2 library provided by fzi-forschungszentrum-informatik](https://github.com/fzi-forschungszentrum-informatik/Lanelet2).

<!--- cSpell:enable --->

Contributors are encouraged to make their validators by following the class structure shown in [`validator_template.cpp`](https://github.com/tier4/autoware_lanelet2_map_validator/blob/main/autoware_lanelet2_map_validator/template/validator_template.cpp) and [`validator_template.hpp`](https://github.com/tier4/autoware_lanelet2_map_validator/blob/main/autoware_lanelet2_map_validator/template/validator_template.hpp).

Note that the main thing to do for a validator is to output a `lanelet::validation::Issues (a.k.a std::vector<lanelet::validation::Issue>)` object, and the details of the issue is defined in [`issues_info.json`](https://github.com/tier4/autoware_lanelet2_map_validator/blob/main/autoware_lanelet2_map_validator/config/issues_info.json). The title of a each JSON block is an _issue_code_ which is written in a rule like "Category.ValidatorNameInCamelCase-XXX". For the issue message, an English issue message is mandatory. You can also represent substitutions by using the brackets `{}` like the example below but do not forget to write the substitution in your implementation.

```json
"Intersection.IntersectionAreaValidity-001": {
  "severity": "Error",
  "primitive": "polygon",
  "message": {
    "en": "This intersection_area doesn't satisfy boost::geometry::is_valid. (reason: {boost_geometry_message})",
    "ja": "この intersection_area は boost::geometry::is_valid を満たしていません。（理由： {boost_geometry_message}）"
  }
}
```

The following `1-a` to `1-d` are tips that might help you.

#### 1-a. `create_new_validator.py` may be useful

You can use the script [`create_new_validator.py`](https://github.com/tier4/autoware_lanelet2_map_validator/blob/main/autoware_lanelet2_map_validator/template/create_new_validator.py) to generate the required files below.

- Source codes (cpp and hpp)
- Test code (cpp)
- Document file (md)

You can use this by the command like this example:

```shell
create_new_validator.py \
--base_directory ./ \
--category_name traffic_light \
--code_name traffic_light_facing \
--class_name TrafficLightFacingValidator \
--validator_name mapping.traffic_light.correct_facing \
--check_function_name check_traffic_light_facing
```

OR

```shell
ros2 run autoware_lanelet2_map_validator create_new_validator.py \
--base_directory ./ \
--category_name traffic_light \
--code_name traffic_light_facing \
--class_name TrafficLightFacingValidator \
--validator_name mapping.traffic_light.correct_facing \
--check_function_name check_traffic_light_facing
```

All arguments are required.

- `--base_directory`: The directory to the `autoware_lanelet2_map_validator` package.
- `--category_name`: The category (like lanelet, traffic_light...) where your validator belongs to. Look [Design Concept](#design-concept) to see the list of categories.
- `--code_name`: The name for the files. The source code names will be like `<code_name>.cpp` and `<code_name.hpp>`
- `--class_name`: The base class name of your validator which will be defined in your new header file.
- `--validator_name`: The name of the validator which will be displayed when `autoware_lanelet2_map_validator` is executed with a `--print` option. The naming rules are explained in [Restrictions for validator class implementation](#1-c-restrictions-for-validator-class-implementation).
- `--check_function_name`: The main function name of your validator which will be defined in your header file, and its implementation will be written in the cpp source file.

It may be quicker to recognize what this script do by trying the command out.
If you feel typing these arguments exhausting, you can overwrite the `default` value in the python script, but do not forget not to commit those changes.

#### 1-b. Restrictions for path structure

- The source file (`.cpp`) must belong to `src/validators/\<CATEGORY\>/`
- Avoid source file names that are the same as those in other categories.
- The header file (`.hpp`) must belong to `src/include/lanelet2_map_validator/validators/\<CATEGORY\>/`
- Currently, there are no naming rules for source and header files, but the pair of source and header files should have the same name.

#### 1-c. Restrictions for validator class implementation

- Define the name of the validator in the header file (`.hpp` file).
  - The name must follow the structure `aaa.bbb.ccc`
    - The first part (`aaa`) must be either `mapping`, `routing` or `rule`
    - The second part (`bbb`) should be either `general`, `lane`, `stop_line`, `intersection`, `traffic_light`, `crosswalk`, `area`, `others`.
    - The third part can be anything, as long as it is not hard to recognize the validator's feature.
  - The issue code of the validator will be generated from this name. It removes the first part of the name, converts it to upper camel case, and adds a number for classification. (e. g. `Bbb.Ccc-001`)
- Write your implementation in the `operator()` function that outputs an [Issues (a.k.a vector\<Issue\>) object](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_validation/include/lanelet2_validation/Issue.h). Not all of the implementation has to be written in the operator; you can privately define and use functions in your validator class.
- You can use the `construct_issue_from_code` function to generate the Issue object from the `issues_info.json`. The first argument is the issue code which can be done by `issue_code(this->name(), n)`, the second argument is the ID of the primitive, and the third argument (optional) is a string-to-string map if your issue message requires it.
- Currently, there are no rules to decide the severity of the issue. If you're not confident about your severity decisions please discuss them with your PR reviewers.
- Other coding rules are mentioned in the [Autoware Documentation](https://autowarefoundation.github.io/autoware-documentation/main/contributing/). However, this coding rule doesn't hold if it conflicts with the Lanelet2 library.

#### Parameters

If your validator needs parameters, you can add them to [config/params.yaml](../config/params.yaml).
Then, call [ValidatorConfigStore::parameters()](../src/include/lanelet2_map_validator/config_store.hpp) to get all the parameters from `params.yaml`.
`ValidatorConfigStore::parameters()[\<name of validator\>]` will return the parameters for your validator only.
You can call this code anywhere in your implementation.
The parameters can be defined in the YAML map format like the following.

```yaml
mapping.category.validator_name:
  parameter_a: 0.5
  parameter_b: true
```

Note that you should declare the validator's name first and then write the parameters below it.

### 2. Write a test code

Contributors must also provide test codes to ensure your validator is working properly and be able to be tested again when changes occur to the validator in the future.

#### Restrictions for path structure

- The source code (`.cpp`) must belong to `test/src/`.
  - The test codes are not categorized because there are few codes, but they might be categorized in the future.
- The source code name should be `test_<ORIGINAL_SOURCE_NAME>.cpp`
- The maps (`.osm`) for testing must belong to `test/data/map/\<CATEGORY\>/`
- The JSON files (`.json`) for testing must belong to `test/data/json/`

#### Restrictions for test code implementation

- Tests should be executable by `colcon test`. It is strongly recommended to use the [gtest (googletest) format](https://github.com/google/googletest).
- If possible, the `MapValidationTester` class may be useful to inherit common map loading process.
- The test code must contain the following.
  - A test function that checks whether the validator is available.
  - A test function for each unique issue the validator can detect. It is recommended to create a small lanelet2 map for each unique issue.
    - In this test, please also check that the issue code is emitted as expected.
  - A test function ensuring that no issues occur when validating `test/data/map/sample_map.osm`. If `sample_map.osm` violates the validation or doesn't contain the primitive to validate, please fix or add the primitives to it.

### 3. Test the entire validator

Please check that the `autoware_lanelet2_map_validator` works perfectly.

1. Execute `colcon test --packages-select autoware_lanelet2_map_validator --event-handlers console_cohesion+` and confirm that all tests pass.
2. Execute the following command and confirm that no issues appear.

```bash
ros2 run autoware_lanelet2_map_validator autoware_lanelet2_map_validator -p mgrs -m <PATH_TO_sample_map.osm> -i <PATH_TO_autoware_requirement_set.json> -o ./
```

### 4. Write a document

Contributors must provide documentation to explain what the validator can do.
The document must explain the following.

- The validator's name
- Feature of the validator
- The source code where the validator is implemented
- A table of issues that the validator can detect. The following details are required.
  - Issue Code
  - Message
  - Severity
  - Primitive
  - Description of the issue
  - Approach to fix the issue

In addition, add a link of the document to the table [Relationship between requirements and validators](https://github.com/tier4/autoware_lanelet2_map_validator/tree/main/map/autoware_lanelet2_map_validator#relationship-between-requirements-and-validators) in the main `README.md` to let the users know which map requirement your validator relates with.

### 5. Submit a pull request

Submit a pull request to the [tier4/autoware_lanelet2_map_validator](https://github.com/tier4/autoware_lanelet2_map_validator) repository.
