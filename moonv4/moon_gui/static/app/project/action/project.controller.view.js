/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('ProjectViewController', ProjectViewController);
	
	ProjectViewController.$inject = ['$q', '$scope', '$translate', 'alertService', 'projectService'];
	
	function ProjectViewController($q, $scope, $translate, alertService, projectService) {
		
		var view = this;
		
		/*
		 * 
		 */
		
		view.project = $scope.project;
		
        // view.subjects = [];
        // view.subjectsLoading = true;
        // view.selectedSubject = null;
        // view.hasSubjects = hasSubjects;
        // view.hasSelectedSubject = hasSelectedSubject;
        //
        // view.objects = [];
        // view.objectsLoading = true;
        // view.hasObjects = hasObjects;
        //
        // view.roles = [];
        // view.groups = [];
        // view.roleAssignments = [];
        // view.groupAssignments = [];
        //
        // view.hasRoles = hasRoles;
        // view.hasGroups = hasGroups;
        //
        // view.isRoleAssigned = isRoleAssigned;
        // view.isGroupAssigned = isGroupAssigned;
        //
        // view.resolveRoles = resolveRoles;
        // view.resolveGroups = resolveGroups;
        //
        // //resolveObjects();
        // //resolveSubjects();
        //
        // /*
		 // * ---- objects
		 // */
        //
        // function resolveObjects() {
			//
			// projectService.data.object.query({project_uuid: view.project.id}).$promise.then(resolveSuccess, resolveError);
			//
			// function resolveSuccess(data) {
			//
			// 	view.objectsLoading = false;
	    	// 	view.objects = data.objects;
	    	//
			// }
			//
			// function resolveError(reason) {
			//
			// 	view.objectsLoading = false;
			//
			// 	$translate('moon.project.view.object.error').then(function (translatedValue) {
	    	// 		alertService.alertError(translatedValue);
	     //        });
			//
			// }
			//
        // }
        //
        // function hasObjects() {
			// return view.objects.length > 0;
        // }
        //
        // /*
		 // * ---- subjects
		 // */
        //
        // function resolveSubjects() {
			//
			// projectService.data.subject.query({project_uuid: view.project.uuid}).$promise.then(resolveSuccess, resolveError);
			//
			// function resolveSuccess(data) {
			//
			// 	view.subjectsLoading = false;
			// 	view.subjects = data.users;
		 //
			// }
			//
			// function resolveError(reason) {
			//
			// 	view.subjectsLoading = false;
			//
			// 	$translate('moon.project.view.subject.error').then(function (translatedValue) {
	    	// 		alertService.alertError(translatedValue);
	     //        });
			//
			// }
			//
        // }
        //
        // function hasSubjects() {
			// return view.subjects.lenght > 0;
        // }
        //
        // function hasSelectedSubject() {
			// return view.selectedSubject != null;
        // }
        //
        // /*
		 // * ---- role
		 // */
        //
        // function isRoleAssigned(role) {
        //
        // 	return _(view.roleAssignment.attributes).find(function(role_uuid) {
        // 		return role.uuid === role_uuid;
        // 	}).length !== 0;
        //
        // }
        //
        // function hasRoles() {
        // 	return view.roles.length > 0;
        // }
        //
        // function resolveRoles(subject) {
        //
        // 	view.rolesLoading = true;
        //
        // 	view.roles = [];
        // 	view.roleAssignment = null;
        //
        // 	var promises = { roles: projectService.data.subjectRole.get({project_uuid: view.project.uuid, user_uuid: subject.uuid}).$promise,
        // 					 roleAssigment: projectService.data.roleAssigment.get({project_uuid: view.project.uuid, user_uuid: subject.uuid}).$promise };
        //
        // 	$q.all(promises).then(resolveSuccess, resolveError);
        //
        // 	function resolveSuccess(data) {
        //
        // 		view.rolesLoading = false;
        // 		view.roles = data.roles.roles;
        // 		view.roleAssignment = _.first(data.roleAssigment.role_assignments);
        //
        // 	}
        //
        // 	function resolveError(reason) {
        //
        // 		view.rolesLoading = false;
    		//
    		// 	$translate('moon.project.view.role.error').then(function (translatedValue) {
        // 			alertService.alertError(translatedValue);
        //         });
        //
        // 	}
        //
        // }
        //
        // /*
        //  * ---- group
        //  */
        //
        // function isGroupAssigned(group) {
        //
        // 	return _($scope.view.groupAssignment.attributes).find(function(group_uuid) {
        // 		return group.uuid === group_uuid;
        // 	}).length !== 0;
        //
        // }
        //
        // function hasGroups() {
        // 	return view.groups.length > 0;
        // }
        //
        // function resolveGroups(subject) {
        //
        // 	view.groupsLoading = true;
        //
        // 	view.groups = [];
        // 	view.groupAssignment = null;
        //
        // 	var promises = { groups: projectService.data.subjectGroup.get({project_uuid: view.project.uuid, user_uuid: subject.uuid}).$promise,
        // 					 groupAssignment: projectService.data.groupAssigment.get({project_uuid: view.project.uuid, user_uuid: subject.uuid}).$promise };
        //
        // 	$q.all(promises).then(resolveSuccess, resolveError);
        //
        // 	function resolveSuccess(data) {
        //
        // 		view.groupsLoading = false;
        // 		view.groups = data.groups.groups;
        // 		view.groupAssignment = _.first(data.groupAssignment.group_assignments);
        //
        // 	}
        //
        // 	function resolveError(reason) {
        //
        // 		view.groupsLoading = false;
    		//
 		//     	$translate('moon.project.view.group.error').then(function (translatedValue) {
        // 			alertService.alertError(translatedValue);
        //         });
        //
        // 	}
        //
        // }
        //
	}
	
})();
