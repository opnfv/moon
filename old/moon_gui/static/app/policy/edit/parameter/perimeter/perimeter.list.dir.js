(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonPerimeterList', moonPerimeterList);

    moonPerimeterList.$inject = [];

    function moonPerimeterList() {

        return {
            templateUrl : 'html/policy/edit/parameter/perimeter/perimeter-list.tpl.html',
            bindToController : true,
            controller : moonPerimeterListController,
            controllerAs : 'list',
            scope : {
                policy: '=',
                editMode : '='
            },
            restrict : 'E',
            replace : true
        };

    }

    angular
        .module('moon')
        .controller('moonPerimeterListController', moonPerimeterListController);

    moonPerimeterListController.$inject = ['$scope', '$rootScope', 'perimeterService', '$translate', 'alertService', 'PERIMETER_CST'];

    function moonPerimeterListController($scope, $rootScope, perimeterService, $translate, alertService, PERIMETER_CST){

        var list = this;

        list.policy = $scope.list.policy;
        list.editMode = $scope.list.editMode;

        list.typeOfSubject = PERIMETER_CST.TYPE.SUBJECT;
        list.typeOfObject = PERIMETER_CST.TYPE.OBJECT;
        list.typeOfAction = PERIMETER_CST.TYPE.ACTION;

        list.unMapSub = unMapSub;
        list.unMapObj = unMapObj;
        list.unMapAct = unMapAct;

        list.getSubjects = getSubjects;
        list.getObjects = getObjects;
        list.getActions = getActions;

        activate();

        function activate(){

            manageSubjects();

            manageObjects();

            manageActions();

        }

        var rootListeners = {

            'event:deletePerimeterFromPerimeterAddSuccess': $rootScope.$on('event:deletePerimeterFromPerimeterAddSuccess', deletePolicy),
            'event:createAssignmentsFromAssignmentsEditSuccess': $rootScope.$on('event:createAssignmentsFromAssignmentsEditSuccess', addAssignmentsToPolicy)

        };

        _.each(rootListeners, function(unbind){
            $scope.$on('$destroy', rootListeners[unbind]);
        });


        function manageSubjects(){

            list.loadingSub = true;

            perimeterService.subject.findAllFromPolicyWithCallback(list.policy.id, function(perimeters){

                list.subjects = perimeters;
                list.loadingSub = false;

            });
        }

        function manageObjects(){

            list.loadingObj = true;

            perimeterService.object.findAllFromPolicyWithCallback(list.policy.id, function(perimeters){

                list.objects = perimeters;
                list.loadingObj = false;

            });

        }

        function manageActions(){

            list.loadingAct = true;

            perimeterService.action.findAllFromPolicyWithCallback(list.policy.id, function(perimeters){

                list.actions = perimeters;
                list.loadingAct = false;

            });

        }

        /**
         * UnMap
         */

        function unMapSub(perimeter){

            perimeter.policy_list = _.without(perimeter.policy_list, list.policy.id);

            perimeter.loader = true;

            var perimeterToSend = angular.copy(perimeter);

            perimeterService.subject.unMapPerimeterFromPolicy(list.policy.id , perimeter.id, updatePerimeterSuccess, updatePerimeterError);

            function updatePerimeterSuccess(data){

                $translate('moon.policy.perimeter.update.success', { perimeterName: perimeterToSend.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                $scope.$emit('event:unMapPerimeterFromPerimeterList', perimeter, PERIMETER_CST.TYPE.SUBJECT);

                activate();

                perimeter.loader = false;
            }

            function updatePerimeterError(reason){

                $translate('moon.policy.perimeter.update.error', { perimeterName: perimeter.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                perimeter.loader = false;

            }

        }

        function unMapObj(perimeter){

            perimeter.policy_list = _.without(perimeter.policy_list, list.policy.id);

            perimeter.loader = true;

            var perimeterToSend = angular.copy(perimeter);

            perimeterService.object.unMapPerimeterFromPolicy(list.policy.id , perimeter.id, updatePerimeterSuccess, updatePerimeterError);

            function updatePerimeterSuccess(data){

                $translate('moon.policy.perimeter.update.success', { perimeterName: perimeterToSend.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                $scope.$emit('event:unMapPerimeterFromPerimeterList', perimeter, PERIMETER_CST.TYPE.OBJECT);

                activate();

                perimeter.loader = false;
            }

            function updatePerimeterError(reason){

                $translate('moon.policy.perimeter.update.error', { perimeterName: perimeter.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                perimeter.loader = false;

            }

        }

        function unMapAct(perimeter){

            perimeter.policy_list = _.without(perimeter.policy_list, list.policy.id);

            perimeter.loader = true;

            var perimeterToSend = angular.copy(perimeter);

            perimeterService.action.unMapPerimeterFromPolicy(list.policy.id , perimeter.id, updatePerimeterSuccess, updatePerimeterError);

            function updatePerimeterSuccess(data){

                $translate('moon.policy.perimeter.update.success', { perimeterName: perimeterToSend.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                $scope.$emit('event:unMapPerimeterFromPerimeterList', perimeter, PERIMETER_CST.TYPE.ACTION);

                activate();

                perimeter.loader = false;
            }

            function updatePerimeterError(reason){

                $translate('moon.policy.perimeter.update.error', { perimeterName: perimeter.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                perimeter.loader = false;

            }

        }

        function getSubjects(){
            return list.subjects ? list.subjects : [];
        }

        function getObjects(){
            return list.objects ? list.objects : [];
        }

        function getActions(){
            return list.actions ? list.actions : [];
        }

        function removeSubFromSubList(subject){
            list.subjects = _.without(list.subjects, subject);
        }

        function removeObjFromObjList(object){
            list.objects = _.without(list.objects, object);
        }

        function removeActFromActList(action){
            list.actions = _.without(list.actions, action);
        }

        function deletePolicy( event, policy){

            list.policy = policy;

            activate();

        }

        function addAssignmentsToPolicy( event, assignments, type){

            switch (type) {

                case PERIMETER_CST.TYPE.SUBJECT:

                    list.subjects.push(assignments);
                    break;

                case PERIMETER_CST.TYPE.OBJECT:

                    list.objects.push(assignments);
                    break;

                case PERIMETER_CST.TYPE.ACTION:

                    list.actions.push(assignments);
                    break;

                default :
                    break;

            }

        }

    }

})();