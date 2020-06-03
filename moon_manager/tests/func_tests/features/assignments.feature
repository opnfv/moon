Feature: Assignments

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
      | Cambridge Policy | This is a basic policy | universitymodel3 | Education |
    And the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy  |
      | WilliamsJoeseph      | Thisistheexpecteduser       | wjoeseph@orange.com   | abc1234                  | Stanford Policy  |
      | WilliamsJoeseph      | Thisistheexpecteduser       | wjoeseph@orange.com   | abc1234                  | Cambridge Policy |
      | WilliamsGeorge       | Thisdatahasthevalueofsubjectperimeter | gwilliams@orange.com  | abc1234                  |                 |
    And the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Stanford Policy  |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Cambridge Policy |
      | Vacations                   | Thisistherequesttoaccessfile |                  |
    And the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies         |
      | Read                | Thisistheactionrequired    | Stanford Policy  |
      | Delete              | Thisistheactionrequired    | Stanford Policy  |
      | Delete              | Thisistheactionrequired    | Cambridge Policy |
      | Edit                | Thisistheactionrequired    |                 |
    And the following subject data exists
      | policyname       | subjectcategory      | subjectdataname         | subjectdatadescription                      |
      | Stanford Policy  | Affiliation:         | University-of-Stanford  | This data has the value of subject category |
      | Stanford Policy  | Affiliation:         | Stanford                | This data has the value of subject category |
      | Stanford Policy  | Authorization-Level: | Professor               | This data has the value of subject category |
      | Cambridge Policy | Affiliation:         | University-of-Cambridge | This data has the value of subject category |
      | Cambridge Policy | Authorization-Level: | Professor               | This data has the value of subject category |
      | Cambridge Policy | Authorization-Level: | Lecturer                | This data has the value of subject category |
    And the following object data exists
      | policyname       | objectcategory | objectdataname         | objectdatadescription                      |
      | Stanford Policy  | Clearance:     | Top-Secret             | This data has the value of object category |
      | Stanford Policy  | Clearance:     | Confidential           | This data has the value of object category |
      | Stanford Policy  | Clearance:     | Public                 | This data has the value of object category |
      | Stanford Policy  | Type:          | Adminstrative          | This data has the value of object category |
      | Stanford Policy  | Type:          | Staff                  | This data has the value of object category |
      | Cambridge Policy | Type:          | Adminstrative          | This data has the value of object category |
      | Cambridge Policy | Type:          | Teaching-Staff         | This data has the value of object category |
      | Cambridge Policy | Clearance:     | Confidential           | This data has the value of object category |
      | Cambridge Policy | Clearance:     | Access-with-permission | This data has the value of object category |
      | Cambridge Policy | Clearance:     | Public                 | This data has the value of object category |

    And the following action data exists
      | policyname       | actioncategory   | actiondataname | actiondatadescription                      |
      | Stanford Policy  | Action-Class:    | Severe         | This data has the value of action category |
      | Stanford Policy  | Action-Class:    | Low            | This data has the value of action category |
      | Stanford Policy  | Action-Priority: | Low            | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | High           | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | Medium         | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | Low            | This data has the value of action category |
      | Cambridge Policy | Action-Class:    | Severe         | This data has the value of action category |
      | Cambridge Policy | Action-Class:    | Intermediate   | This data has the value of action category |
      | Cambridge Policy | Action-Class:    | Low            | This data has the value of action category |


    Scenario: Add subject assignment
    When the user sets to add the following subject assignment
      | subjectperimetername | subjectcategory      | subjectdata             | policyname       |
      | JohnLewis            | Affiliation:         | University-of-Stanford  | Stanford Policy  |
      | WilliamsJoeseph      | Affiliation:         | University-of-Stanford  | Stanford Policy  |
      | WilliamsJoeseph      | Affiliation:         | University-of-Cambridge | Cambridge Policy |
      | WilliamsJoeseph      | Authorization-Level: | Lecturer                | Cambridge Policy |
    Then the following subject assignment should be existed in the system
      | subjectperimetername | subjectcategory      | subjectdata             | policyname       |
      | JohnLewis            | Affiliation:         | University-of-Stanford  | Stanford Policy  |
      | WilliamsJoeseph      | Affiliation:         | University-of-Stanford  | Stanford Policy  |
      | WilliamsJoeseph      | Affiliation:         | University-of-Cambridge | Cambridge Policy |
      | WilliamsJoeseph      | Authorization-Level: | Lecturer                | Cambridge Policy |


  Scenario Outline: Add subject assignment validations
    When the user sets to add the following subject assignment
      | subjectperimetername   | subjectcategory   | subjectdata   | policyname   |
      | <subjectperimetername> | <subjectcategory> | <subjectdata> | <policyname> |

    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | subjectperimetername                                | subjectcategory                                     | subjectdata                                         | policyname                                          | flag  |
      |                                                     | Affiliation:                                        | University-of-Stanford                              | Stanford Policy                                     | False |
      | 000000000000000000000000000000000000000000000000000 | Affiliation:                                        | University-of-Stanford                              | Stanford Policy                                     | False |
      | GeorgeWilliams                                      | Affiliation:                                        | University-of-Cambridge                             | Cambridge Policy                                    | False |
      | WilliamsGeorge                                      | Authorization-Level:                                | Professor                                           | Cambridge Policy                                    | False |
      | JohnLewis                                           |                                                     | University-of-Stanford                              | Stanford Policy                                     | False |
      | JohnLewis                                           | 000000000000000000000000000000000000000000000000000 | University-of-Stanford                              | Stanford Policy                                     | False |
      | WilliamsJoeseph                                     | Authorization-Level:                                |                                                     | Cambridge Policy                                    | False |
      | WilliamsJoeseph                                     | Authorization-Level:                                | 000000000000000000000000000000000000000000000000000 | Cambridge Policy                                    | False |
      | WilliamsJoeseph                                     | Authorization-Level:                                | Admin                                               |                                                     | False |
      | WilliamsJoeseph                                     | Authorization-Level:                                | Admin                                               | 000000000000000000000000000000000000000000000000000 | False |

  Scenario Outline: Add an existing subject assignment
    Given the following subject assignment exists
      | subjectperimetername | subjectcategory      | subjectdata | policyname       |
      | WilliamsJoeseph      | Authorization-Level: | Lecturer    | Cambridge Policy |
    When the user sets to add the following subject assignment
      | subjectperimetername   | subjectcategory   | subjectdata   | policyname   |
      | <subjectperimetername> | <subjectcategory> | <subjectdata> | <policyname> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | subjectperimetername | subjectcategory      | subjectdata | policyname       | flag  |
      | WilliamsJoeseph      | Authorization-Level: | Lecturer    | Cambridge Policy | False |
      | WilliamsJoeseph      | Authorization-Level: | Professor   | Cambridge Policy | True  |

  Scenario: Delete subject assignments
    Given the following subject assignment exists
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
      | JohnLewis            | Affiliation:    | Stanford               | Stanford Policy |
    When the user sets to delete the following subject assignment
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
    Then the following subject assignment should be existed in the system
      | subjectperimetername | subjectcategory | subjectdata | policyname      |
      | JohnLewis            | Affiliation:    | Stanford    | Stanford Policy |


  Scenario: Add object assignments
    When the user sets to add the following object assignment
      | objectperimetername         | objectcategory | objectdata   | policyname       |
      | ProfessorsPromotionDocument | Clearance:     | Confidential | Stanford Policy  |
      | ProfessorsPromotionDocument | Clearance:     | Public       | Stanford Policy  |
      | StudentsGradesSheet         | Clearance:     | Top-Secret   | Stanford Policy  |
      | StudentsGradesSheet         | Clearance:     | Confidential | Stanford Policy  |
      | StudentsGradesSheet         | Clearance:     | Public       | Stanford Policy  |
      | StudentsGradesSheet         | Clearance:     | Confidential | Cambridge Policy |
      | StudentsGradesSheet         | Clearance:     | Public       | Cambridge Policy |
    Then the following object assignment should be existed in the system
      | objectperimetername         | objectcategory | objectdata                     | policyname       |
      | ProfessorsPromotionDocument | Clearance:     | Confidential,Public            | Stanford Policy  |
      | StudentsGradesSheet         | Clearance:     | Top-Secret,Confidential,Public | Stanford Policy  |
      | StudentsGradesSheet         | Clearance:     | Confidential,Public            | Cambridge Policy |


  Scenario Outline: Add object assignment validations
    When the user sets to add the following object assignment
      | objectperimetername   | objectcategory   | objectdata   | policyname   |
      | <objectperimetername> | <objectcategory> | <objectdata> | <policyname> |

    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | objectperimetername                                 | objectcategory                                      | objectdata                                          | policyname                                          | flag  |
      |                                                     | Clearance:                                          | Confidential                                        | Cambridge Policy                                    | False |
      | Vacations                                           | Clearance:                                          | Confidential                                        | Stanford Policy                                     | False |
      | 000000000000000000000000000000000000000000000000000 | Clearance:                                          | Confidential                                        | Stanford Policy                                     | False |
      | StudentsGradesSheet                                 |                                                     | Confidential                                        | Cambridge Policy                                    | False |
      | StudentsGradesSheet                                 | 000000000000000000000000000000000000000000000000000 | Confidential                                        | Cambridge Policy                                    | False |
      | StudentsGradesSheet                                 | Clearance:                                          |                                                     | Cambridge Policy                                    | False |
      | StudentsGradesSheet                                 | Clearance:                                          | 000000000000000000000000000000000000000000000000000 | Stanford Policy                                     | False |
      | StudentsGradesSheet                                 | Clearance:                                          | Confidential                                        |                                                     | False |
      | StudentsGradesSheet                                 | Clearance:                                          | Confidential                                        | 000000000000000000000000000000000000000000000000000 | False |

  Scenario Outline: Add an existing object assignment
    Given the following object assignment exists
      | objectperimetername | objectcategory | objectdata   | policyname      |
      | StudentsGradesSheet | Clearance:     | Confidential | Stanford Policy |
    When the user sets to add the following object assignment
      | objectperimetername   | objectcategory   | objectdata   | policyname   |
      | <objectperimetername> | <objectcategory> | <objectdata> | <policyname> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | objectperimetername | objectcategory | objectdata   | policyname      | flag  |
      | StudentsGradesSheet | Clearance:     | Confidential | Stanford Policy | False |

  Scenario: Delete object assignment
    Given the following object assignment exists
      | objectperimetername         | objectcategory | objectdata   | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Public       | Stanford Policy |
      | ProfessorsPromotionDocument | Clearance:     | Confidential | Stanford Policy |
    When the user sets to delete the following object assignment
      | objectperimetername         | objectcategory | objectdata   | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Confidential | Stanford Policy |
    Then the following object assignment should be existed in the system
      | objectperimetername         | objectcategory | objectdata | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Public     | Stanford Policy |

  Scenario: Add action assignment
    When the user sets to add the following action assignment
      | actionperimetername | actioncategory   | actiondata | policyname       |
      | Delete              | Action-Priority: | Medium     | Cambridge Policy |
      | Read                | Action-Class:    | Low        | Stanford Policy  |
    Then the following action assignment should be existed in the system
      | actionperimetername | actioncategory   | actiondata | policyname       |
      | Delete              | Action-Priority: | Medium     | Cambridge Policy |
      | Read                | Action-Class:    | Low        | Stanford Policy  |

  Scenario Outline: Add action assignment validations
    When the user sets to add the following action assignment
      | actionperimetername   | actioncategory   | actiondata   | policyname   |
      | <actionperimetername> | <actioncategory> | <actiondata> | <policyname> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | actionperimetername                                 | actioncategory                                      | actiondata                                          | policyname                                          | flag  |
      |                                                     | Action-Class:                                       | Severe                                              | Stanford Policy                                     | False |
      | Edit                                                | Action-Class:                                       | Severe                                              | Stanford Policy                                     | False |
      | 000000000000000000000000000000000000000000000000000 | Action-Class:                                       | Severe                                              | Stanford Policy                                     | False |
      | Read                                                |                                                     | Severe                                              | Stanford Policy                                     | False |
      | Read                                                | Action-Priority:                                    | Severe                                              | Stanford Policy                                     | False |
      | Read                                                | 000000000000000000000000000000000000000000000000000 | Severe                                              | Stanford Policy                                     | False |
      | Read                                                | Action-Class:                                       |                                                     | Stanford Policy                                     | False |
      | Read                                                | Action-Class:                                       | 000000000000000000000000000000000000000000000000000 | Stanford Policy                                     | False |
      | Read                                                | Action-Class:                                       | high                                                |                                                     | False |
      | Delete                                              | Action-Class:                                       | high                                                | 000000000000000000000000000000000000000000000000000 | False |
      | Delete                                              | Action-Class:                                       | high                                                | Stanford Policy                                     | False |

  Scenario Outline: Add an existing action assignment
    Given the following action assignment exists
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
    When the user sets to add the following action assignment
      | actionperimetername   | actioncategory   | actiondata   | policyname   |
      | <actionperimetername> | <actioncategory> | <actiondata> | <policyname> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | actionperimetername | actioncategory | actiondata | policyname      | flag  |
      | Read                | Action-Class:  | Severe     | Stanford Policy | False |

  Scenario: Delete action assignments
    Given the following action assignment exists
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
      | Read                | Action-Class:  | Low        | Stanford Policy |
    When the user sets to delete the following action assignment
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
    Then the following action assignment should be existed in the system
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Low        | Stanford Policy |