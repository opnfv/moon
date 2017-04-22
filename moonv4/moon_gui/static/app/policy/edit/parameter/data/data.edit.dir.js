(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonDataEdit', moonDataEdit);

    moonDataEdit.$inject = [];

    function moonDataEdit() {

        return {
            templateUrl : 'html/policy/edit/parameter/data/data-edit.tpl.html',
            bindToController : true,
            controller : moonDataEditController,
            controllerAs : 'edit',
            scope : {
                //Type can be 'ACTION', 'OBJECT', 'SUBJECT'
                metaDataType: '=',
                metaRule : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonDataEditController', moonDataEditController);

    moonDataEditController.$inject = ['$scope', 'metaDataService', 'DATA_CST', 'alertService', '$translate', 'formService', 'policyService', 'utilService'];

    function moonDataEditController($scope, metaDataService, DATA_CST, alertService, $translate, formService, policyService, utilService) {

        var edit = this;

        edit.metaDataType = $scope.edit.metaDataType;
        edit.metaRule = $scope.edit.metaRule;

        edit.fromList = true;

        edit.laoading = false;

        edit.form = {};

        edit.metaData = { name: null, description: null};

        edit.list = [];

        edit.create = createMetaData;
        edit.addToMetaRule = addToMetaRule;
        edit.deleteMetaData = deleteMetaData;

        activate();

        /*
         *
         */

        function activate(){

            switch(edit.metaDataType){

                case DATA_CST.TYPE.SUBJECT:

                    metaDataService.subject.findAllWithCallback(callBackList);
                    break;

                case DATA_CST.TYPE.OBJECT:

                    metaDataService.object.findAllWithCallback(callBackList);
                    break;

                case DATA_CST.TYPE.ACTION:

                    metaDataService.action.findAllWithCallback(callBackList);
                    break;

                default :

                    edit.list = [];
                    break;

            }

            function callBackList(list){

                edit.list = list

            }

        }

        /**
         * Add
         */

        function addToMetaRule(){

            if(!edit.selectedMetaData){

                return;

            }

            var metaRuleToSend = edit.metaRule;

            switch(edit.metaDataType){

                case DATA_CST.TYPE.SUBJECT:

                    metaRuleToSend.subject_categories.push(edit.selectedMetaData.id);
                    break;

                case DATA_CST.TYPE.OBJECT:

                    metaRuleToSend.object_categories.push(edit.selectedMetaData.id);
                    break;

                case DATA_CST.TYPE.ACTION:

                    metaRuleToSend.action_categories.push(edit.selectedMetaData.id);
                    break;
            }

            policyService.update(metaRuleToSend, updateMetaRuleSuccess, updateMetaRuleError);

            function updateMetaRuleSuccess(data){

                $translate('moon.model.metarules.update.success', { metaRuleName: metaRuleToSend.name }).then( function(translatedValue) {

                    alertService.alertSuccess(translatedValue);

                });

                metaRuleToSend = utilService.transformOne(data, 'meta_rules');

                $scope.$emit('event:updateMetaRuleFromMetaDataAddSuccess', metaRuleToSend);

                stopLoading();

            }

            function updateMetaRuleError(reason){

                $translate('moon.model.metarules.update.error', { metaRuleName: metaRuleToSend.name, reason: reason.message}).then( function(translatedValue) {

                    alertService.alertError(translatedValue);

                });

                stopLoading();

            }

        }

        /**
         * Create
         */

        function createMetaData() {

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            } else {

                startLoading();

                var metaDataToSend = angular.copy(edit.metaData);

                switch(edit.metaDataType){

                    case DATA_CST.TYPE.SUBJECT:

                        metaDataService.subject.add(metaDataToSend, createSuccess, createError);
                        break;

                    case DATA_CST.TYPE.OBJECT:

                        metaDataService.object.add(metaDataToSend, createSuccess, createError);
                        break;

                    case DATA_CST.TYPE.ACTION:

                        metaDataService.action.add(metaDataToSend, createSuccess, createError);
                        break;
                }

            }

            function createSuccess(data) {

                var created = {};

                switch(edit.metaDataType){

                    case DATA_CST.TYPE.SUBJECT:

                        created = utilService.transformOne(data, 'subject_categories');
                        break;

                    case DATA_CST.TYPE.OBJECT:

                        created = utilService.transformOne(data, 'object_categories');
                        break;

                    case DATA_CST.TYPE.ACTION:

                        created = utilService.transformOne(data, 'action_categories');
                        break;
                }

                $translate('moon.model.metadata.edit.create.success', { name: created.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                stopLoading();

                edit.list.push(created);

                displayList();

            }

            function createError(reason) {

                $translate('moon.model.metadata.edit.create.error', { name: metaDataToSend.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

            }

        }

        function deleteMetaData(){

            if(!edit.selectedMetaData){

                return;

            }

            startLoading();

            var metaDataToDelete = angular.copy(edit.selectedMetaData);

            switch(edit.metaDataType){
                case DATA_CST.TYPE.SUBJECT:

                    metaDataService.subject.delete(metaDataToDelete, deleteSuccess, deleteError);
                    break;

                case DATA_CST.TYPE.OBJECT:

                    metaDataService.object.delete(metaDataToDelete, deleteSuccess, deleteError);
                    break;

                case DATA_CST.TYPE.ACTION:

                    metaDataService.action.delete(metaDataToDelete, deleteSuccess, deleteError);
                    break;
            }


            function deleteSuccess(data) {

                $translate('moon.model.metadata.edit.delete.success', { name: metaDataToDelete.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                policyService.findOneWithMetaData(edit.metaRule.id).then( function(metaRule){

                    edit.metaRule = metaRule;

                    cleanSelectedValue();

                    activate();

                    stopLoading();

                    $scope.$emit('event:deleteMetaDataFromMetaDataAddSuccess', edit.metaRule);

                });

            }

            function deleteError(reason) {

                $translate('moon.model.metadata.edit.delete.error', { name: metaDataToDelete.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

            }
        }

        function cleanSelectedValue(){

            delete edit.selectedMetaData;

        }

        function startLoading(){

            edit.loading = true;

        }

        function stopLoading(){

            edit.loading = false;

        }

        function displayList(){

            edit.fromList = true;

        }

    }

})();