Feature: Policy

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
      | metarule8    | This is a basic metarule | Authorization-Level:              | Action-Priority:               | Type:            |
      | metarule9    | This is a basic metarule | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: | Clearance:,Type: |
    And the following model exists
      | modelname     | modeldescription      | metarule                      |
      | generalmodel  | This is a basic model | metarule9                     |
      | generalmodel2 | This is a basic model | metarule3,metarule5,metarule8 |
      | generalmodel3 | This is a basic model | metarule9                     |

  Scenario: Add policy
    When the user sets to add the following policy
      | policyname | policydescription      | modelname    | genre          |
      | A policy   | This is a basic policy | generalmodel | financial      |
      | B policy   | This is a basic policy | generalmodel | administrative |
    Then the following policy should be existed in the system
      | policyname | policydescription      | modelname    | genre          |
      | A policy   | This is a basic policy | generalmodel | financial      |
      | B policy   | This is a basic policy | generalmodel | administrative |

 Scenario Outline: Add policy validations
    When the user sets to add the following policy
      | policyname   | policydescription   | modelname   | genre   |
      | <policyname> | <policydescription> | <modelname> | <genre> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname    | policydescription        | modelname                                                            | genre      | flag  |
      |               | This is a basic policy   | generalmodel                                                         | financial  | False |
      | generalpolicy |                          | generalmodel                                                         | financial  | True  |
      | generalpolicy | This is a basic policy   |                                                                      | financial  | False |
      | generalpolicy | This is a basic policy   | 0000000000000000000000                                               | financial  | False |
      | generalpolicy | This is a basic policy   | 0000000000000000000000000000000000000000000000000000000000000000     | financial  | False |
      | generalpolicy | This is a basic policy   | 00000000000000000000000000000000000000000000000000000000000000000000 | financial  | False |
      | generalpolicy | This is a basic policy   | generalmodel                                                         |            | True  |
      | 1             | This is a basic policy   | generalmodel                                                         | financial  | True  |
      | _%policy%_    | This is a basic policy   | generalmodel                                                         | financial  | True  |
      | policy        | This is a basic policy % | generalmodel                                                         | 1          | True  |
      | policy        | This is a basic policy % | generalmodel2                                                        | 1          | True  |
      | policy        | This is a basic policy % | generalmodel                                                         | _%genere%_ | True  |

  Scenario Outline: Add an existing policy
    Given the following policy exists
      | policyname    | policydescription      | modelname    | genre     |
      | generalpolicy | This is a basic policy | generalmodel | financial |
    When the user sets to add the following policy
      | policyname   | policydescription   | modelname   | genre   |
      | <policyname> | <policydescription> | <modelname> | <genre> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname     | policydescription      | modelname     | genre     | flag  |
      | generalpolicy  | This is a basic policy | generalmodel2 | financial | False |
      | generalpolicy2 | This is a basic policy | generalmodel  | financial | True  |

  Scenario: Update policy
    Given the following policy exists
      | policyname    | policydescription      | modelname    | genre     |
      | generalpolicy | This is a basic policy | generalmodel | financial |
    When the user sets to update the following policy
      | policyname    | updatedpolicyname | updatedpolicydescription | updatedmodelname | updatedgenre |
      | generalpolicy | 1 P %             | This is a basic policy   | generalmodel     | financial    |
    Then the following policy should be existed in the system
      | policyname | policydescription      | modelname    | genre     |
      | 1 P %      | This is a basic policy | generalmodel | financial |

  Scenario Outline: Update policy validations
    Given the following policy exists
      | policyname  | policydescription      | modelname    | genre         |
      | mainpolicy  | This is a basic policy | generalmodel | adminstrative |
      | mainpolicy2 | This is a basic policy | generalmodel | adminstrative |
    When the user sets to update the following policy
      | policyname   | updatedpolicyname   | updatedpolicydescription   | updatedmodelname   | updatedgenre   |
      | <policyname> | <updatedpolicyname> | <updatedpolicydescription> | <updatedmodelname> | <updatedgenre> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | policyname | updatedpolicyname | updatedpolicydescription | updatedmodelname                                                     | updatedgenre  | flag  |
      | mainpolicy |                   | This is a basic policy   | generalmodel                                                         | financial     | False |
      | mainpolicy | generalpolicy     |                          | generalmodel                                                         | financial     | True  |
      | mainpolicy | generalpolicy     | This is a basic policy   |                                                                      | financial     | False |
      | mainpolicy | generalpolicy     | This is a basic policy   | 0000000000000000000000                                               | financial     | False |
      | mainpolicy | generalpolicy     | This is a basic policy   | 0000000000000000000000000000000000000000000000000000000000000000     | financial     | False |
      | mainpolicy | generalpolicy     | This is a basic policy   | 00000000000000000000000000000000000000000000000000000000000000000000 | financial     | False |
      | mainpolicy | generalpolicy     | This is a basic policy   | generalmodel                                                         |               | True  |
      | mainpolicy | 1                 | This is a basic policy   | generalmodel                                                         | financial     | True  |
      | mainpolicy | _%policy%_        | This is a basic policy   | generalmodel                                                         | financial     | True  |
      | mainpolicy | policy            | This is a basic policy % | generalmodel                                                         | financial     | True  |
      | mainpolicy | policy            | This is a basic policy % | generalmodel                                                         | 1             | True  |
      | mainpolicy | policy            | This is a basic policy % | generalmodel2                                                        | 1             | False |
      | mainpolicy | policy            | This is a basic policy % | generalmodel                                                         | _%genere%_    | True  |
      | mainpolicy | mainpolicy        | This is a basic policy % | generalmodel                                                         | adminstrative | True  |
      | mainpolicy | mainpolicy2       | This is a basic policy % | generalmodel                                                         | adminstrative | False |

  Scenario: Delete policy
    Given the following policy exists
      | policyname    | policydescription      | modelname    | genre     |
      | generalpolicy | This is a basic policy | generalmodel | financial |
    When the user sets to delete the following policy
      | policyname    |
      | generalpolicy |
    Then the following policy should be existed in the system
      | policyname | policydescription | modelname | genre |
      |            |                   |           |       |


   Scenario: Delete a policy that has a system attributes dependency
    Given the following policy exists
      | policyname       | policydescription      | modelname     | genre     |
      | Stanford Policy  | This is a basic policy | generalmodel  | financial |
      | Cambridge Policy | This is a basic policy | generalmodel2 | Education |
    And the following pdp exists
      | pdpname    | pdpdescription      | keystone_project_id                                              | security_pipeline |
      | generalpdp | This is a basic pdp | 0000000000000000000000000000000000000000000000000000000000000000 | Stanford Policy   |
    And the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy  |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Cambridge Policy |
      | WilliamsJoeseph      | Thisistheexpecteduser       | wjoeseph@orange.com   | abc1234                  | Stanford Policy  |
    And the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Cambridge Policy |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Stanford Policy  |
    And the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies         |
      | Delete              | Thisistheactionrequired    | Stanford Policy  |
      | Read                | Thisistheactionrequired    | Stanford Policy  |
      | Read                | Thisistheactionrequired    | Cambridge Policy |
    And the following subject data exists
      | policyname      | subjectcategory      | subjectdataname        | subjectdatadescription                      |
      | Stanford Policy | Affiliation:         | University-of-Stanford | This data has the value of subject category |
      | Stanford Policy | Affiliation:         | Stanford               | This data has the value of subject category |
      | Stanford Policy | Authorization-Level: | Professor              | This data has the value of subject category |
    And the following object data exists
      | policyname      | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford Policy | Clearance:     | Top-Secret     | This data has the value of object category |
      | Stanford Policy | Clearance:     | Confidential   | This data has the value of object category |
      | Stanford Policy | Clearance:     | Public         | This data has the value of object category |
      | Stanford Policy | Type:          | Adminstrative  | This data has the value of object category |
      | Stanford Policy | Type:          | Staff          | This data has the value of object category |
    And the following action data exists
      | policyname      | actioncategory   | actiondataname | actiondatadescription                      |
      | Stanford Policy | Action-Class:    | Severe         | This data has the value of action category |
      | Stanford Policy | Action-Class:    | Low            | This data has the value of action category |
      | Stanford Policy | Action-Priority: | Low            | This data has the value of action category |
    And the following subject assignment exists
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
      | WilliamsJoeseph      | Affiliation:    | Stanford               | Stanford Policy |
    And the following object assignment exists
      | objectperimetername | objectcategory | objectdata   | policyname      |
      | StudentsGradesSheet | Clearance:     | Public       | Stanford Policy |
      | StudentsGradesSheet | Clearance:     | Top-Secret   | Stanford Policy |
      | StudentsGradesSheet | Clearance:     | Confidential | Stanford Policy |
    And the following action assignment exists
      | actionperimetername | actioncategory   | actiondata | policyname      |
      | Read                | Action-Class:    | Severe     | Stanford Policy |
      | Read                | Action-Class:    | Low        | Stanford Policy |
      | Read                | Action-Priority: | Low        | Stanford Policy |
    When the user sets to delete the following policy
      | policyname      |
      | Stanford Policy |
    Then the following policy should be existed in the system
      | policyname       | policydescription      | modelname     | genre     |
      | Cambridge Policy | This is a basic policy | generalmodel2 | Education |
    And the following pdp should be existed in the system
      | pdpname    | pdpdescription      | keystone_project_id                                              | security_pipeline |
      | generalpdp | This is a basic pdp | 0000000000000000000000000000000000000000000000000000000000000000 |                   |
    And the following subject perimeter should be existed in the system
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Cambridge Policy |
      | WilliamsJoeseph      | Thisistheexpecteduser       | wjoeseph@orange.com   | abc1234                  |   |
    And the following object perimeter should be existed in the system
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Cambridge Policy |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile |   |
    And the following action perimeter should be existed in the system
      | actionperimetername | actionperimeterdescription | policies         |
      | Delete                | Thisistheactionrequired    |  |
      | Read                | Thisistheactionrequired    | Cambridge Policy |
    And the following subject data should be existed in the system
      | policyname | subjectcategory | subjectdataname | subjectdatadescription |
      |            |                 |                 |                        |
    And the following object data should be existed in the system
      | policyname | objectcategory | objectdataname | objectdatadescription |
      |            |                |                |                       |
    And the following action data should be existed in the system
      | policyname | actioncategory | actiondataname | actiondatadescription |
      |            |                |                |                       |
    And the following subject assignment should be existed in the system
      | subjectperimetername | subjectcategory | subjectdata | policyname |
      |                      |                 |             |            |
    And the following object assignment should be existed in the system
      | objectperimetername | objectcategory | objectdata | policyname |
      |                     |                |            |            |
    And the following action assignment should be existed in the system
      | actionperimetername | actioncategory | actiondata | policyname |
      |                     |                |            |            |

