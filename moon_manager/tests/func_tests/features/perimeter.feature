Feature: Perimeter

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
      | metarulename | metaruledescription  | subjectmetadata                   | actionmetadata                 | objectmetadata   |
      | metarule1    | Thisisabasicmetarule | Affiliation:                      | Action-Class:                  | Clearance:       |
      | metarule2    | Thisisabasicmetarule | Authorization-Level:              | Action-Class:                  | Clearance:       |
      | metarule3    | Thisisabasicmetarule | Affiliation:                      | Action-Priority:               | Clearance:       |
      | metarule4    | Thisisabasicmetarule | Authorization-Level:              | Action-Priority:               | Clearance:       |
      | metarule5    | Thisisabasicmetarule | Affiliation:                      | Action-Class:                  | Type:            |
      | metarule6    | Thisisabasicmetarule | Authorization-Level:              | Action-Class:                  | Type:            |
      | metarule7    | Thisisabasicmetarule | Affiliation:                      | Action-Priority:               | Type:            |
      | metarule8    | Thisisabasicmetarule | Authorization-Level:              | Action-Priority:               | Type:            |
      | metarule9    | Thisisabasicmetarule | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: | Clearance:,Type: |
    And the following model exists
      | modelname        | modeldescription  | metarule                      |
      | universitymodel  | Thisisabasicmodel | metarule1,metarule9           |
      | universitymodel2 | Thisisabasicmodel | metarule3,metarule5,metarule8 |
      | universitymodel3 | Thisisabasicmodel | metarule9                     |
    And the following policy exists
      | policyname       | policydescription      | modelname        | genre     |
      | Stanford Policy  | This is a basic policy | universitymodel  | Education |
      | Cambridge Policy | This is a basic policy | universitymodel2 | Education |


  Scenario: Add subject perimeter
    When the user sets to add the following subject perimeter
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy  |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Cambridge Policy |
    Then the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies                         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Cambridge Policy,Stanford Policy |

  Scenario Outline: Add subject perimeter validations
    When the user sets to add the following subject perimeter
      | subjectperimetername   | subjectperimeterdescription   | subjectperimeteremail   | subjectperimeterpassword   | policies   |
      | <subjectperimetername> | <subjectperimeterdescription> | <subjectperimeteremail> | <subjectperimeterpassword> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        | flag  |
      |                      | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy | False |
      | _%JohnLewis%_        | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy | True  |
      | JohnLewis            |                             | jlewis@orange.com     | abc1234                  | Stanford Policy | True  |
      | JohnLewis            | Thisistheexpecteduser%      | jlewis@orange.com     | abc1234                  | Stanford Policy | True  |
      | JohnLewis            | Thisistheexpecteduser%      | jlewis@orange.com     | abc1234                  |                 | True  |

  Scenario Outline: Add an existing subject perimeter
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    When the user sets to add the following subject perimeter
      | subjectperimetername   | subjectperimeterdescription   | subjectperimeteremail   | subjectperimeterpassword   | policies   |
      | <subjectperimetername> | <subjectperimeterdescription> | <subjectperimeteremail> | <subjectperimeterpassword> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         | flag  |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy  | False |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Cambridge Policy | True  |

  Scenario: Update subject perimeter
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy  |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Cambridge Policy |
    When the user sets to update the following subject perimeter
      | subjectperimetername | updatedsubjectperimetername | updatedsubjectperimeterdescription    | updatedsubjectperimeteremail | updatedsubjectperimeterpassword | policies        |
      | JohnLewis            | JoesephWilliams             | Thisdatahasthevalueofsubjectperimeter | jwilliams@orange.com         | abc1234                         | Stanford Policy |
    Then the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription           | subjectperimeteremail | subjectperimeterpassword | policies                         |
      | JoesephWilliams      | Thisdatahasthevalueofsubjectperimeter | jwilliams@orange.com  | abc1234                  | Cambridge Policy,Stanford Policy |

  Scenario Outline: Update subject perimeter validations
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    When the user sets to update the following subject perimeter
      | subjectperimetername   | updatedsubjectperimetername   | updatedsubjectperimeterdescription   | updatedsubjectperimeteremail   | updatedsubjectperimeterpassword   | policies   |
      | <subjectperimetername> | <updatedsubjectperimetername> | <updatedsubjectperimeterdescription> | <updatedsubjectperimeteremail> | <updatedsubjectperimeterpassword> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | subjectperimetername | updatedsubjectperimetername | updatedsubjectperimeterdescription | updatedsubjectperimeteremail | updatedsubjectperimeterpassword | policies        | flag  |
      #| JohnLewis            |                             | Thisistheexpecteduser              | jlewis@orange.com            | abc1234                         | Stanford Policy | False |
      | JohnLewis            | _%JohnLewis%_               | Thisistheexpecteduser              | jlewis@orange.com            | abc1234                         | Stanford Policy | True  |
      #| JohnLewis            | JohnLewis                   |                                    | jlewis@orange.com            | abc1234                         | Stanford Policy | True  |
      #| JohnLewis            | JohnLewis                   | Thisistheexpecteduser%             | jlewis@orange.com            | abc1234                         | Stanford Policy | True  |

