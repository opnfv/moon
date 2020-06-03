Feature: Authorization Wrapper

  Background:

    Given no slave is created
    And the slave is created
    And the system has no rules
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
      | universitymodel3 | Thisisabasicmodel | metarule9                     |
    And the following policy exists
      | policyname       | policydescription      | modelname        | genre     |
      | Stanford Policy  | This is a basic policy | universitymodel  | Education |
      | Cambridge Policy | This is a basic policy | universitymodel3 | Education |
    And the following pdp exists
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Stanford Policy   |
    And the following subject perimeter exists
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies         |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy  |
      | WilliamsJoeseph      | Thisistheexpecteduser       | wjoeseph@orange.com   | abc1234                  | Stanford Policy  |
      | WilliamsJoeseph      | Thisistheexpecteduser       | wjoeseph@orange.com   | abc1234                  | Cambridge Policy |
      #| WilliamsGeorge       | Thisdatahasthevalueofsubjectperimeter | gwilliams@orange.com  | abc1234                  |                  |
    And the following object perimeter exists
      | objectperimetername         | objectperimeterdescription   | policies         |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy  |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Stanford Policy  |
      | StudentsGradesSheet         | Thisistherequesttoaccessfile | Cambridge Policy |
      #| Vacations                   | Thisistherequesttoaccessfile |                  |
    And the following action perimeter exists
      | actionperimetername | actionperimeterdescription | policies         |
      | Read                | Thisistheactionrequired    | Stanford Policy  |
      | Delete              | Thisistheactionrequired    | Stanford Policy  |
      | Delete              | Thisistheactionrequired    | Cambridge Policy |
      #| Edit                | Thisistheactionrequired    |                 |
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
    And the following rule exists
      | rule                                       | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | grant        | Stanford Policy |
      #| University-of-Stanford,Professor,Public,Adminstrative,Low,Low | metarule9    | grant        | Stanford Policy |
    And the following authorization request is granted through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |

  Scenario: Check authorization response after rule deletion
    When the user sets to delete the following rules
      | rule                                       | metarulename | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after rule deletion then addition
    When the user sets to delete the following rules
      | rule                                       | metarulename | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | Stanford Policy |
    And the user sets to add the following rules
      | rule                                       | metarulename | instructions | policyname      |
      | University-of-Stanford,Confidential,Severe | metarule1    | grant        | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after subject assignment deletion
    When the user sets to delete the following subject assignment
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after subject assignment deletion then addition
    When the user sets to delete the following subject assignment
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
    And the user sets to add the following subject assignment
      | subjectperimetername | subjectcategory | subjectdata            | policyname      |
      | JohnLewis            | Affiliation:    | University-of-Stanford | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after object assignment deletion
    When the user sets to delete the following object assignment
      | objectperimetername | objectcategory | objectdata             | policyname      |
      | JohnLewis           | Affiliation:   | University-of-Stanford | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after object assignment deletion then addition
    When the user sets to delete the following object assignment
      | objectperimetername         | objectcategory | objectdata   | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Confidential | Stanford Policy |
    And the user sets to add the following object assignment
      | objectperimetername         | objectcategory | objectdata   | policyname      |
      | ProfessorsPromotionDocument | Clearance:     | Confidential | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after action assignment deletion
    When When the user sets to delete the following action assignment
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after action assignment deletion then addition
    When the user sets to delete the following action assignment
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Severe     | Stanford Policy |
    And the user sets to add the following action assignment
      | actionperimetername | actioncategory | actiondata | policyname      |
      | Read                | Action-Class:  | Low        | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |


  Scenario: Check authorization response after subject data deletion
    When the user sets to delete the following subject data
      | policyname      | subjectcategory | subjectdataname        |
      | Stanford Policy | Affiliation:    | University-of-Stanford |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after subject data deletion then addition
    When the user sets to delete the following subject data
      | policyname      | subjectcategory | subjectdataname        |
      | Stanford Policy | Affiliation:    | University-of-Stanford |
    And the user sets to add the following subject data
      | policyname      | subjectcategory | subjectdataname        | subjectdatadescription                      |
      | Stanford Policy | Affiliation:    | University-of-Stanford | This data has the value of subject category |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after object data deletion
    When the user sets to delete the following object data
      | policyname      | objectcategory | objectdataname |
      | Stanford Policy | Clearance:     | Top-Secret     |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after object data deletion then addition
    When the user sets to delete the following object data
      | policyname      | objectcategory | objectdataname |
      | Stanford Policy | Clearance:     | Top-Secret     |
    And the user sets to add the following object data
      | policyname      | objectcategory | objectdataname | objectdatadescription                      |
      | Stanford Policy | Clearance:     | Confidential   | This data has the value of object category |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after action data deletion
    When the user sets to delete the following action data
      | policyname      | actioncategory | actiondataname |
      | Stanford Policy | Action-Class:  | Severe         |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after action data deletion then addition
    When the user sets to delete the following action data
      | policyname      | actioncategory | actiondataname |
      | Stanford Policy | Action-Class:  | Severe         |
    And the user sets to add the following action data
      | policyname      | actioncategory | actiondataname | actiondatadescription                      |
      | Stanford Policy | Action-Class:  | Severe         | This data has the value of action category |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |


  Scenario: Check authorization response after subject perimeter deletion
    When the user sets to delete the following subject perimeter for a given policy
      | subjectperimetername | policies        |
      | JohnLewis            | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after subject perimeter deletion then addition
    When the user sets to delete the following subject perimeter for a given policy
      | subjectperimetername | policies        |
      | JohnLewis            | Stanford Policy |
    And the user sets to add the following subject perimeter
      | subjectperimetername | subjectperimeterdescription | subjectperimeteremail | subjectperimeterpassword | policies        |
      | JohnLewis            | Thisistheexpecteduser       | jlewis@orange.com     | abc1234                  | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after object perimeter deletion
    When the user sets to delete the following object perimeter
      | objectperimetername         | policies        |
      | ProfessorsPromotionDocument | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after object perimeter deletion then addition
    When the user sets to delete the following object perimeter
      | objectperimetername         | policies        |
      | ProfessorsPromotionDocument | Stanford Policy |
    And the user sets to add the following object perimeter
      | objectperimetername         | objectperimeterdescription   | policies        |
      | ProfessorsPromotionDocument | Thisistherequesttoaccessfile | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |

  Scenario: Check authorization response after action perimeter deletion
    When the user sets to delete the following action perimeter
      | actionperimetername | policies        |
      | Read                | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | denied        |

  Scenario: Check authorization response after action perimeter deletion then addition
    When the user sets to delete the following action perimeter
      | actionperimetername | policies        |
      | Read                | Stanford Policy |
    And the user sets to add the following action perimeter
      | actionperimetername | actionperimeterdescription | policies        |
      | Read                | Thisistheactionrequired    | Stanford Policy |
    And the following authorization request is sent through wrapper
      | keystone_project_id                                              | subjectperimetername | objectperimetername | actionperimetername |
      | 0000000000000000000000000000000000000000000000000000000000000000 | JohnLewis            | StudentsGradesSheet | Read                |
    Then the authorization response should be the following
      | auth_response |
      | grant         |
