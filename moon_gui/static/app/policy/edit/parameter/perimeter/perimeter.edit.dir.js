(function () {

    'use strict';

    angular
        .module('moon')
        .directive('moonPerimeterEdit', moonPerimeterEdit);

    moonPerimeterEdit.$inject = [];

    function moonPerimeterEdit() {

        return {
            templateUrl: 'html/policy/edit/parameter/perimeter/perimeter-edit.tpl.html',
            bindToController: true,
            controller: moonPerimeterEditController,
            controllerAs: 'edit',
            scope: {
                //Type can be 'ACTION', 'OBJECT', 'SUBJECT'
                perimeterType: '=',
                policy: '='
            },
            restrict: 'E',
            replace: true
        };
    }


    angular
        .module('moon')
        .controller('moonPerimeterEditController', moonPerimeterEditController);

    moonPerimeterEditController.$inject = ['$scope', '$rootScope',
        'perimeterService', 'PERIMETER_CST', 'alertService',
        '$translate', 'formService', 'policyService', 'utilService'];

    function moonPerimeterEditController($scope, $rootScope,
                                         perimeterService, PERIMETER_CST, alertService,
                                         $translate, formService, policyService, utilService) {

        var edit = this;

        edit.perimeterType = $scope.edit.perimeterType;
        // This variable is used in the view in order to display or not display email field
        edit.subjectType = PERIMETER_CST.TYPE.SUBJECT;
        edit.policy = $scope.edit.policy;

        edit.fromList = true;

        edit.loading = false;

        edit.form = {};

        edit.perimeter = {name: null, description: null, partner_id: null, policy_list: [], email: null};

        edit.list = [];
        edit.policyList = [];
        edit.policiesToBeSelected = [];
        edit.selectedPolicyList = []; // List of Policies to be added to a new perimeter

        edit.create = createPerimeter;
        edit.addToPolicy = addToPolicy;
        edit.addPolicyToPerimeter = addPolicyToPerimeter;
        edit.clearSelectedPolicies = clearSelectedPolicies;
        edit.removeSelectedPolicy = removeSelectedPolicy;
        edit.deletePerimeter = deletePerimeter;

        activate();

        /*
         *
         */

        function activate() {

            loadAllPolicies();

            switch (edit.perimeterType) {

                case PERIMETER_CST.TYPE.SUBJECT:

                    perimeterService.subject.findAllWithCallback(callBackList);
                    break;

                case PERIMETER_CST.TYPE.OBJECT:

                    perimeterService.object.findAllWithCallback(callBackList);
                    break;

                case PERIMETER_CST.TYPE.ACTION:

                    perimeterService.action.findAllWithCallback(callBackList);
                    break;

                default :

                    edit.list = [];
                    break;

            }

            function callBackList(list) {

                // For each Perimeter, there is a check about the mapping between the perimeter and the policy
                _.each(list, function (element) {

                    if (_.indexOf(element.policy_list, edit.policy.id) === -1) {

                        edit.list.push(element);

                    }

                });

            }

        }

        var rootListeners = {

            'event:unMapPerimeterFromPerimeterList': $rootScope.$on('event:unMapPerimeterFromPerimeterList', manageUnMappedPerimeter)

        };

        _.each(rootListeners, function(unbind){
            $scope.$on('$destroy', rootListeners[unbind]);
        });


        function loadAllPolicies() {

            edit.policyList = [];

            policyService.findAllWithCallback( function(data) {

                edit.policyList = data;
                edit.policiesToBeSelected = angular.copy(edit.policyList);

            });
        }

        function addPolicyToPerimeter() {

            if (!edit.selectedPolicy || _.contains(edit.perimeter.policy_list, edit.selectedPolicy.id)) {
                return;
            }

            edit.perimeter.policy_list.push(edit.selectedPolicy.id);
            edit.selectedPolicyList.push(edit.selectedPolicy);
            edit.policiesToBeSelected = _.without(edit.policiesToBeSelected, edit.selectedPolicy);

        }

        function clearSelectedPolicies() {

            edit.perimeter.policy_list = [];
            edit.selectedPolicyList = [];
            edit.policiesToBeSelected = angular.copy(edit.policyList);

        }

        function removeSelectedPolicy(policy) {

            edit.policiesToBeSelected.push(policy);
            edit.perimeter.policy_list = _.without(edit.perimeter.policy_list, policy.id);
            edit.selectedPolicyList = _.without(edit.selectedPolicyList, policy);

        }

        /**
         * Add
         */

        function addToPolicy() {

            if (!edit.selectedPerimeter) {

                return;

            }

            startLoading();

            var  perimeterToSend = edit.selectedPerimeter;

            perimeterToSend.policy_list.push(edit.policy.id);

            switch (edit.perimeterType) {

                case PERIMETER_CST.TYPE.SUBJECT:

                    perimeterService.subject.update(perimeterToSend, updatePerimeterSuccess, updatePerimeterError);
                    break;

                case PERIMETER_CST.TYPE.OBJECT:

                    perimeterService.object.update(perimeterToSend, updatePerimeterSuccess, updatePerimeterError);
                    break;

                case PERIMETER_CST.TYPE.ACTION:

                    perimeterService.action.update(perimeterToSend, updatePerimeterSuccess, updatePerimeterError);
                    break;
            }


            function updatePerimeterSuccess(data) {

                $translate('moon.perimeter.update.success', {policyName: perimeterToSend.name}).then(function (translatedValue) {

                    alertService.alertSuccess(translatedValue);

                });

                stopLoading();

            }

            function updatePerimeterError(reason) {

                $translate('moon.policy.update.error', {
                    policyName: perimeterToSend.name,
                    reason: reason.message
                }).then(function (translatedValue) {

                    alertService.alertError(translatedValue);

                });

                stopLoading();

            }

        }

        /**
         * Create
         */

        function createPerimeter() {

            if (formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            } else {

                startLoading();

                var perimeterToSend = angular.copy(edit.perimeter);

                switch (edit.perimeterType) {

                    case PERIMETER_CST.TYPE.SUBJECT:

                        perimeterService.subject.add(perimeterToSend, createSuccess, createError);
                        break;

                    case PERIMETER_CST.TYPE.OBJECT:

                        perimeterService.object.add(perimeterToSend, createSuccess, createError);
                        break;

                    case PERIMETER_CST.TYPE.ACTION:

                        perimeterService.action.add(perimeterToSend, createSuccess, createError);
                        break;
                }

            }

            function createSuccess(data) {

                var created = {};

                switch (edit.perimeterType) {

                    case PERIMETER_CST.TYPE.SUBJECT:

                        created = utilService.transformOne(data, 'subjects');
                        break;

                    case PERIMETER_CST.TYPE.OBJECT:

                        created = utilService.transformOne(data, 'objects');
                        break;

                    case PERIMETER_CST.TYPE.ACTION:

                        created = utilService.transformOne(data, 'actions');
                        break;
                }

                $translate('moon.policy.perimeter.edit.create.success', {name: created.name}).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                stopLoading();

                /**
                 * If during the creating the created assignments has be mapped with the current policy, then it is not required to push the new Assignments in the list
                 */
                if (_.indexOf(created.policy_list, edit.policy.id) === -1) {

                    edit.list.push(created);

                }else{

                    $scope.$emit('event:createAssignmentsFromAssignmentsEditSuccess', created, edit.perimeterType);

                }

                displayList();

                clearSelectedPolicies();

            }

            function createError(reason) {

                $translate('moon.policy.perimeter.edit.create.error', {name: perimeterToSend.name}).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

            }

        }

        /**
         * Delete
         */
        function deletePerimeter() {

            if (!edit.selectedPerimeter) {

                return;

            }

            startLoading();

            var perimeterToDelete = angular.copy(edit.selectedPerimeter);

            switch (edit.perimeterType) {
                case PERIMETER_CST.TYPE.SUBJECT:

                    perimeterService.subject.delete(perimeterToDelete, deleteSuccess, deleteError);
                    break;

                case PERIMETER_CST.TYPE.OBJECT:

                    perimeterService.object.delete(perimeterToDelete, deleteSuccess, deleteError);
                    break;

                case PERIMETER_CST.TYPE.ACTION:

                    perimeterService.action.delete(perimeterToDelete, deleteSuccess, deleteError);
                    break;
            }


            function deleteSuccess(data) {

                $translate('moon.policy.perimeter.edit.delete.success', {name: perimeterToDelete.name})
                    .then(function (translatedValue) {
                        alertService.alertSuccess(translatedValue);
                    });

                policyService.findOneReturningPromise(edit.policy.id).then(function (data) {

                    edit.policy = utilService.transformOne(data, 'policies');

                    cleanSelectedValue();
                    activate();
                    stopLoading();

                    $scope.$emit('event:deletePerimeterFromPerimeterAddSuccess', edit.policy);

                });

            }

            function deleteError(reason) {

                $translate('moon.policy.perimeter.edit.delete.error', {name: perimeterToDelete.name}).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

            }
        }

        function cleanSelectedValue() {
            edit.list = _.without(edit.list, edit.selectedPerimeter);
            delete edit.selectedPerimeter;

        }

        function startLoading() {

            edit.loading = true;

        }

        function stopLoading() {

            edit.loading = false;

        }

        function displayList() {

            edit.fromList = true;

        }

        /**
         * If A perimeter has been unMapped, maybe it has to be display into the available list of Perimeter
         * @param perimeter
         * @param type
         */
        function manageUnMappedPerimeter(event, perimeter, type){

            if(type === edit.perimeterType && _.indexOf(perimeter.policy_list, edit.policy.id) === -1){

                edit.list.push(perimeter);

            }

        }

    }

})();