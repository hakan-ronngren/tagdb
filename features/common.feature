Feature: All features in one file for DRY reasons

  (To split scenarios into features in a meaningful way, I must first
  find out where to put common step definitions. Behave remembers all
  definitions that it has seen in previous features, but I do not want 
  to rely on execution order.)


  Scenario: query what object has one tag
    Given that the tag "fruit" applies to "apple,banana,lemon"
    When I enter: "tagdb list fruit"
    Then the output lines should be "apple,banana,lemon" in any order

  Scenario: query what object has two tags
    Given that the tag "fruit" applies to "apple,banana,lemon"
    And that the tag "yellow" applies to "banana,butter,chicken,lemon"
    When I enter: "tagdb list yellow fruit"
    Then the output lines should be "banana,lemon" in any order

  Scenario: no matches when an object does not have a particular tag
    Given that the tag "fruit" applies to "apple,banana,lemon"
    When I enter: "tagdb list animal"
    Then the output should be empty

  Scenario: exclude a tag
    Given that the tag "fruit" applies to "apple,banana,pear"
    And that the tag "yellow" applies to "banana,butter"
    When I enter: "tagdb list fruit ^yellow"
    Then the output lines should be "apple,pear" in any order

  Scenario: the excluded tag can be the first
    Given that the tag "fruit" applies to "apple,banana,pear"
    And that the tag "yellow" applies to "banana,butter"
    When I enter: "tagdb list ^yellow fruit"
    Then the output lines should be "apple,pear" in any order


  Scenario: query what tags an object has
    Given that the tag "fruit" applies to "banana"
    And that the tag "yellow" applies to "banana"
    When I enter: "tagdb describe banana"
    Then the output lines should be "fruit,yellow" in any order


  Scenario: get an alphabetical list of all existing tags
    Given that the tag "fruit" applies to "banana"
    And that the tag "nut" applies to "cashew"
    And that the tag "meat" applies to "ham"
    And that the tag "dairy" applies to "milk"
    When I enter: "tagdb tags"
    Then the output lines should be "dairy,fruit,meat,nut" in this order


  Scenario: set an new tag to an object
    When I enter: "tagdb tag fruit banana"
    And I enter: "tagdb list fruit"
    Then the output lines should be "banana" in any order

  Scenario: set an existing tag to an object
    Given that the tag "fruit" applies to "apple"
    When I enter: "tagdb tag fruit banana"
    And I enter: "tagdb list fruit"
    Then the output lines should be "apple,banana" in any order

  Scenario: set tag to one object at once (check eof newline on write)
    When I enter: "tagdb tag fruit banana"
    And I enter: "tagdb tag fruit apple"
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
