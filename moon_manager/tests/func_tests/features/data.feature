Feature: Data

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
      | universitymodel  | Thisisabasicmodel | metarule1                     |
      | universitymodel2 | Thisisabasicmodel | metarule3,metarule5,metarule8 |
      | universitymodel3 | Thisisabasicmodel | metarule8                     |
      | universitymodel4 | Thisisabasicmodel | metarule9                     |
    And the following policy exists
      | policyname       | policydescription      | modelname        | genre     |
      | Stanford Policy  | This is a basic policy | universitymodel  | Education |
      | Cambridge Policy | This is a basic policy | universitymodel3 | Education |
      | MIT Policy       | This is a basic policy | universitymodel2 | Education |
      | Oxford Policy    | This is a basic policy | universitymodel4 | Education |


  Scenario: Add subject data
    When the user sets to add the following subject data
      | policyname       | subjectcategory      | subjectdataname        | subjectdatadescription                      |
      | Cambridge Policy | Authorization-Level: | Teaching-staff         | This data has the value of subject category |
      | MIT Policy       | Authorization-Level: | Teaching-staff         | This data has the value of subject category |
      | MIT Policy       | Affiliation:         | University-of-MIT      | This data has the value of subject category |
      | Oxford Policy    | Affiliation:         | University-of-Oxford   | This data has the value of subject category |
      | Oxford Policy    | Authorization-Level: | Teaching-staff         | This data has the value of subject category |
      | Stanford Policy  | Affiliation:         | University-of-Stanford | This data has the value of subject category |
    Then the following subject data should be existed in the system
      | policyname       | subjectcategory      | subjectdataname        | subjectdatadescription                      |
      | Cambridge Policy | Authorization-Level: | Teaching-staff         | This data has the value of subject category |
      | MIT Policy       | Authorization-Level: | Teaching-staff         | This data has the value of subject category |
      | MIT Policy       | Affiliation:         | University-of-MIT      | This data has the value of subject category |
      | Oxford Policy    | Affiliation:         | University-of-Oxford   | This data has the value of subject category |
      | Oxford Policy    | Authorization-Level: | Teaching-staff         | This data has the value of subject category |
      | Stanford Policy  | Affiliation:         | University-of-Stanford | This data has the value of subject category |

  Scenario Outline: Add subject data validations
    When the user sets to add the following subject data
      | policyname   | subjectcategory   | subjectdataname   | subjectdatadescription   |
      | <policyname> | <subjectcategory> | <subjectdataname> | <subjectdatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname                                                          | subjectcategory                                                     | subjectdataname            | subjectdatadescription                          | flag  |
      |                                                                     | Affiliation:                                                        | University-of-Stanford     | This data has the value of subject category     | False |
      | 000000000000000000000000000000000000000000000000000000000           | Affiliation:                                                        | University-of-Stanford     | This data has the value of subject category     | False |
      | 0000000000000000000000000000000000000000000000000000000000000000    | Affiliation:                                                        | University-of-Stanford     | This data has the value of subject category     | False |
      | 0000000000000000000000000000000000000000000000000000000000000000000 | Affiliation:                                                        | University-of-Stanford     | This data has the value of subject category     | False |
      | Cambridge Policy                                                    | Affiliation:                                                        | University-of-Cambridge    | This data has the value of subject category     | False |
      | Stanford Policy                                                     |                                                                     | University-of-Stanford     | This data has the value of subject category     | False |
      | Stanford Policy                                                     | 000000000000000000000000000000000000000000000000000000000           | University-of-Stanford     | This data has the value of subject category     | False |
      | Stanford Policy                                                     | 0000000000000000000000000000000000000000000000000000000000000000    | University-of-Stanford     | This data has the value of subject category     | False |
      | Stanford Policy                                                     | 0000000000000000000000000000000000000000000000000000000000000000000 | University-of-Stanford     | This data has the value of subject category     | False |
      | Stanford Policy                                                     | Affiliation:                                                        |                            | This data has the value of subject category     | False |
      | Stanford Policy                                                     | Affiliation:                                                        | _%University-of-Stanford%_ | This data has the value of subject category     | True  |
      | Stanford Policy                                                     | Affiliation:                                                        | 1                          | This data has the value of subject category     | True  |
      | Stanford Policy                                                     | Affiliation:                                                        | University-of-Stanford     |                                                 | True  |
      | Stanford Policy                                                     | Affiliation:                                                        | University-of-Stanford     | _%This data has the value of subject category%_ | True  |

  Scenario Outline: Add an existing subject data
    Given the following subject data exists
      | policyname      | subjectcategory | subjectdataname        | subjectdatadescription                      |
      | Stanford Policy | Affiliation:    | University-of-Stanford | This data has the value of subject category |
    When the user sets to add the following subject data
      | policyname   | subjectcategory   | subjectdataname   | subjectdatadescription   |
      | <policyname> | <subjectcategory> | <subjectdataname> | <subjectdatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname      | subjectcategory | subjectdataname                                    | subjectdatadescription                      | flag  |
      | Stanford Policy | Affiliation:    | University-of-Stanford                             | This data has the value of subject category | False |
      | Stanford Policy | Affiliation:    | University-of-Stanford,Faculty-of-Computer-Science | This data has the value of subject category | True  |

  Scenario: Delete subject data
    Given the following subject data exists
      | policyname      | subjectcategory | subjectdataname        | subjectdatadescription                      |
      | Stanford Policy | Affiliation:    | University-of-Stanford | This data has the value of subject category |
    When the user sets to delete the following subject data
      | policyname      | subjectcategory | subjectdataname        |
      | Stanford Policy | Affiliation:    | University-of-Stanford |
    Then the following subject data should be existed in the system
      | policyname | subjectcategory | subjectdataname | subjectdatadescription |
      |            |                 |                 |                        |

  Scenario: Delete subject data that has a recorded assignment dependency
    Given the following subject data exists
      | policyname      | subjectcategory | subjectdataname        | subjectdatadescription                      |
      | Stanford Policy | Affiliation:    | University-of-Stanford | This data has the value of subject category |
    And the following subject perimeter exists
      | policies        | subjectperimetername | subjectperimeterdescription                  | subjectperimeteremail | subjectperimeterpassword |
      | Stanford Policy | JohnLewis            | This data has the value of subject perimeter | jlewis@orange.com     | abc1234                  |
    And the following subject assignment exists
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | John Lewis           | Affiliation:    | University-of-Stanford | Stanford Policy |
    When the user sets to delete the following subject data
      | policyname      | subjectcategory | subjectdataname        |
      | Stanford Policy | Affiliation:    | University-of-Stanford |
    Then the system should reply the following
      | flag |
      | True |
    And the following subject data should be existed in the system
      | policyname | subjectcategory | subjectdataname | subjectdatadescription |
      |            |                 |                 |                        |


  Scenario: Add object data
    When the user sets to add the following object data
      | policyname       | objectcategory | objectdataname | objectdatadescription                      |
      | Cambridge Policy | Type:          | Adminstrative  | This data has the value of object category |
      | MIT Policy       | Type:          | Adminstrative  | This data has the value of object category |
      | MIT Policy       | Clearance:     | Confidential   | This data has the value of object category |
      | Oxford Policy    | Type:          | Adminstrative  | This data has the value of object category |
      | Oxford Policy    | Clearance:     | Confidential   | This data has the value of object category |
      | Stanford Policy  | Clearance:     | Confidential   | This data has the value of object category |

    Then the following object data should be existed in the system
      | policyname       | objectcategory | objectdataname | objectdatadescription                      |
      | Cambridge Policy | Type:          | Adminstrative  | This data has the value of object category |
      | MIT Policy       | Type:          | Adminstrative  | This data has the value of object category |
      | MIT Policy       | Clearance:     | Confidential   | This data has the value of object category |
      | Oxford Policy    | Type:          | Adminstrative  | This data has the value of object category |
      | Oxford Policy    | Clearance:     | Confidential   | This data has the value of object category |
      | Stanford Policy  | Clearance:     | Confidential   | This data has the value of object category |

  Scenario Outline: Add object data validations
    When the user sets to add the following object data
      | policyname   | objectcategory   | objectdataname   | objectdatadescription   |
      | <policyname> | <objectcategory> | <objectdataname> | <objectdatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname                                                          | objectcategory                                                      | objectdataname   | objectdatadescription                          | flag  |
      |                                                                     | Clearance:                                                          | Confidential     | This data has the value of object category     | False |
      | 000000000000000000000000000000000000000000000000000000000           | Clearance:                                                          | Confidential     | This data has the value of object category     | False |
      | 0000000000000000000000000000000000000000000000000000000000000000    | Clearance:                                                          | Confidential     | This data has the value of object category     | False |
      | 0000000000000000000000000000000000000000000000000000000000000000000 | Clearance:                                                          | Confidential     | This data has the value of object category     | False |
      #| Cambridge Policy                                                    | Clearance:                                                          | Confidential     | This data has the value of object category     | False |
      | Stanford Policy                                                     |                                                                     | Confidential     | This data has the value of object category     | False |
      #| Stanford Policy                                                     | Type:                                                               | Confidential     | This data has the value of object category     | False |
      | Stanford Policy                                                     | 000000000000000000000000000000000000000000000000000000000           | Confidential     | This data has the value of object category     | False |
      | Stanford Policy                                                     | 0000000000000000000000000000000000000000000000000000000000000000    | Confidential     | This data has the value of object category     | False |
      | Stanford Policy                                                     | 0000000000000000000000000000000000000000000000000000000000000000000 | Confidential     | This data has the value of object category     | False |
      | Stanford Policy                                                     | Clearance:                                                          |                  | This data has the value of object category     | False |
      | Stanford Policy                                                     | Clearance:                                                          | _%Confidential%_ | This data has the value of object category     | True  |
      | Stanford Policy                                                     | Clearance:                                                          | 1                | This data has the value of object category     | True  |
      | Stanford Policy                                                     | Clearance:                                                          | Confidential     |                                                | True  |
      | Stanford Policy                                                     | Clearance:                                                          | Confidential     | _%This data has the value of object category%_ | True  |

  Scenario Outline: Add an existing object data
    Given the following object data exists
      | policyname      | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford Policy | Clearance:     | Confidential   | This data has the value of object category |
    When the user sets to add the following object data
      | policyname   | objectcategory   | objectdataname   | objectdatadescription   |
      | <policyname> | <objectcategory> | <objectdataname> | <objectdatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname      | objectcategory | objectdataname | objectdatadescription                      | flag  |
      | Stanford Policy | Clearance:     | Confidential   | This data has the value of object category | False |
      | Stanford Policy | Clearance:     | Top-Secret     | This data has the value of object category | True  |

  Scenario: Delete object data
    Given the following object data exists
      | policyname      | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford Policy | Clearance:     | Top-Secret     | This data has the value of object category |
    When the user sets to delete the following object data
      | policyname      | objectcategory | objectdataname |
      | Stanford Policy | Clearance:     | Top-Secret     |
    Then the following object data should be existed in the system
      | policyname | objectcategory | objectdataname | objectdatadescription |
      |            |                |                |                       |

  Scenario: Delete object data that has a recorded assignment dependency
    Given the following object data exists
      | policyname       | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford Policy  | Clearance:     | Top-Secret     | This data has the value of object category |
      | Cambridge Policy | Type:          | Top-Secret     | This data has the value of object category |
    And the following object perimeter exists
      | policies        | objectperimetername         | objectperimeterdescription                  |
      | Stanford Policy | ProfessorsPromotionDocument | This data has the value of object perimeter |
    And the following object assignment exists
      | objectperimetername         | objectcategory | objectdata | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Top-Secret | Stanford Policy |
    When the user sets to delete the following object data
      | policyname      | objectcategory | objectdataname |
      | Stanford Policy | Clearance:     | Top-Secret     |
    Then the system should reply the following
      | flag |
      | True |
    And the following object data should be existed in the system
      | policyname       | objectcategory | objectdataname | objectdatadescription                      |
      | Cambridge Policy | Type:          | Top-Secret     | This data has the value of object category |


  Scenario: Add action data
    When the user sets to add the following action data
      | policyname       | actioncategory   | actiondataname | actiondatadescription                      |
      | Cambridge Policy | Action-Priority: | high           | This data has the value of action category |
      | MIT Policy       | Action-Priority: | high           | This data has the value of action category |
      | MIT Policy       | Action-Class:    | Severe         | This data has the value of action category |
      | Oxford Policy    | Action-Priority: | high           | This data has the value of action category |
      | Oxford Policy    | Action-Class:    | Severe         | This data has the value of action category |
      | Stanford Policy  | Action-Class:    | Severe         | This data has the value of action category |

    Then the following action data should be existed in the system
      | policyname       | actioncategory   | actiondataname | actiondatadescription                      |
      | Cambridge Policy | Action-Priority: | high           | This data has the value of action category |
      | MIT Policy       | Action-Priority: | high           | This data has the value of action category |
      | MIT Policy       | Action-Class:    | Severe         | This data has the value of action category |
      | Oxford Policy    | Action-Priority: | high           | This data has the value of action category |
      | Oxford Policy    | Action-Class:    | Severe         | This data has the value of action category |
      | Stanford Policy  | Action-Class:    | Severe         | This data has the value of action category |

  Scenario Outline: Add action data validations
    When the user sets to add the following action data
      | policyname   | actioncategory   | actiondataname   | actiondatadescription   |
      | <policyname> | <actioncategory> | <actiondataname> | <actiondatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname                                                          | actioncategory                                                      | actiondataname | actiondatadescription                          | flag  |
      |                                                                     | Action-Class:                                                       | Severe         | This data has the value of action category     | False |
      | 000000000000000000000000000000000000000000000000000000000           | Action-Class:                                                       | Severe         | This data has the value of action category     | False |
      | 0000000000000000000000000000000000000000000000000000000000000000    | Action-Class:                                                       | Severe         | This data has the value of action category     | False |
      | 0000000000000000000000000000000000000000000000000000000000000000000 | Action-Class:                                                       | Severe         | This data has the value of action category     | False |
      #| Cambridge Policy                                                    | Action-Class:                                                       | Severe         | This data has the value of action category     | False |
      | Stanford Policy                                                     |                                                                     | Severe         | This data has the value of action category     | False |
      | Stanford Policy                                                     | 000000000000000000000000000000000000000000000000000000000           | Severe         | This data has the value of action category     | False |
      | Stanford Policy                                                     | 0000000000000000000000000000000000000000000000000000000000000000    | Severe         | This data has the value of action category     | False |
      | Stanford Policy                                                     | 0000000000000000000000000000000000000000000000000000000000000000000 | Severe         | This data has the value of action category     | False |
      | Stanford Policy                                                     | Action-Class:                                                       |                | This data has the value of action category     | False |
      | Stanford Policy                                                     | Action-Class:                                                       | _%Severe%_     | This data has the value of action category     | True  |
      | Stanford Policy                                                     | Action-Class:                                                       | 1              | This data has the value of action category     | True  |
      | Stanford Policy                                                     | Action-Class:                                                       | Severe         |                                                | True  |
      | Stanford Policy                                                     | Action-Class:                                                       | Severe         | _%This data has the value of action category%_ | True  |

  Scenario Outline: Add an existing action data
    Given the following action data exists
      | policyname      | actioncategory | actiondataname | actiondatadescription                      |
      | Stanford Policy | Action-Class:  | Severe         | This data has the value of action category |
    When the user sets to add the following action data
      | policyname   | actioncategory   | actiondataname   | actiondatadescription   |
      | <policyname> | <actioncategory> | <actiondataname> | <actiondatadescription> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname      | actioncategory | actiondataname | actiondatadescription                      | flag  |
      | Stanford Policy | Action-Class:  | Severe         | This data has the value of action category | False |
      | Stanford Policy | Action-Class:  | high           | This data has the value of action category | True  |

  Scenario: Delete action data
    Given the following action data exists
      | policyname      | actioncategory | actiondataname | actiondatadescription                      |
      | Stanford Policy | Action-Class:  | Severe         | This data has the value of action category |
    When the user sets to delete the following action data
      | policyname      | actioncategory | actiondataname |
      | Stanford Policy | Action-Class:  | Severe         |
    Then the following action data should be existed in the system
      | policyname | actioncategory | actiondataname | actiondatadescription |
      |            |                |                |                       |

  Scenario: Delete action data that has a recorded assignment dependency
    Given the following action data exists
      | policyname       | actioncategory   | actiondataname | actiondatadescription                      |
      | Stanford Policy  | Action-Class:    | Severe         | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | Medium         | This data has the value of action category |
    And the following action perimeter exists
      | policies        | actionperimetername | actionperimeterdescription                  |
      | Stanford Policy | Read                | This data has the value of action perimeter |
    And the following action assignment exists
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
    When the user sets to delete the following action data
      | policyname      | actioncategory | actiondataname |
      | Stanford Policy | Action-Class:  | Severe         |
    Then the system should reply the following
      | flag |
      | True |
    And the following action data should be existed in the system
      | policyname       | actioncategory   | actiondataname | actiondatadescription                      |
      | Cambridge Policy | Action-Priority: | Medium         | This data has the value of action category |
