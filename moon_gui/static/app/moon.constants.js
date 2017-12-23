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
                PDP : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/pdp/',
				MODELS : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/models/',
				METARULES:  'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/meta_rules/',
                RULES:  'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/rules/',
				POLICIES: 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/policies/',
				METADATA: {
                	subject : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/subject_categories/',
					object : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/object_categories/',
                    action : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/action_categories/'
                },
				PERIMETERS :{
                    subject : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/subjects/',
                    object : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/objects/',
                    action : 'http://{{MANAGER_HOST}}:{{MANAGER_PORT}}/actions/'
				},
                KEYSTONE : 'http://{{KEYSTONE_HOST}}:{{KEYSTONE_PORT}}/v3/'
			});
})();
