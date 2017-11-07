(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonRulesEdit', moonRulesEdit);

    moonRulesEdit.$inject = [];

    function moonRulesEdit() {

        return {
            templateUrl : 'html/policy/edit/parameter/rules/rules-edit.tpl.html',
            bindToController : true,
            controller : moonRulesEditController,
            controllerAs : 'edit',
            scope : {
                policy : '='
            },
            restrict : 'E',
            replace : true
        };

    }

    angular
        .module('moon')
        .controller('moonRulesEditController', moonRulesEditController);

    moonRulesEditController.$inject = ['$scope', 'rulesService', 'alertService', '$translate',
        'formService', 'policyService', 'utilService', 'metaRuleService', 'metaDataService', 'modelService', 'dataService', 'DATA_CST'];

    function moonRulesEditController($scope, rulesService, alertService, $translate,
                                    formService, policyService, utilService, metaRuleService, metaDataService, modelService, dataService, DATA_CST) {

        var edit = this;

        edit.policy = $scope.edit.policy;
        edit.editMode = true;

        edit.fromList = false;

        edit.loading = false;

        edit.form = {};
        edit.showDetailselectedMetaRules = false;

        edit.list = [];
        edit.policyList = [];

        edit.categories = {
            subject : [],
            loadingSubjects: true,
            object : [],
            loadingObjects: true,
            action : [],
            loadingActions : true
        };

        edit.data = {}; // this object is filled in declareDataObject():

        edit.create = createRules;
        edit.addDataToRules = addDataToRules;
        edit.removeSelectedDataFromRules = removeSelectedDataFromRules;
        edit.isNumberSelectedDataAtMaximum = isNumberSelectedDataAtMaximum;

        //this variable is related to checks on Instruction field which is in JSON
        edit.instructionsValid = true;
        edit.numberOfSelectedSubjectValid = true;
        edit.numberOfSelectedObjecttValid = true;
        edit.numberOfSelectedActionsValid = true;

        activate();

        /*
         *
         */
        function activate(){

            edit.rules = {meta_rule_id: null,  rule: [], policy_id: null, instructions: '[{"decision": "grant"}]', enabled: true};
            declareDataObject();
            loadAllPolicies();
            clearSelectedMetaRules();

        }

        function loadAllPolicies() {

            edit.policyList = [];

            policyService.findAllWithCallback( function(data) {

                _.each(data, function(element){

                    if(element.id === edit.policy.id){
                        edit.selectedPolicy = element;
                    }

                });

                edit.policyList = data;

            });
        }

        $scope.$watch('edit.selectedPolicy', function(newValue){

            clearSelectedMetaRules();

            if(!_.isUndefined(newValue)){

                loadRelatedMetaRules();

            }

        });

        $scope.$watch('edit.selectedMetaRules', function(newValue){

            clearSelectedData();

            edit.categories = {
                subject : [],
                loadingSubjects: true,
                object : [],
                loadingObjects: true,
                action : [],
                loadingActions : true
            };

           declareDataObject();

            if(!_.isUndefined(newValue)){

                loadRelatedCategoriesAndData(newValue.subject_categories, newValue.object_categories, newValue.action_categories);

            }

        });

        /**
         * To get the related MetaRules, it is required to :
         * - Get the model related to the policy
         * - Get the metaRules associated to the model
         * - Get the MetaData associated to the metaRules
         */
        function loadRelatedMetaRules() {

            edit.selectedPolicy.meta_rules_values = undefined;

            modelService.findOneWithCallback(edit.selectedPolicy.model_id, function(model){

                metaRuleService.findSomeWithCallback(model.meta_rules, function(metaRules){

                    edit.selectedPolicy.meta_rules_values = metaRules;

                });

            });

        }

        /**
         * Load categories from arrays of id in args
         * @param subjectsCategories, list of subject id related to the metaRule
         * @param objectCategories, list of object id related to the metaRule
         * @param actionsCategories, list of action id related to the metaRule
         */
        function loadRelatedCategoriesAndData(subjectsCategories, objectCategories, actionsCategories){

            metaDataService.subject.findSomeWithCallback(subjectsCategories, function(list){

                edit.categories.subject = list;
                edit.categories.loadingSubjects = false;

                _.each(edit.categories.subject, function(aSubject){

                    dataService.subject.findAllFromCategoriesWithCallback(edit.selectedPolicy.id, aSubject.id, function(subjects){

                        edit.data.subject = subjects;
                        edit.data.loadingSubjects = false;
                        edit.data.subjectsToBeSelected = angular.copy(edit.data.subject);

                    });

                });

            });

            metaDataService.object.findSomeWithCallback(objectCategories, function(list){

                edit.categories.object = list;
                edit.categories.loadingObjects = false;

                _.each(edit.categories.object, function(aObject){

                    dataService.object.findAllFromCategoriesWithCallback(edit.selectedPolicy.id, aObject.id, function(objects){

                        edit.data.object = objects;
                        edit.data.loadingObjects = false;
                        edit.data.objectsToBeSelected = angular.copy(edit.data.object);

                    });

                });

            });

            metaDataService.action.findSomeWithCallback(actionsCategories, function(list){

                edit.categories.action = list;
                edit.categories.loadingActions = false;

                _.each(edit.categories.action, function(aAction){

                    dataService.action.findAllFromCategoriesWithCallback(edit.selectedPolicy.id, aAction.id, function(actions){

                        edit.data.action = actions;
                        edit.data.loadingActions = false;
                        edit.data.actionsToBeSelected = angular.copy(edit.data.action);

                    });

                });

            });

        }

        /**
         * createRules, create Rules depending of what has been filled in the view
         */
        function createRules() {

            edit.instructionsValid = true;
            edit.numberOfSelectedSubjectValid = true;
            edit.numberOfSelectedObjecttValid = true;
            edit.numberOfSelectedActionsValid = true;

            manageInstructionContent();
            // bellow function is called here in order to display errors into the view
            manageNumberOfSelectedData();

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

                //manageNumberOfSelectedData is call again in order to check if errors have been display into the view
            }else if(edit.instructionsValid && manageNumberOfSelectedData()){

                startLoading();
                buildRulesArray();

                edit.rules.meta_rule_id = edit.selectedMetaRules.id;
                edit.rules.policy_id = edit.selectedPolicy.id;

                var rulesToSend = angular.copy(edit.rules);
                rulesToSend.instructions = JSON.parse(edit.rules.instructions);

                rulesService.add(rulesToSend, edit.policy.id, createSuccess, createError);
            }


            function createSuccess(data) {

                var created = utilService.transformOne(data, 'rules');

                $translate('moon.policy.rules.edit.action.add.create.success').then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                $scope.$emit('event:createRulesFromDataRulesSuccess', created);

                activate();

                stopLoading();

            }

            function createError(reason) {

                $translate('moon.policy.rules.edit.action.add.create.error').then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

            }

        }

        /**
         * if instructions attribute is not good then edit.instructionsValid is set to false
         * it will allow the view to display an error
         */
        function manageInstructionContent(){

            if (!isInstructionValid(edit.rules.instructions)){

                edit.instructionsValid = false;

            }else{

                edit.instructionsValid = true;

            }
        }

        /**
         * return true if the user has selected the number required of Selected Data (subject, object or action)
         * if one is missing then return false
         * it will also set numberOfSelected(Subject/Object/Action)Valid to true or false in order to display errors form in the view
         * @returns {boolean}
         */
        function manageNumberOfSelectedData(){

            isNumberSelectedDataAtMaximum(DATA_CST.TYPE.SUBJECT) ?
                edit.numberOfSelectedSubjectValid = true: edit.numberOfSelectedSubjectValid = false;
            isNumberSelectedDataAtMaximum(DATA_CST.TYPE.OBJECT) ?
                edit.numberOfSelectedObjecttValid = true: edit.numberOfSelectedObjecttValid = false;
            isNumberSelectedDataAtMaximum(DATA_CST.TYPE.ACTION) ?
                edit.numberOfSelectedActionsValid = true: edit.numberOfSelectedActionsValid = false;

            return edit.numberOfSelectedSubjectValid && edit.numberOfSelectedObjecttValid && edit.numberOfSelectedActionsValid;
        }

        /**
         * Check if the variables in param is not undefined and if it is a JSON
         * It is used for instructions attribute of a Rules object
         * @param str
         * @returns {boolean|*}
         */
        function isInstructionValid(str){

            return !_.isUndefined(str) && isJsonString(str);

        }

        function isJsonString(str) {

            var item = null;

            try {
                item = JSON.parse(str);
            } catch (e) {

                return false;
            }

            if (typeof item === 'object' && item !== null) {

                return true;
            }

            return false;
        }

        function startLoading(){

            edit.loading = true;

        }

        function stopLoading(){

            edit.loading = false;

        }

        /**
         * allow to clear selected values in the form
         */
        function clearSelectedMetaRules(){

            edit.selectedMetaRules = undefined;

            clearSelectedData();

        }

        function clearSelectedData(){

            edit.selectedSubject = undefined;
            edit.selectedObject = undefined;
            edit.selectedAction = undefined;

        }

        /**
         * check if the number of Selected Data is equal to the number of categories associated to the metaRule
         * @param typeCST : 'SUBJECT', 'OBJECT', 'ACTION'
         * @returns {boolean}
         */
        function isNumberSelectedDataAtMaximum(typeCST){

            if(!edit.selectedMetaRules){
                return false;
            }

            switch (typeCST) {

                case DATA_CST.TYPE.SUBJECT:

                    return edit.data.selectedSubjectsList.length === edit.selectedMetaRules.subject_categories.length;

                case DATA_CST.TYPE.OBJECT:

                    return  edit.data.selectedObjectsList.length === edit.selectedMetaRules.object_categories.length;

                case DATA_CST.TYPE.ACTION:

                  return edit.data.selectedActionsList.length === edit.selectedMetaRules.action_categories.length;
            }
        }

        /**
         * Add a data to an array of selected value (SUBJECT/OBJECT/ACTION)
         * those arrays will used in the create function in order to filled the rule attribute of a rules object
         * it will remove the selected value from the possible  value to be selected once the data is added
         * @param typeCST
         */
        function addDataToRules(typeCST){

            switch (typeCST) {
                case DATA_CST.TYPE.SUBJECT:

                    if (!edit.selectedSubject || isNumberSelectedDataAtMaximum(typeCST)
                        || _.contains(edit.data.selectedSubjectsList, edit.selectedSubject)) {
                        return;
                    }

                    edit.data.selectedSubjectsList.push(edit.selectedSubject);
                    edit.data.subjectsToBeSelected = _.without(edit.data.subjectsToBeSelected, edit.selectedSubject);

                    break;
                case DATA_CST.TYPE.OBJECT:

                    if (!edit.selectedObject || isNumberSelectedDataAtMaximum(typeCST)
                        || _.contains(edit.data.selectedObjectsList, edit.selectedObject)) {
                        return;
                    }

                    edit.data.selectedObjectsList.push(edit.selectedObject);
                    edit.data.objectsToBeSelected = _.without(edit.data.objectsToBeSelected, edit.selectedObject);

                    break;

                case DATA_CST.TYPE.ACTION:
                    if (!edit.selectedAction || isNumberSelectedDataAtMaximum(typeCST)
                        || _.contains(edit.data.selectedActionsList, edit.selectedAction)) {
                        return;
                    }

                    edit.data.selectedActionsList.push(edit.selectedAction);
                    edit.data.actionsToBeSelected = _.without(edit.data.actionsToBeSelected, edit.selectedAction);

                    break;
            }

        }

        /**
         * Remove a selected value,
         * refresh the list of possible value to be selected with the removed selected value
         * @param data
         * @param typeCST
         */
        function removeSelectedDataFromRules(data, typeCST) {

            switch (typeCST) {

                case DATA_CST.TYPE.SUBJECT:

                    edit.data.subjectsToBeSelected.push(data);
                    edit.data.selectedSubjectsList = _.without(edit.data.selectedSubjectsList, data);
                    break;

                case DATA_CST.TYPE.OBJECT:

                    edit.data.objectsToBeSelected.push(data);
                    edit.data.selectedObjectsList = _.without(edit.data.selectedObjectsList, data);
                    break;

                case DATA_CST.TYPE.ACTION:

                    edit.data.actionsToBeSelected.push(data);
                    edit.data.selectedActionsList = _.without(edit.data.selectedActionsList, data);
                    break;
            }

        }

        /**
         * fill edit.rules.rule array with the selected data
         * it will first add subject list, object list and then action list
         */
        function buildRulesArray(){

            _.each(edit.data.selectedSubjectsList, pushInRulesTab);
            _.each(edit.data.selectedObjectsList, pushInRulesTab);
            _.each(edit.data.selectedActionsList, pushInRulesTab);

            function pushInRulesTab(elem){
                edit.rules.rule.push(elem.id);
            }
        }

        /**
         * Declare the data object which contains attributes related to data,
         * values to be selected, values selected, loader...
         */
        function declareDataObject(){

            edit.data = {
                subject : [], // List of subjects related to the policy
                loadingSubjects: true, // allow to know if a call to the API is in progress
                subjectsToBeSelected : [], // List of subjects the user can select
                selectedSubjectsList: [], // List of subjects selected by the user from subjectsToBeSelected
                subjectCST : DATA_CST.TYPE.SUBJECT,
                object : [],
                loadingObjects: true,
                objectsToBeSelected: [],
                selectedObjectsList: [],
                objectCST : DATA_CST.TYPE.OBJECT,
                action : [],
                loadingActions : true,
                actionsToBeSelected : [],
                selectedActionsList: [],
                actionCST : DATA_CST.TYPE.ACTION
            }

        }

    }

})();