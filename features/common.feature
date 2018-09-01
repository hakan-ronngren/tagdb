Feature: All features in one file for DRY reasons

  (To split scenarios into features in a meaningful way, I must first
  find out where to put common step definitions. Behave remembers all
  definitions that it has seen in previous features, but I do not want 
  to rely on execution order.)


  Scenario: list one tag
    Given that the tag "fruit" applies to "apple,banana,lemon"
    When I enter: "tagdb list fruit"
    Then the output lines should be "apple,banana,lemon" in any order

  Scenario: list two tags
    Given that the tag "fruit" applies to "apple,banana,lemon"
    And that the tag "yellow" applies to "banana,butter,chicken,lemon"
    When I enter: "tagdb list yellow fruit"
    Then the output lines should be "banana,lemon" in any order

  Scenario: list not mathing a tag
    Given that the tag "fruit" applies to "apple,banana,lemon"
    When I enter: "tagdb list animal"
    Then the output should be empty


  Scenario: set an new tag to an object
    When I enter: "tagdb tag fruit banana"
    And I enter: "tagdb list fruit"
    Then the output lines should be "banana" in any order

  Scenario: set an existing tag to an object
    Given that the tag "fruit" applies to "apple"
    When I enter: "tagdb tag fruit banana"
    And I enter: "tagdb list fruit"
    Then the output lines should be "apple,banana" in any order

  Scenario: set multiple tags to an object
    Given that the tag "yellow" applies to "butter"
    And that the tag "fruit" applies to "apple"
    When I enter: "tagdb tag yellow fruit banana"
    And I enter: "tagdb list fruit"
    Then the output lines should be "apple,banana" in any order
    When I enter: "tagdb list yellow"
    Then the output lines should be "banana,butter" in any order