Scenario: Delete subject perimeter with a policy and no assignments
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    When the user sets to delete the following subject perimeter
      | subjectperimetername |
      | JohnLewis            |
    Then the system should reply the following
      | flag  |
      | False |
    And the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |

  Scenario: Check subject perimeter after removing the policy
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    When the user sets to delete the following subject perimeter for a given policy
      | subjectperimetername | policies        |
      | JohnLewis            | Stanford Policy |
    Then the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  |          |

Scenario: Delete subject perimeter with no policy
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    When the user sets to delete the following subject perimeter for a given policy
      | subjectperimetername | policies        |
      | JohnLewis            | Stanford Policy |
    And the user sets to delete the following subject perimeter
      | subjectperimetername |
      | JohnLewis            |
    Then the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies |
      |                      |                             |                       |                          |          |

  Scenario: Delete subject perimeter with a policy and with assignments
    Given the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    And the following subject data exists
      | policyname      | subjectcategory | subjectdataname        | subjectdatadescription                      |
      | Stanford Policy | Affiliation:    | University-of-Stanford | This data has the value of subject category |
      | Stanford Policy | Affiliation:    | Stanford               | This data has the value of subject category |
    And the following subject assignment exists
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
      | JohnLewis            | Affiliation:    | Stanford               | Stanford Policy |
    When the user sets to delete the following subject perimeter for a given policy
      | subjectperimetername | policies        |
      | JohnLewis            | Stanford Policy |
    Then the system should reply the following
      | flag |
      | True |
    And the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  |          |
    And the following subject assignment should be existed in the system
      | subjectperimetername | subjectcategory | subjectdata | policyname      |
      |                      |                 |             | Stanford Policy |

  Scenario: Add object perimeter
    When the user sets to add the following object perimeter
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Cambridge Policy |

    Then the following object perimeter should be existed in the system
      | objectperimetername         | objectperimeterdescription   | policies                         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Cambridge Policy,Stanford Policy |

  Scenario Outline: Add object perimeter validations
    When the user sets to add the following object perimeter
      | objectperimetername   | objectperimeterdescription   | policies   |
      | <objectperimetername> | <objectperimeterdescription> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | objectperimetername             | objectperimeterdescription    | policies        | flag  |
      |                                 | Thisistherequesttoaccessfile  | Stanford Policy | False |
      | _%ProfessorsPromotionDocument%_ | Thisistherequesttoaccessfile  | Stanford Policy | True  |
      | ProfessorsPromotionDocument     |                               | Stanford Policy | True  |
      | ProfessorsPromotionDocument     | Thisistherequesttoaccessfile% | Stanford Policy | True  |
      | ProfessorsPromotionDocument     | Thisistherequesttoaccessfile% |                 | True  |


  Scenario Outline: Add an existing object perimeter
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    When the user sets to add the following object perimeter
      | objectperimetername   | objectperimeterdescription   | policies   |
      | <objectperimetername> | <objectperimeterdescription> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | objectperimetername         | objectperimeterdescription   | policies         | flag  |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  | False |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Cambridge Policy | True  |

  Scenario: Update object perimeter
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Cambridge Policy |
    When the user sets to update the following object perimeter
      | objectperimetername         | updatedobjectperimetername | updatedobjectperimeterdescription | policies        |
      | ProfessorsPromotionDocument | StudentsGradsSheet         | Thisistherequesttoaccessfile      | Stanford Policy |
    Then the following object perimeter should be existed in the system
      | objectperimetername | objectperimeterdescription   | policies                         |
      | StudentsGradsSheet  | Thisistherequesttoaccessfile | Cambridge Policy,Stanford Policy |

  Scenario Outline: Update object perimeter validations
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    When the user sets to update the following object perimeter
      | objectperimetername   | updatedobjectperimetername   | updatedobjectperimeterdescription   | policies   |
      | <objectperimetername> | <updatedobjectperimetername> | <updatedobjectperimeterdescription> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | objectperimetername         | updatedobjectperimetername      | updatedobjectperimeterdescription | policies        | flag  |
      | ProfessorsPromotionDocument |                                 | Thisistherequesttoaccessfile      | Stanford Policy | False |
      | ProfessorsPromotionDocument | _%ProfessorsPromotionDocument%_ | Thisistherequesttoaccessfile      | Stanford Policy | True  |
      | ProfessorsPromotionDocument | ProfessorsPromotionDocument     |                                   | Stanford Policy | True  |
      | ProfessorsPromotionDocument | ProfessorsPromotionDocument     | Thisistherequesttoaccessfile%     | Stanford Policy | True  |

  Scenario: Delete object perimeter with a policy
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    When the user sets to delete the following object perimeter
      | objectperimetername         |
      | ProfessorsPromotionDocument |
    Then the system should reply the following
      | flag  |
      | False |
    And the following object perimeter should be existed in the system
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |

  Scenario: Check object perimeter after removing the policy
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    When the user sets to delete the following object perimeter for a given policy
      | objectperimetername         | policies        |
      | ProfessorsPromotionDocument | Stanford Policy |
    Then the following object perimeter should be existed in the system
      | objectperimetername         | objectperimeterdescription   | policies |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile |          |

  Scenario: Delete object perimeter after removing the policy
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    When the user sets to delete the following object perimeter for a given policy
      | objectperimetername         | policies        |
      | ProfessorsPromotionDocument | Stanford Policy |
    And the user sets to delete the following object perimeter
      | objectperimetername         |
      | ProfessorsPromotionDocument |
    Then the following object perimeter should be existed in the system
      | objectperimetername | objectperimeterdescription | policies |
      |                     |                            |          |

  Scenario: Delete object perimeter with a policy and with assignments
    Given the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    And the following object data exists
      | policyname      | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford Policy | Clearance:     | Top-Secret     | This data has the value of object category |
      | Stanford Policy | Clearance:     | Confidential   | This data has the value of object category |
      | Stanford Policy | Clearance:     | Public         | This data has the value of object category |
      | Stanford Policy | Type:          | Adminstrative  | This data has the value of object category |
      | Stanford Policy | Type:          | Staff          | This data has the value of object category |
    And the following object assignment exists
      | objectperimetername         | objectcategory | objectdata   | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Public       | Stanford Policy |
      | ProfessorsPromotionDocument | Clearance:     | Confidential | Stanford Policy |
    When the user sets to delete the following object perimeter for a given policy
      | objectperimetername        | policies        |
      | ProfessorsPromotionDocument | Stanford Policy |
    Then the system should reply the following
      | flag |
      | True |
    And the following object perimeter should be existed in the system
      | objectperimetername         | objectperimeterdescription   | policies |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile |          |
    And the following object assignment should be existed in the system
      | objectperimetername | objectcategory | objectdata | policyname      |
      |                     |                |            | Stanford Policy |


  Scenario: Add action perimeter
    When the user sets to add the following action perimeter
      | actionperimetername | actionperimeterdescription | policies         |
      | Read                | Thisistheactionrequired    | Stanford Policy  |
      | Read                | Thisistheactionrequired    | Cambridge Policy |
      | Delete              | Thisistheactionrequired    | Stanford Policy  |
      | Delete              | Thisistheactionrequired    | Cambridge Policy |
    Then the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription | policies                         |
      | Delete              | Thisistheactionrequired    | Cambridge Policy,Stanford Policy |
      | Read                | Thisistheactionrequired    | Cambridge Policy,Stanford Policy |

  Scenario Outline: Add action perimeter validations
    When the user sets to add the following action perimeter
      | actionperimetername   | actionperimeterdescription   | policies   |
      | <actionperimetername> | <actionperimeterdescription> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | actionperimetername | actionperimeterdescription | policies        | flag  |
      |                     | Thisistheactionrequired    | Stanford Policy | False |
      | _%Read%_            | Thisistheactionrequired    | Stanford Policy | True  |
      | Read                |                            | Stanford Policy | True  |
      | Read                | Thisistheactionrequired%   | Stanford Policy | True  |
      | Read                | Thisistheactionrequired%   |                 | True  |


  Scenario Outline: Add an existing action perimeter
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
    When the user sets to add the following action perimeter
      | actionperimetername   | actionperimeterdescription   | policies   |
      | <actionperimetername> | <actionperimeterdescription> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | actionperimetername | actionperimeterdescription | policies         | flag  |
      | Read                | Thisistheactionrequired    | Stanford Policy  | False |
      | Read                | Thisistheactionrequired    | Cambridge Policy | True  |

  Scenario: Update action perimeter
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies         |
      | Read                | Thisistheactionrequired    | Stanford Policy  |
      | Read                | Thisistheactionrequired    | Cambridge Policy |
    When the user sets to update the following action perimeter
      | actionperimetername | updatedactionperimetername | updatedactionperimeterdescription | policies        |
      | Read                | Delete                     | Thisistheactionrequired           | Stanford Policy |
    Then the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription | policies                         |
      | Delete              | Thisistheactionrequired    | Cambridge Policy,Stanford Policy |

  Scenario Outline: Update action perimeter validations
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
    When the user sets to update the following action perimeter
      | actionperimetername   | updatedactionperimetername   | updatedactionperimeterdescription   | policies   |
      | <actionperimetername> | <updatedactionperimetername> | <updatedactionperimeterdescription> | <policies> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | actionperimetername | updatedactionperimetername | updatedactionperimeterdescription | policies        | flag  |
      | Read                |                            | Thisistheactionrequired           | Stanford Policy | False |
      | Read                | _%Read%_                   | Thisistheactionrequired           | Stanford Policy | True  |
      | Read                | Read                       |                                   | Stanford Policy | True  |
      | Read                | Read                       | Thisistheactionrequired%          | Stanford Policy | True  |

  Scenario: Delete action perimeter with a policy
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription  | policies        |
      | Read                | This is the action required | Stanford Policy |
    When the user sets to delete the following action perimeter
      | actionperimetername |
      | Read                |
    Then the system should reply the following
      | flag  |
      | False |
    And the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription  | policies        |
      | Read                | This is the action required | Stanford Policy |

  Scenario: Check action perimeter after removing the policy
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
    When the user sets to delete the following action perimeter for a given policy
      | actionperimetername | policies        |
      | Read                | Stanford Policy |
    Then the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription | policies |
      | Read                | Thisistheactionrequired    |          |

  Scenario: Delete action perimeter after removing the policy
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
    When the user sets to delete the following action perimeter for a given policy
      | actionperimetername | policies        |
      | Read                | Stanford Policy |
    And the user sets to delete the following action perimeter
      | actionperimetername |
      | Read                |
    Then the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription | policies |
      |                     |                            |          |

  Scenario: Delete action perimeter with a policy and with assignments
    Given the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
    And the following action data exists
      | policyname      | actioncategory   | actiondataname | actiondatadescription                      |
      | Stanford Policy | Action-Class:    | Severe         | This data has the value of action category |
      | Stanford Policy | Action-Class:    | Low            | This data has the value of action category |
      | Stanford Policy | Action-Priority: | Low            | This data has the value of action category |
    And the following action assignment exists
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
      | Read                | Action-Class:  | Low        | Stanford Policy |
    When the user sets to delete the following action perimeter for a given policy
      | actionperimetername | policies        |
      | Read                | Stanford Policy |
    Then the system should reply the following
      | flag |
      | True |
    And the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription | policies |
      | Read                | Thisistheactionrequired    |          |
    And the following action assignment should be existed in the system
      | actionperimetername | actioncategory | actiondata | policyname      |
      |                     |                |            | Stanford Policy |


