Feature: Model

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
    And the following meta data subject category exists
      | subjectmetadataname  | subjectmetadatadescription                                     |
      | Affiliation:         | This meta data has the categorical information about a subject |
      | Authorization-Level: | This meta data has the categorical information about an object |
      | Degree:              | This meta data has the categorical information about an object |
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
      | Type:              | This meta data has the categorical information about an object |
      | Class:             | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
      | Action-Priority:   | This meta data has the categorical information about an action |
      | Recommendation:    | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription      | subjectmetadata                   | actionmetadata                 | objectmetadata   |
      | metarule1    | This is a basic metarule | Affiliation:                      | Action-Class:                  | Clearance:       |
      | metarule2    | This is a basic metarule | Authorization-Level:              | Action-Class:                  | Clearance:       |
      | metarule3    | This is a basic metarule | Affiliation:                      | Action-Priority:               | Clearance:       |
      | metarule4    | This is a basic metarule | Authorization-Level:              | Action-Priority:               | Clearance:       |
      | metarule5    | This is a basic metarule | Affiliation:                      | Action-Class:                  | Type:            |
      | metarule6    | This is a basic metarule | Authorization-Level:              | Action-Class:                  | Type:            |
      | metarule7    | This is a basic metarule | Affiliation:                      | Action-Priority:               | Type:            |
      | metarule8    | This is a basic metarule | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: | Clearance:,Type: |
      | metarule9    | This is a basic metarule |                                   | Action-Class:,Action-Priority: | Clearance:,Type: |
      | metarule10   | This is a basic metarule | Affiliation:,Authorization-Level: |                                | Clearance:,Type: |
      | metarule11   | This is a basic metarule | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: |                  |


  Scenario: Add model
    When the user sets to add the following model
      | modelname | modeldescription  | metarule                      |
      | A-model   | Thisisabasicmodel | metarule1,metarule2,metarule6 |
      | B-model   | Thisisabasicmodel | metarule3,metarule4,metarule5 |
    Then the following model should be existed in the system
      | modelname | modeldescription  | metarule                      |
      | A-model   | Thisisabasicmodel | metarule1,metarule2,metarule6 |
      | B-model   | Thisisabasicmodel | metarule3,metarule4,metarule5 |

  Scenario Outline: Add model validations
    When the user sets to add the following model
      | modelname   | modeldescription   | metarule   |
      | <modelname> | <modeldescription> | <metarule> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | modelname    | modeldescription                             | metarule                                                                | flag  |
      |              | This model is for creating policy prototype  | metarule8,metarule3                                                     | False |
      | generalmodel |                                              | metarule8                                                               | True  |
      | 1            | This model is for creating policy prototype% | metarule8                                                               | True  |
      | _%model%_    | This model is for creating policy prototype1 | metarule8                                                               | True  |
      | generalmodel | This model is for creating policy prototype  |                                                                         | True  |
      | generalmodel | This model is for creating policy prototype  | metarule9                                                               | True  |
      | generalmodel | This model is for creating policy prototype  | metarule10                                                              | True  |
      | generalmodel | This model is for creating policy prototype  | metarule11                                                              | True  |
      | generalmodel | This model is for creating policy prototype  | metarule20                                                              | False |
      | generalmodel | This model is for creating policy prototype  | metarule3,,metarule20                                                   | False |
      | generalmodel | This model is for creating policy prototype  | 000000000000000000000                                                   | False |
      | generalmodel | This model is for creating policy prototype  | 0000000000000000000000000000000000000000000000000000000000000000000     | False |
      | generalmodel | This model is for creating policy prototype  | 00000000000000000000000000000000000000000000000000000000000000000000000 | False |
      | generalmodel | This model is for creating policy prototype  | metarule8,metarule10                                                    | True  |

