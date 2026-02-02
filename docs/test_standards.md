# Purpose

Defines testing standards in this repository.

## Overview

All tests follow the Arrange - Act - Assert pattern and full test suite should run in under three seconds. We use dependency injection (DI) in our production code to support use of mock objects rather than patches. Tests, fixtures, and objects under test all follow strict naming conventions for readability and clarity of intent.

## Testing paradigm

All tests follow the Arrange - Act - Assert pattern as proposed by Bill Wake in 2001. Each test focuses on one specific aspect or behavior of the code. All tests are geared towards testing of behavior rather than internals.

## Performance

The full test suite should complete in under three seconds to promote continuous and low-friction testing during development and routine operations.

## Dependency injection and fixtures

To the extent possible, this repository organizes production code with dependency injection (DI) to enable streamlined testing practices with mock objects. By default, we attempt to provide mock objects to our tests using fixtures to make test refactoring easier and reduce code duplication. Our rule is to prefer mocks over patching and enable usage of mocks by incorporating DI in our production code. We will maintain our production code to support use of mocks. The only exception to this rule is main.main(), where patching is acceptable to verify program setup.

## Naming tests

### Files and function definitions

- Test files are scoped to one concept and named after the concept, for example:
  - Given concept "storage_service.py" we name the test file "test_storage_service.py"
- Individual test function definitions are named according to the specific element under test, for example:
  - Given the element "YouTubeService.__init__()" we name the test "test_youtube_service_init()"

### Fixtures and objects

- Fixtures that return factory functions are prefixed with "factory_"
- Fixtures that return mock objects are prefixied with "mock_"
- Fixtures that return real concepts follow the same naming conventions in the production code, for example:
  - Given the class "YouTubService", when initialized we use snakecase "youtube_service" and in a fixture we use "youtube_service"
