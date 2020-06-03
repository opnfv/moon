Feature: Meta Rule

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


  Scenario: Add meta rules
    When the user sets to add the following meta-rule
      | metarulename | subjectmetadata                   | actionmetadata                 | objectmetadata   | metaruledescription   |
      | A-rule       | Affiliation:                      | Action-Class:                  | Clearance:       | AThisisabasicmetarule |
      | Z-rule       | Authorization-Level:,Affiliation: | Action-Priority:,Action-Class: | Type:,Clearance: | ZThisisabasicmetarule |
    Then the following meta-rules should be existed in the system
      | metarulename | metaruledescription   | subjectmetadata                   | actionmetadata                 | objectmetadata   |
      | A-rule       | AThisisabasicmetarule | Affiliation:                      | Action-Class:                  | Clearance:       |
      | Z-rule       | ZThisisabasicmetarule | Authorization-Level:,Affiliation: | Action-Priority:,Action-Class: | Type:,Clearance: |

  Scenario Outline: Add meta-rule validations
    When the user sets to add the following meta-rule
      | metarulename   | metaruledescription   | subjectmetadata   | actionmetadata   | objectmetadata   |
      | <metarulename> | <metaruledescription> | <subjectmetadata> | <actionmetadata> | <objectmetadata> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | metarulename | metaruledescription  | subjectmetadata                                                           | actionmetadata                                                            | objectmetadata                                                            | flag  |
      |              | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    |                      | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | True  |
      | 1            | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | True  |
      | _%metarule%_ | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | True  |
      | metarule1    | Thisisabasicmetarule |                                                                           | Action-Class:                                                             | Clearance:                                                                | True  |
      | metarule1    | Thisisabasicmetarule | 00000000000000000000000000000000000000000                                 | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | 0000000000000000000000000000000000000000000000000000000000000000          | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | 0000000000000000000000000000000000000000000000000000000000000000000000000 | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:,,Authorization-Level:                                        | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              |                                                                           | Clearance:                                                                | True  |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | 00000000000000000000000000000000000000000                                 | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | 0000000000000000000000000000000000000000000000000000000000000000          | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | 0000000000000000000000000000000000000000000000000000000000000000000000000 | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:,,Action-Priority:                                           | Clearance:                                                                | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             |                                                                           | True  |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | 00000000000000000000000000000000000000000                                 | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | 0000000000000000000000000000000000000000000000000000000000000000          | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | 0000000000000000000000000000000000000000000000000000000000000000000000000 | False |
      | metarule1    | Thisisabasicmetarule | Affiliation:                                                              | Action-Class:                                                             | Clearance:,,Type:                                                         | False |

  Scenario Outline: Add an existing meta-rule
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to add the following meta-rule
      | metarulename   | metaruledescription   | subjectmetadata   | actionmetadata   | objectmetadata   |
      | <metarulename> | <metaruledescription> | <subjectmetadata> | <actionmetadata> | <objectmetadata> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata   | objectmetadata | flag  |
      | metarule1    | Thisisabasicmetarule | Service         | Action-Priority: | Service        | False |
      | metarule2    | Thisisabasicmetarule | Affiliation:    | Action-Class:    | Clearance:     | False |

  Scenario: Update meta rules
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata   | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:    | Clearance:     |
      | metarule3    | Thisisabasicmetarule | Affiliation:    | Action-Priority: | Clearance:     |
    When the user sets to update the following meta-rule
      | metarulename | updatedmetarulename | updatedmetaruledescription | updatedsubjectmetadata            | updatedactionmetadata          | updatedobjectmetadata |
      | metarule1    | 1-MR-%              | Thisisabasicmetarule%      | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: | Clearance:,Type:      |
    Then the following meta-rules should be existed in the system
      | metarulename | metaruledescription   | subjectmetadata                   | actionmetadata                 | objectmetadata   |
      | 1-MR-%       | Thisisabasicmetarule% | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: | Clearance:,Type: |
      | metarule3    | Thisisabasicmetarule  | Affiliation:                      | Action-Priority:               | Clearance:       |

  Scenario Outline: Update meta rules validations
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata      | actionmetadata   | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:         | Action-Class:    | Clearance:     |
      | metarule3    | Thisisabasicmetarule | Authorization-Level: | Action-Priority: | Type:          |
    When the user sets to update the following meta-rule
      | metarulename   | updatedmetarulename   | updatedmetaruledescription   | updatedsubjectmetadata   | updatedactionmetadata   | updatedobjectmetadata   |
      | <metarulename> | <updatedmetarulename> | <updatedmetaruledescription> | <updatedsubjectmetadata> | <updatedactionmetadata> | <updatedobjectmetadata> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | metarulename | updatedmetarulename | updatedmetaruledescription | updatedsubjectmetadata                                                    | updatedactionmetadata                                                     | updatedobjectmetadata                                                     | flag  |
      | metarule1    |                     | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | metaruleX           |                            | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | True  |
      | metarule1    | 1                   | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | True  |
      | metarule1    | _%metarule%_        | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | True  |
