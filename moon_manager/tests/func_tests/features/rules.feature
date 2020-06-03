Feature: Rules

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
      | subjectperimetername | subjectperimeterdescription           | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser                 | jlewis@orange.com     | abc1234                  | Stanford Policy |
      | WilliamsJoeseph      | Thisistheexpecteduser                 | wjoeseph@orange.com   | abc1234                  | Stanford Policy |
      | WilliamsJoeseph      | Thisistheexpecteduser                 | wjoeseph@orange.com   | abc1234                  | Cambridge Policy |
      | WilliamsGeorge       | Thisdatahasthevalueofsubjectperimeter | gwilliams@orange.com  | abc1234                  |                 |
    And the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Stanford Policy  |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Cambridge Policy |
      | Vacations                   | Thisistherequesttoaccessfile |                  |
    And the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
      | Delete              | Thisistheactionrequired    | Stanford Policy |
      | Edit                | Thisistheactionrequired    |                 |
     And the following subject data exists
      | policyname       | subjectcategory      | subjectdataname         | subjectdatadescription                      |
      | Stanford Policy  | Affiliation:         | University-of-Stanford  | This data has the value of subject category |
      | Stanford Policy  | Affiliation:         | Stanford                | This data has the value of subject category |
      | Cambridge Policy | Affiliation:         | University-of-Cambridge | This data has the value of subject category |
      | Cambridge Policy | Authorization-Level: | Professor               | This data has the value of subject category |
      | Cambridge Policy | Authorization-Level: | Lecturer                | This data has the value of subject category |
    And the following object data exists
      | policyname       | objectcategory | objectdataname         | objectdatadescription                      |
      | Stanford Policy  | Clearance:     | Top-Secret             | This data has the value of object category |
      | Stanford Policy  | Clearance:     | Confidential           | This data has the value of object category |
      | Stanford Policy  | Clearance:     | Public                 | This data has the value of object category |
      | Cambridge Policy | Type:          | Adminstrative          | This data has the value of object category |
      | Cambridge Policy | Type:          | Teaching-Staff         | This data has the value of object category |
      | Cambridge Policy | Clearance:     | Confidential           | This data has the value of object category |
      | Cambridge Policy | Clearance:     | Access-with-permission | This data has the value of object category |
      | Cambridge Policy | Clearance:     | Public                 | This data has the value of object category |

    And the following action data exists
      | policyname       | actioncategory   | actiondataname | actiondatadescription                      |
      | Stanford Policy  | Action-Class:    | Severe         | This data has the value of action category |
      | Stanford Policy  | Action-Class:    | Low            | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | High           | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | Medium         | This data has the value of action category |
      | Cambridge Policy | Action-Priority: | Low            | This data has the value of action category |
      | Cambridge Policy | Action-Class:    | Severe         | This data has the value of action category |
      | Cambridge Policy | Action-Class:    | Intermediate   | This data has the value of action category |
      | Cambridge Policy | Action-Class:    | Low            | This data has the value of action category |

    And the following subject assignment exists
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
      | WilliamsJoeseph      | Affiliation:    | Stanford               | Stanford Policy |

    And the following object assignment exists
      | objectperimetername | objectcategory | objectdata             | policyname       |
      | StudentsGradesSheet | Clearance:     | Access-with-permission | Cambridge Policy |
      | StudentsGradesSheet | Clearance:     | Public                 | Cambridge Policy |
      #| StudentsGradesSheet | Clearance:     | Top-Secret             | Stanford Policy  |
      | StudentsGradesSheet | Clearance:     | Confidential           | Stanford Policy  |
      #| StudentsGradesSheet | Clearance:     | Public                 | Stanford Policy  |
    And the following action assignment exists
      | actionperimetername | actioncategory   | actiondata | policyname       |
      | Read                | Action-Class:    | Severe     | Stanford Policy  |
      #| Read                | Action-Class:    | Low        | Stanford Policy  |
      | Delete              | Action-Priority: | High       | Cambridge Policy |
      | Delete              | Action-Priority: | Medium     | Cambridge Policy |
      | Delete              | Action-Priority: | Low        | Cambridge Policy |

  Scenario: Add rule
    When the user sets to add the following rules
      | rule                                                          | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe                    | metarule1    | grant        | Stanford Policy |
      | University-of-Cambridge,Professor,Public,Adminstrative,Low,Low | metarule9    | grant        | Cambridge Policy |
    Then the following rules should be existed in the system
      | rule                                                          | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe                    | metarule1    | grant        | Stanford Policy |
      | University-of-Cambridge,Professor,Public,Adminstrative,Low,Low | metarule9    | grant        | Cambridge Policy |

Scenario Outline: Add rules validations
    When the user sets to add the following rules
      | rule   | metarulename   | instructions   | policyname   |
      | <rule> | <metarulename> | <instructions> | <policyname> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | rule                                                                         | metarulename                                        | instructions | policyname                                          | flag  |
      |                                                                              | metarule1                                           | grant        | Stanford Policy                                     | False |
      | Confidential,Severe                                                          | metarule1                                           | grant        | Stanford Policy                                     | False |
      | ,Confidential,Severe                                                         | metarule1                                           | grant        | Stanford Policy                                     | False |
      | 0000000000000000000000000000000000000000,Confidential,Severe                 | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University of USA,Confidential,Severe                                        | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,,Confidential,Severe                                  | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,,Confidential                                         | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Superficial,Severe                                    | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,0000000000000000000000000000000000000000,Severe       | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,,Severe                                  | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,                                         | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,Non-Accessable                           | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,0000000000000000000000000000000000000000 | metarule1                                           | grant        | Stanford Policy                                     | False |
      #| University-of-Stanford,Confidential,Severe,                                  | metarule1                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,Severe                                   |                                                     | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,Severe                                   | metarule9                                           | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,Severe                                   | 000000000000000000000000000000000000000000000000000 | grant        | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,Severe                                   | metarule1                                           | not grant    | Stanford Policy                                     | False |
      | University-of-Stanford,Confidential,Severe                                   | metarule1                                           |              | Stanford Policy                                     | True |
      | University-of-Stanford,Confidential,Severe                                   | metarule1                                           | grant        |                                                     | False |
      | University-of-Stanford,Confidential,Severe                                   | metarule1                                           | grant        | 000000000000000000000000000000000000000000000000000 | False |
      | University-of-Stanford,Confidential,Severe                                   | metarule1                                           | grant        | Cambridge Policy                                    | False |


  Scenario: Add existing rule
    Given the following rule exists
      | rule                                       | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | grant        | Stanford Policy |
    When the user sets to add the following rules
      | rule                                       | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | grant        | Stanford Policy |
    Then the system should reply the following
      | flag  |
      | False |


  Scenario: Delete rule
    Given the following rule exists
      | rule                                       | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | grant        | Stanford Policy |
    When the user sets to delete the following rules
      | rule                                       | metarulename | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | Stanford Policy |
    Then the system should reply the following
      | flag |
      | True |


