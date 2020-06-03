Feature: Meta Data ( Category )

 Background:
    Given the system has no rules
    And the system has no subject assignments
    And the system has no action assignments
    And the system has no object assignments
    And the system has no subject data
    And the system has no action data
    And the system has no object data
    And the system has no subject perimeter
    And the system has no object perimeter
    And the system has no action perimeter
    And the system has no pdps
    And the system has no policies
    And the system has no models
    And the system has no meta-rules
    And the system has no subject categories
    And the system has no action categories
    And the system has no object categories



  Scenario: Add subject category
    When the user sets to add the following meta data subject category
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    Then the following meta data subject category should be existed in the system
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |

  Scenario Outline: Add meta data subject validations
    When the user sets to add the following meta data subject category
      | subjectmetadataname   | subjectmetadatadescription   |
      | <subjectmetadataname> | <subjectmetadatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | subjectmetadataname | subjectmetadatadescription                                      | flag  |
      |                     | This meta data has the categorical information about a subject  | False |
      | Affiliation:        |                                                                 | True  |
      | 1                   | This meta data has the categorical information about a subject% | True  |
      | _%Affiliation:%_    | This meta data has the categorical information about a subject  | True  |

  Scenario: Add an existing meta data subject
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                       |
      | Affiliation:        | This meta data has the categorical information about an subject1 |
    When the user sets to add the following meta data subject category
      | subjectmetadataname | subjectmetadatadescription                                       |
      | Affiliation:        | This meta data has the categorical information about an subject1 |
    Then the system should reply the following
      | flag  |
      | False |

  Scenario: Delete subject category
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    When the user sets to delete the following meta data subject category
      | subjectmetadataname |
      | Affiliation:        |
    Then the following meta data subject category should be existed in the system
      | subjectmetadataname | subjectmetadatadescription |
      |                     |                            |

  Scenario: Delete subject category that has a recorded meta-rule dependency
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription       | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | This is a basic meta rule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta data subject category
      | subjectmetadataname |
      | Affiliation:        |
    Then the system should reply the following
      | flag  |
      | False |
    And the following meta data subject category should be existed in the system
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |

  Scenario: Delete subject category after deleting the recorded meta-rule dependency
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription       | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | This is a basic meta rule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta-rule
      | metarulename |
      | metarule1    |
    And the user sets to delete the following meta data subject category
      | subjectmetadataname |
      | Affiliation:        |
    Then the following meta data subject category should be existed in the system
      | subjectmetadataname | subjectmetadatadescription |
      |                     |                            |


  Scenario: Add object category
    When the user sets to add the following meta data object category
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    Then the following meta data object category should be existed in the system
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |

  Scenario Outline: Add meta data object validations
    When the user sets to add the following meta data object category
      | objectmetadataname   | objectmetadatadescription   |
      | <objectmetadataname> | <objectmetadatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | objectmetadataname | objectmetadatadescription                                        | flag  |
      |                    | This meta data has the categorical information about an object   | False |
      | Clearance:         |                                                                  | True  |
      | 1                  | This meta data has the categorical information about an object % | True  |
      | _%Clearance:%_     | This meta data has the categorical information about an object   | True  |

  Scenario: Add an existing meta data object
    Given the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    When the user sets to add the following meta data object category
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    Then the system should reply the following
      | flag  |
      | False |

  Scenario: Delete object category
    Given the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                       |
      | Clearance:         | This meta data has the categorical information about an object1 |
    When the user sets to delete the following meta data object category
      | objectmetadataname |
      | Clearance:         |
    Then the following meta data object category should be existed in the system
      | objectmetadataname | objectmetadatadescription |
      |                    |                           |

  Scenario: Delete object category that has a recorded meta-rule dependency
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription       | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | This is a basic meta rule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta data object category
      | objectmetadataname |
      | Clearance:         |
    Then the system should reply the following
      | flag  |
      | False |
    And the following meta data object category should be existed in the system
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |

  Scenario: Delete object category after deleting the recorded meta-rule dependency
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription       | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | This is a basic meta rule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta-rule
      | metarulename |
      | metarule1    |
    And the user sets to delete the following meta data object category
      | objectmetadataname |
      | Clearance:         |
    Then the following meta data object category should be existed in the system
      | objectmetadataname | objectmetadatadescription |
      |                    |                           |


  Scenario: Add action category
    When the user sets to add the following meta data action category
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    Then the following meta data action category should be existed in the system
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |

  Scenario Outline: Add meta data action validations
    When the user sets to add the following meta data action category
      | actionmetadataname   | actionmetadatadescription   |
      | <actionmetadataname> | <actionmetadatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | actionmetadataname | actionmetadatadescription                                        | flag  |
      |                    | This meta data has the categorical information about the action  | False |
      | Action-Class:      |                                                                  | True  |
      | 1                  | This meta data has the categorical information about the action% | True  |
      | _%Action-Class:%_  | This meta data has the categorical information about the action  | True  |

  Scenario: Add an existing meta data action
    Given the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    When the user sets to add the following meta data action category
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    Then the system should reply the following
      | flag  |
      | False |

  Scenario: Delete action category
    Given the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    When the user sets to delete the following meta data action category
      | actionmetadataname |
      | Action-Class:      |
    Then the following meta data action category should be existed in the system
      | actionmetadataname | actionmetadatadescription |
      |                    |                           |

  Scenario: Delete action category that has a recorded meta-rule
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription       | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | This is a basic meta rule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta data action category
      | actionmetadataname |
      | Action-Class:      |
    Then the system should reply the following
      | flag  |
      | False |
    And the following meta data action category should be existed in the system
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |

  Scenario: Delete action Category after deleting the recorded meta-rule dependency
    Given the following meta data subject category exists
      | subjectmetadataname | subjectmetadatadescription                                     |
      | Affiliation:        | This meta data has the categorical information about a subject |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription       | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | This is a basic meta rule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta-rule
      | metarulename |
      | metarule1    |
    And the user sets to delete the following meta data action category
      | actionmetadataname |
      | Action-Class:      |
    Then the following meta data action category should be existed in the system
      | actionmetadataname | actionmetadatadescription |
      |                    |                           |

