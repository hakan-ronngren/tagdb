Feature: List the objects matching one or several tags

  As a database user
  I want to list all objects that match a set of tags
  So that I can include them in further processing

  Scenario: one tag
    Given that the tag "fruit" applies to "apple,banana,lemon"
    And the daemon is running
    When I issue: "tagdb list fruit"
    Then the output lines should be "apple,banana,lemon" in any order

  Scenario: two tags
    Given that the tag "fruit" applies to "apple,banana,lemon"
    And that the tag "yellow" applies to "banana,butter,chicken,lemon"
    And the daemon is running
    When I issue: "tagdb list yellow fruit"
    Then the output lines should be "banana,lemon" in any order

  Scenario: not mathing a tag
    Given that the tag "fruit" applies to "apple,banana,lemon"
    And the daemon is running
    When I issue: "tagdb list animal"
    Then the output should be empty