#      | metarule1    | metarule1           | Thisisabasicmetarule       | 0000000000000000000000                                                    | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | 0000000000000000000000000000000000000000000000000000000000000000          | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | 0000000000000000000000000000000000000000000000000000000000000000000000000 | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:,,Authorization-Level:                                        | Action-Class:                                                             | Clearance:                                                                | False |
#      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | 0000000000000000000000                                                    | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | 0000000000000000000000000000000000000000000000000000000000000000          | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | 0000000000000000000000000000000000000000000000000000000000000000000000000 | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:,,Action-Priority:                                           | Clearance:                                                                | False |
#      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | 0000000000000000000000                                                    | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | 0000000000000000000000000000000000000000000000000000000000000000          | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | 0000000000000000000000000000000000000000000000000000000000000000000000000 | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | Clearance:,,Type:                                                         | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       |                                                                           | Action-Class:                                                             | Clearance:                                                                | True  |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              |                                                                           | Clearance:                                                                | True  |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             |                                                                           | True  |
      | metarule1    | metarule3           | Thisisabasicmetarule       | Affiliation:                                                              | Action-Class:                                                             | Clearance:                                                                | False |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Authorization-Level:                                                      | Action-Priority:                                                          | Type:                                                                     | False |

  Scenario: Update a meta rule that has a recorded rule dependency
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |
    And the following model exists
      | modelname       | modeldescription  | metarule  |
      | universitymodel | Thisisabasicmodel | metarule1 |
    And the following policy exists
      | policyname      | policydescription  | modelname       | genre     |
      | Stanford-Policy | Thisisabasicpolicy | universitymodel | Education |
    And the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford-Policy |
    And the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford-Policy |
    And the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford-Policy |
    And the following subject data exists
      | policyname      | subjectcategory | subjectdataname        | subjectdatadescription                      |
      | Stanford-Policy | Affiliation:    | University-of-Stanford | This data has the value of subject category |
    And the following object data exists
      | policyname      | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford-Policy | Clearance:     | Top-Secret     | This data has the value of object category |
    And the following action data exists
      | policyname      | actioncategory | actiondataname | actiondatadescription                      |
      | Stanford-Policy | Action-Class:  | Severe         | This data has the value of action category |
    And the following subject assignment exists
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford-Policy |
    And the following object assignment exists
      | objectperimetername         | objectcategory | objectdata | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Top-Secret | Stanford-Policy |
    And the following action assignment exists
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford-Policy |
    And the following rule exists
      | rule                                     | metarulename | instructions | policyname      |
      | University-of-Stanford,Top-Secret,Severe | metarule1    | grant        | Stanford-Policy |
    When the user sets to update the following meta-rule
      | metarulename | updatedmetarulename | updatedmetaruledescription | updatedsubjectmetadata | updatedactionmetadata | updatedobjectmetadata |
      | metarule1    | metarule1           | Thisisabasicmetarule       | Authorization-Level:   | Action-Priority:      | Type:                 |
    Then the system should reply the following
      | flag  |
      | False |
    And the following meta-rules should be existed in the system
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |


  Scenario: Delete meta rules
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |
    When the user sets to delete the following meta-rule
      | metarulename |
      | metarule1    |
    Then the following meta-rules should be existed in the system
      | metarulename | metaruledescription | subjectmetadata | actionmetadata | objectmetadata |
      |              |                     |                 |                |                |

  Scenario: Delete meta rules that has a recorded model dependency
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |
    And the following model exists
      | modelname    | modeldescription  | metarule  |
      | generalmodel | Thisisabasicmodel | metarule1 |
    When the user sets to delete the following meta-rule
      | metarulename |
      | metarule1    |
    Then the system should reply the following
      | flag  |
      | False |
    And the following meta-rules should be existed in the system
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |

  Scenario: Delete meta rules after deleting the recorded model dependency
    Given the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata | actionmetadata | objectmetadata |
      | metarule1    | Thisisabasicmetarule | Affiliation:    | Action-Class:  | Clearance:     |
    And the following model exists
      | modelname    | modeldescription  | metarule  |
      | generalmodel | Thisisabasicmodel | metarule1 |
    When the user sets to delete the following model
      | modelname    |
      | generalmodel |
    And the user sets to delete the following meta-rule
      | metarulename |
      | metarule1    |
    Then the following meta-rules should be existed in the system
      | metarulename | metaruledescription | subjectmetadata | actionmetadata | objectmetadata |
      |              |                     |                 |                |                |