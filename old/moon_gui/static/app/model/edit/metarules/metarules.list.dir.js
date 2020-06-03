(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonMetaRulesList', moonMetaRulesList);

    moonMetaRulesList.$inject = [];

    function moonMetaRulesList() {

        return {
            templateUrl : 'html/model/edit/metarules/metarules-list.tpl.html',
            bindToController : true,
            controller : moonMetaRulesListController,
            controllerAs : 'list',
            scope : {
                // if edit and delete possibilities are displayed
                // Value are True or False
                editMode : '=',
                mappedModel : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonMetaRulesListController', moonMetaRulesListController);

    moonMetaRulesListController.$inject = ['$scope', '$rootScope', 'NgTableParams', '$filter', '$modal', 'metaRuleService'];

    function moonMetaRulesListController($scope, $rootScope, NgTableParams, $filter, $modal, metaRuleService ){

        var list = this;

        list.table = {};

        list.editMode = $scope.list.editMode;
        list.model = $scope.list.mappedModel;
        list.metaRules = list.model.meta_rules_values;

        list.getMetaRules = getMetaRules;
        list.hasMetaRules = hasMetaRules;
        list.showDetail = showDetail;
        list.getSubjectList = getSubjectList;
        list.getObjectList = getObjectList;
        list.getActionlist = getActionlist;
        list.getShowDetailValue = getShowDetailValue;

        list.showDetailValue = false;

        list.subject_list = [];
        list.object_list = [];
        list.action_list = [];

        list.edit = { modal: $modal({ template: 'html/model/edit/metarules/action/metarules-edit.tpl.html', show: false }),
            showModal: showEditModal };

        /*list.edit.modal.result.finally(function(){
             console.log('CATCHING');
        });*/


        list.map = { modal: $modal({ template: 'html/model/edit/metarules/action/mapping/metarules-map.tpl.html', show: false }),
            showModal: showMapModal };

        list.unmap = { modal: $modal({ template: 'html/model/edit/metarules/action/mapping/metarules-unmap.tpl.html', show: false }),
            showModal: showUnmapModal };

        activate();

        function activate(){

            newMetaRulesTable();

        }

        /*
         * ---- events
         */
        var rootListeners = {

            'event:metaRuleMapToModelSuccess': $rootScope.$on('event:metaRuleMapToModelSuccess', updateModelFromMapSuccess),

            'event:metaRuleUnMappedToModelSuccess': $rootScope.$on('event:metaRuleUnMappedToModelSuccess', modelUnmappedSuccess),
            'event:metaRuleUnMappedToModelError': $rootScope.$on('event:metaRuleUnMappedToModelError', modelUnmappedError),
            

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }



        function newMetaRulesTable() {

            list.table = new NgTableParams({

                page: 1,            // show first page
                count: 10,          // count per page
                sorting: {
                    name: 'asc' // initial sorting
                }

            }, {

                total: function () { return list.getMetaRules().length; }, // length of data
                getData: function($defer, params) {

                    var orderedData = params.sorting() ? $filter('orderBy')(list.getMetaRules(), params.orderBy()) : list.getMetaRules();
                    $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));

                },
                $scope: { $data: {} }

            });

            return list.table;

        }

        /**
         * If the directive is not in editMode and displaying MetaData Content, if the editMode change to true, MetaData Content need to be hidden
         */
        $scope.$watch('list.editMode',  function(newValue, oldValue){
            list.showDetailValue = false;
        });

        function getMetaRules() {
            return (list.metaRules) ? list.metaRules : [];
        }

        function hasMetaRules() {
            return list.getMetaRules().length > 0;
        }

        function showDetail(aMetaRule){

            if(aMetaRule.id === getShowDetailValue().id){

                list.showDetailValue = false;
                list.subject_list = [];
                list.object_list = [];
                list.action_list = [];

            }else{

                list.subject_list = aMetaRule.subject_categories_values;
                list.object_list = aMetaRule.object_categories_values;
                list.action_list = aMetaRule.action_categories_values;
                list.showDetailValue = aMetaRule;

            }

        }

        function showEditModal(aMetaRule) {
            list.edit.modal.$scope.metaRule = aMetaRule;
            list.edit.modal.$promise.then(list.edit.modal.show);
        }

        function getShowDetailValue(){
            return list.showDetailValue;
        }

        function getSubjectList(){
            return list.subject_list;
        }

        function getObjectList(){
            return list.object_list;
        }

        function getActionlist(){
            return list.action_list;
        }

        /*
         * ---- add
         */
        function showMapModal() {
            list.map.modal.$scope.model = list.model;
            list.map.modal.$promise.then(list.map.modal.show);
        }

        function refreshRules(){

            list.metaRules = list.model.meta_rules_values;
            list.table.total(list.getMetaRules().length);
            list.table.reload();

        }

        function updateModelFromMapSuccess(event, model){

            list.model = model;

            refreshRules();

            list.map.modal.hide();

        }

        /*
         * ---- unmap
         */

        function showUnmapModal(metaRule) {

            list.unmap.modal.$scope.model = list.model;
            list.unmap.modal.$scope.metaRule = metaRule;
            list.unmap.modal.$promise.then(list.unmap.modal.show);

        }

        function modelUnmappedSuccess(event, model) {

            list.model = model;

            metaRuleService.findSomeWithCallback(list.model.meta_rules, function(meta_rules){

                list.model.meta_rules_values = meta_rules;
                refreshRules();
                list.unmap.modal.hide();

            });

        }

        function modelUnmappedError(event) {
            list.unmap.modal.hide();
        }

    }

})();
