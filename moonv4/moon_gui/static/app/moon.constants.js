/**
# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.constant('DEFAULT_CST', {
				DOMAIN: {
					DEFAULT: 'Default'
				}
			})
			.constant('SECURITY_PIPELINE_CST', {
				TYPE: {
					POLICY: 'policy'
				}
			})
			.constant('META_DATA_CST', {
				TYPE: {
					SUBJECT: 'SUBJECT',
                    OBJECT: 'OBJECT',
                    ACTION: 'ACTION'
                }
			})
			.constant('PERIMETER_CST', {
				TYPE: {
					SUBJECT: 'SUBJECT',
					OBJECT: 'OBJECT',
					ACTION: 'ACTION'
				}
			})
			.constant('DATA_CST', {
				TYPE: {
					SUBJECT: 'SUBJECT',
					OBJECT: 'OBJECT',
					ACTION: 'ACTION'
				}
			})
			.constant('ASSIGNMENTS_CST', {
				TYPE: {
					SUBJECT: 'SUBJECT',
					OBJECT: 'OBJECT',
					ACTION: 'ACTION'
				}
			})
			.constant('REST_URI', {
                PDP : 'http://interface:8081/pdp/',
				MODELS : 'http://interface:8081/models/',
				METARULES:  'http://interface:8081/meta_rules/',
                RULES:  'http://interface:8081/rules/',
				POLICIES: 'http://interface:8081/policies/',
				METADATA: {
                	subject : 'http://interface:8081/subject_categories/',
					object : 'http://interface:8081/object_categories/',
                    action : 'http://interface:8081/action_categories/'
                },
				PERIMETERS :{
                    subject : 'http://interface:8081/subjects/',
                    object : 'http://interface:8081/objects/',
                    action : 'http://interface:8081/actions/'
				},
                KEYSTONE : 'http://keystone:5000/v3/'
			});
})();
