(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonMetaDataList', moonMetaDataList);

    moonMetaDataList.$inject = [];

    function moonMetaDataList() {

        return {
            templateUrl : 'html/model/edit/metadata/metadata-list.tpl.html',
            bindToController : true,
            controller : moonMetaDataListController,
            controllerAs : 'list',
            scope : {
                metaRule: '=',
                editMode: '=',
                // shortDisplay : boolean value
                //shortDisplay: '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonMetaDataListController', moonMetaDataListController);

    moonMetaDataListController.$inject = ['$scope', '$rootScope', 'metaDataService', '$translate', 'alertService', 'metaRuleService', 'META_DATA_CST', 'utilService'];

    function moonMetaDataListController($scope, $rootScope, metaDataService, $translate, alertService, metaRuleService, META_DATA_CST, utilService){

        var list = this;

        list.metaRule = $scope.list.metaRule;
        list.editMode = $scope.list.editMode;
        list.shortDisplay = $scope.list.shortDisplay;

        list.typeOfSubject = META_DATA_CST.TYPE.SUBJECT;
        list.typeOfObject = META_DATA_CST.TYPE.OBJECT;
        list.typeOfAction = META_DATA_CST.TYPE.ACTION;

        list.unMapSub = unMapSub;
        list.unMapObj = unMapObj;
        list.unMapAct = unMapAct;

        // list.deleteSub = deleteSub;
        // list.deleteObj = deleteObj;
        // list.deleteAct = deleteAct;

        list.getSubjectCategories = getSubjectCategories;
        list.getObjectCategories = getObjectCategories;
        list.getActionCategories = getActionCategories;

        activate();

        function activate(){

            manageSubjectCategories();

            manageObjectCategories();

            manageActionCategories();

        }

        var rootListeners = {

            'event:updateMetaRuleFromMetaDataAddSuccess': $rootScope.$on('event:updateMetaRuleFromMetaDataAddSuccess', updateMetaRuleCategories),

            'event:deleteMetaDataFromMetaDataAddSuccess': $rootScope.$on('event:deleteMetaDataFromMetaDataAddSuccess', deleteMetaRuleCategories)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }

        function manageSubjectCategories(){

            list.loadingCatSub = true;

           metaDataService.subject.findSomeWithCallback(list.metaRule.subject_categories, function(categories){

                list.catSub = categories;
                list.loadingCatSub = false;

            });
        }

        function manageObjectCategories(){

            list.loadingCatObj = true;

            metaDataService.object.findSomeWithCallback(list.metaRule.object_categories, function(categories){

                list.catObj = categories;
                list.loadingCatObj = false;

            });

        }

        function manageActionCategories(){

            list.loadingCatAct = true;

            metaDataService.action.findSomeWithCallback(list.metaRule.action_categories, function(categories){

                list.catAct = categories;
                list.loadingCatAct = false;

            });

        }


        /**
         * UnMap
         */

        function unMapSub(subject){

            subject.loader = true;

            var metaRuleToSend = angular.copy(list.metaRule);

            metaRuleToSend.subject_categories = _.without(metaRuleToSend.subject_categories, subject.id);

            metaRuleService.update(metaRuleToSend, updateMetaRuleSuccess, updateMetaRuleError);

            function updateMetaRuleSuccess(data){

                $translate('moon.model.metarules.update.success', { metaRuleName: list.metaRule.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                metaRuleToSend = metaRuleService.findMetaDataFromMetaRule(utilService.transformOne(data, 'meta_rules'));
                angular.copy(metaRuleToSend, list.metaRule);

                activate();

                subject.loader = false;

            }

            function updateMetaRuleError(reason){

                $translate('moon.model.metarules.update.error', { metaRuleName: list.metaRule.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                subject.loader = false;

            }

        }

        function unMapObj(object){

            object.loader = true;

            var metaRuleToSend = angular.copy(list.metaRule);

            metaRuleToSend.object_categories = _.without(metaRuleToSend.object_categories, object.id);

            metaRuleService.update(metaRuleToSend, updateMetaRuleSuccess, updateMetaRuleError);

            function updateMetaRuleSuccess(data){

                $translate('moon.model.metarules.update.success', { metaRuleName: list.metaRule.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                metaRuleToSend = metaRuleService.findMetaDataFromMetaRule(utilService.transformOne(data, 'meta_rules'));
                angular.copy(metaRuleToSend, list.metaRule);

                activate();

                object.loader = false;

            }

            function updateMetaRuleError(reason){

                $translate('moon.model.metarules.update.error', { metaRuleName: list.metaRule.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                object.loader = false;

            }

        }

        function unMapAct(action){

            action.loader = true;

            var metaRuleToSend = angular.copy(list.metaRule);

            metaRuleToSend.action_categories = _.without(metaRuleToSend.action_categories, action.id);

            metaRuleService.update(metaRuleToSend, updateMetaRuleSuccess, updateMetaRuleError);

            function updateMetaRuleSuccess(data){

                $translate('moon.model.metarules.update.success', { metaRuleName: list.metaRule.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                metaRuleToSend = metaRuleService.findMetaDataFromMetaRule(utilService.transformOne(data, 'meta_rules'));
                angular.copy(metaRuleToSend, list.metaRule);

                activate();

                action.loader = false;

            }

            function updateMetaRuleError(reason){

                $translate('moon.model.metarules.update.error', { metaRuleName: list.metaRule.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                action.loader = false;

            }

        }

        // /**
        //  * Delete
        //  */
        //
        // function deleteSub(subject){
        //
        //     subject.loader = true;
        //
        //     metaDataService.subject.delete(subject, deleteSubSuccess, deleteSubError);
        //
        //     function deleteSubSuccess(data){
        //
        //         $translate('moon.model.metadata.subject.delete.success', { subjectName: subject.name }).then( function(translatedValue) {
        //             alertService.alertSuccess(translatedValue);
        //         });
        //
        //         removeSubFromSubList(subject);
        //
        //         subject.loader = false;
        //
        //     }
        //
        //     function deleteSubError(reason){
        //
        //         $translate('moon.model.metadata.subject.delete.error',
        // { subjectName: subject.name, reason: reason.message}).then( function(translatedValue) {
        //             alertService.alertError(translatedValue);
        //         });
        //
        //         subject.loader = false;
        //
        //     }
        // }
        //
        // function deleteObj(object){
        //
        //     object.loader = true;
        //
        //     metaDataService.object.delete(object, deleteObjSuccess, deleteObjError);
        //
        //     function deleteObjSuccess(data){
        //
        //         $translate('moon.model.metadata.object.delete.success', { objectName: object.name }).then( function(translatedValue) {
        //             alertService.alertSuccess(translatedValue);
        //         });
        //
        //         removeObjFromObjList(object);
        //         /*list.catSub = metaDataService.subject.findSome(list.metaRule.subject_categories);
        //         list.catObj = metaDataService.object.findSome(list.metaRule.object_categories);
        //         list.catAct = metaDataService.action.findSome(list.metaRule.action_categories);*/
        //
        //         object.loader = false;
        //
        //     }
        //
        //     function deleteObjError(reason){
        //
        //         $translate('moon.model.metadata.object.delete.error', { objectName: object.name, reason: reason.message}).then( function(translatedValue) {
        //             alertService.alertError(translatedValue);
        //         });
        //
        //         object.loader = false;
        //     }
        // }
        //
        // function deleteAct(action){
        //
        //     action.loader = true;
        //
        //     metaDataService.action.delete(action, deleteActSuccess, deleteActError);
        //
        //     function deleteActSuccess(data){
        //
        //         $translate('moon.model.metadata.action.delete.success', { actionName: action.name }).then( function(translatedValue) {
        //             alertService.alertSuccess(translatedValue);
        //         });
        //
        //         removeActFromActList(action);
        //
        //         action.loader = false;
        //
        //     }
        //
        //     function deleteActError(reason){
        //
        //         $translate('moon.model.metadata.action.delete.error', { actionName: action.name, reason: reason.message}).then( function(translatedValue) {
        //             alertService.alertError(translatedValue);
        //         });
        //
        //         action.loader = false;
        //
        //     }
        // }

        function getSubjectCategories(){
            return list.catSub ? list.catSub : [];
        }

        function getObjectCategories(){
            return list.catObj ? list.catObj : [];
        }

        function getActionCategories(){
            return list.catAct ? list.catAct : [];
        }

        // function removeSubFromSubList(subject){
        //     list.catSub = _.without(list.catSub, subject);
        // }
        //
        // function removeObjFromObjList(object){
        //     list.catObj = _.without(list.catObj, object);
        // }
        //
        // function removeActFromActList(action){
        //     list.catAct = _.without(list.catAct, action);
        // }

        function updateMetaRuleCategories( event, metaRule){

            list.metaRule = metaRule;

            activate();

        }


        function deleteMetaRuleCategories( event, metaRule){

            list.metaRule = metaRule;

            activate();

        }

    }

})();