Scenario Outline: Add an existing model
    Given the following model exists
      | modelname    | modeldescription      | metarule                      |
      | generalmodel | This is a basic model | metarule1,metarule2,metarule6 |
    When the user sets to add the following model
      | modelname   | modeldescription   | metarule   |
      | <modelname> | <modeldescription> | <metarule> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | modelname     | modeldescription  | metarule                      | flag  |
      | generalmodel  | Thisisabasicmodel | metarule1,metarule3,metarule5 | False |
      | generalmodel1 | Thisisabasicmodel | metarule1,metarule2,metarule6 | False |

  Scenario: Update model
    Given the following model exists
      | modelname    | modeldescription  | metarule                      |
      | generalmodel | Thisisabasicmodel | metarule1,metarule2,metarule6 |
    When the user sets to update the following model
      | modelname    | updatedmodelname | updatedmodeldescription                     | updatedmetarule               |
      | generalmodel | 1-M-%            | This model is for creating policy prototype | metarule3,metarule5,metarule7 |
    Then the following model should be existed in the system
      | modelname | modeldescription                            | metarule                      |
      | 1-M-%     | This model is for creating policy prototype | metarule3,metarule5,metarule7 |

  Scenario Outline: Update model validations
    Given the following model exists
      | modelname    | modeldescription                            | metarule                      |
      | generalmodel | This model is for creating policy prototype | metarule1,metarule2,metarule6 |
    When the user sets to update the following model
      | modelname   | updatedmodelname   | updatedmodeldescription   | updatedmetarule   |
      | <modelname> | <updatedmodelname> | <updatedmodeldescription> | <updatedmetarule> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | modelname    | updatedmodelname | updatedmodeldescription                      | updatedmetarule                                                         | flag  |
      | generalmodel |                  | This model is for creating policy prototype  | metarule8,metarule3                                                     | False |
      | generalmodel | generalmodel     |                                              | metarule8                                                               | True  |
      | generalmodel | 1                | This model is for creating policy prototype% | metarule8                                                               | True  |
      | generalmodel | _%model%_        | This model is for creating policy prototype1 | metarule8                                                               | True  |
      | generalmodel | generalmodel     | This model is for creating policy prototype  |                                                                         | True  |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | metarule9                                                               | True  |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | metarule10                                                              | True  |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | metarule11                                                              | True  |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | metarule3,                                                              | False |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | 0000000000000000000000000000000000000000000000000000000000000000000     | False |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | 00000000000000000000000000000000000000000000000000000000000000000000000 | False |
      | generalmodel | generalmodel     | This model is for creating policy prototype  | metarule8,metarule10                                                    | True  |

  Scenario: Delete a model
    Given the following model exists
      | modelname    | modeldescription                            | metarule  |
      | generalmodel | This model is for creating policy prototype | metarule1 |
    When the user sets to delete the following model
      | modelname    |
      | generalmodel |
    Then the following model should be existed in the system
      | modelname | modeldescription | metarule |
      |           |                  |          |

  Scenario: Delete a model that has a recorded policy dependency
    Given the following model exists
      | modelname    | modeldescription                            | metarule  |
      | generalmodel | This model is for creating policy prototype | metarule1 |
    And the following policy exists
      | policyname    | policydescription      | modelname    | genre     |
      | generalpolicy | This is a basic policy | generalmodel | financial |
    When the user sets to delete the following model
      | modelname    |
      | generalmodel |
    Then the following model should be existed in the system
      | modelname    | modeldescription                            | metarule  |
      | generalmodel | This model is for creating policy prototype | metarule1 |

  Scenario: Delete a model after deleting the recorded policy dependency
    Given the following model exists
      | modelname    | modeldescription                            | metarule  |
      | generalmodel | This model is for creating policy prototype | metarule1 |
    And the following policy exists
      | policyname    | policydescription      | modelname    | genre     |
      | generalpolicy | This is a basic policy | generalmodel | financial |
    When the user sets to delete the following policy
      | policyname    |
      | generalpolicy |
    And the user sets to delete the following model
      | modelname    |
      | generalmodel |
    Then the following model should be existed in the system
      | modelname | modeldescription | metarule |
      |           |                  |          |
