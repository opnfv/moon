Feature: PDP

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
    And the following meta data object category exists
      | objectmetadataname | objectmetadatadescription                                      |
      | Clearance:         | This meta data has the categorical information about an object |
      | Type:              | This meta data has the categorical information about an object |
    And the following meta data action category exists
      | actionmetadataname | actionmetadatadescription                                      |
      | Action-Class:      | This meta data has the categorical information about an action |
      | Action-Priority:   | This meta data has the categorical information about an action |
    And the following meta rule exists
      | metarulename | metaruledescription  | subjectmetadata                   | actionmetadata                 | objectmetadata   |
      | metarule1    | Thisisabasicmetarule | Affiliation:                      | Action-Class:                  | Clearance:       |
      | metarule2    | Thisisabasicmetarule | Authorization-Level:              | Action-Class:                  | Clearance:       |
      | metarule3    | Thisisabasicmetarule | Affiliation:                      | Action-Priority:               | Clearance:       |
      | metarule4    | Thisisabasicmetarule | Authorization-Level:              | Action-Priority:               | Clearance:       |
      | metarule5    | Thisisabasicmetarule | Affiliation:                      | Action-Class:                  | Type:            |
      | metarule6    | Thisisabasicmetarule | Authorization-Level:              | Action-Class:                  | Type:            |
      | metarule7    | Thisisabasicmetarule | Affiliation:                      | Action-Priority:               | Type:            |
      | metarule8    | Thisisabasicmetarule | Affiliation:,Authorization-Level: | Action-Class:,Action-Priority: | Clearance:,Type: |
    And the following model exists
      | modelname     | modeldescription  | metarule                      |
      | generalmodel  | Thisisabasicmodel | metarule1,metarule2,metarule6 |
      | generalmodel2 | Thisisabasicmodel | metarule3,metarule5,metarule8 |
    And the following policy exists
      | policyname | policydescription  | modelname     | genre     |
      | Policy A   | Thisisabasicpolicy | generalmodel  | financial |
      | Policy B   | Thisisabasicpolicy | generalmodel2 | financial |
      | Policy C   | Thisisabasicpolicy | generalmodel2 | financial |


  Scenario: Add PDP
    When the user sets to add the following pdp
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          |
      | B-pdp   | Thisisabasicpolicy | 1111111111111111111111111111111111111111111111111111111111111111 | Policy C          |

    Then the following pdp should be existed in the system
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          |
      | B-pdp   | Thisisabasicpolicy | 1111111111111111111111111111111111111111111111111111111111111111 | Policy C          |

  Scenario Outline: Add PDP validations
    When the user sets to add the following pdp
      | pdpname   | pdpdescription   | keystone_project_id   | security_pipeline   |
      | <pdpname> | <pdpdescription> | <keystone_project_id> | <security_pipeline> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | pdpname    | pdpdescription                                     | keystone_project_id                                              | security_pipeline | flag  |
      |            | This pdp is for creating a collection of policies  | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          | False |
      | generalpdp |                                                    | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          | True  |
      | 1 P        | This pdp is for creating a collection of policies  | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          | True  |
      | _%Pdp%_    | This pdp is for creating a collection of policies% | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          | True  |
      | generalpdp | This pdp is for creating a collection of policies% |                                                                  | Policy A          | False |
      | generalpdp | This pdp is for creating a collection of policies  | 0000000000000000000000000000000000000000000000000000000000000000 |                   | False |
      | generalpdp | This pdp is for creating a collection of policies  | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A,         | False |

  Scenario Outline: Add an existing PDP
    Given the following pdp exists
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy C          |
    When the user sets to add the following pdp
      | pdpname   | pdpdescription   | keystone_project_id   | security_pipeline   |
      | <pdpname> | <pdpdescription> | <keystone_project_id> | <security_pipeline> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline | flag  |
      | B-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy C          | False |
      | A-pdp   | Thisisabasicpolicy | 3333333333333333333333333333333333333333333333333333333333333333 | Policy A          | False |

  Scenario: Update PDP
    Given the following pdp exists
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          |
    When the user sets to update the following pdp
      | pdpname | updatedpdpname | updatedpdpdescription | updatedkeystone_project_id                                | updatedsecurity_pipeline |
      | A-pdp   | B-pdp          | Thisisabasicpolicy    | 111111111111111111111111111111111111111111111111111111111 | Policy B                 |
    Then the following pdp should be existed in the system
      | pdpname | pdpdescription     | keystone_project_id                                       | security_pipeline |
      | B-pdp   | Thisisabasicpolicy | 111111111111111111111111111111111111111111111111111111111 | Policy B          |

  Scenario Outline: Update PDP validations
    Given the following pdp exists
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy B          |
      | B-pdp   | Thisisabasicpolicy | 2222222222222222222222222222222222222222222222222222222222222222 | Policy C          |
    When the user sets to update the following pdp
      | pdpname   | updatedpdpname   | updatedpdpdescription   | updatedkeystone_project_id   | updatedsecurity_pipeline   |
      | <pdpname> | <updatedpdpname> | <updatedpdpdescription> | <updatedkeystone_project_id> | <updatedsecurity_pipeline> |
    Then the system should reply the following
      | flag   |
      | <flag> |
    Examples:
      | pdpname | updatedpdpname | updatedpdpdescription                      | updatedkeystone_project_id                                       | updatedsecurity_pipeline | flag  |
      | A-pdp   |                | Thispdpisforcreatingacollectionofpolicies  | 111111111111111111111111111111111111111111111111111111111        | Policy A                 | False |
      | A-pdp   | generalpdp     |                                            | 111111111111111111111111111111111111111111111111111111111        | Policy A                 | True  |
      | A-pdp   | 1 P            | Thispdpisforcreatingacollectionofpolicies  | 111111111111111111111111111111111111111111111111111111111        | Policy A                 | True  |
      | A-pdp   | _%Pdp%_        | Thispdpisforcreatingacollectionofpolicies% | 111111111111111111111111111111111111111111111111111111111        | Policy A                 | True  |
      | A-pdp   | generalpdp     | Thispdpisforcreatingacollectionofpolicies% |                                                                  | Policy A                 | False |
      | A-pdp   | generalpdp     | Thispdpisforcreatingacollectionofpolicies  | 111111111111111111111111111111111111111111111111111111111        |                          | False |
      | A-pdp   | generalpdp     | Thispdpisforcreatingacollectionofpolicies  | 111111111111111111111111111111111111111111111111111111111        | Policy A,                | False |
      | A-pdp   | A-pdp          | Thisisabasicpolicy                         | 0000000000000000000000000000000000000000000000000000000000000000 | Policy B                 | True  |
      | A-pdp   | B-pdp          | Thisisabasicpolicy                         | 111111111111111111111111111111111111111111111111111111111        | Policy C                 | False |

  Scenario: Delete PDP
    Given the following pdp exists
      | pdpname | pdpdescription     | keystone_project_id                                              | security_pipeline |
      | A-pdp   | Thisisabasicpolicy | 0000000000000000000000000000000000000000000000000000000000000000 | Policy A          |
    When the user sets to delete the following pdp
      | pdpname |
      | A-pdp   |
    Then the following pdp should be existed in the system
      | pdpname | pdpdescription | keystone_project_id | security_pipeline |
      |         |                |                     |                   |
