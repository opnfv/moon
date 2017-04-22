(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonRulesList', moonRulesList);

    moonRulesList.$inject = [];

    function moonRulesList() {

        return {
            templateUrl : 'html/policy/edit/parameter/rules/rules-list.tpl.html',
            bindToController : true,
            controller : moonRulesListController,
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
        .controller('moonRulesListController', moonRulesListController);

    moonRulesListController.$inject = [ 'NgTableParams', '$filter', 'metaRuleService', 'ruleService', 'dataService'];

    function moonRulesListController( NgTableParams, $filter, metaRuleService, ruleService, dataService) {

        var list = this;

        list.rules = [];

        list.loadingRules = true;

        list.table = {};

        list.getRules = getRules;
        list.hasRules = hasRules;
        list.refreshRules = refreshRules;

        list.getMetaRuleFromRule = getMetaRuleFromRule;
        list.getCategoryFromRuleIndex = getCategoryFromRuleIndex;

        list.isRuleIndexSubjectCategory = isRuleIndexSubjectCategory;
        list.isRuleIndexObjectCategory = isRuleIndexObjectCategory;
        list.isRuleIndexActionCategory = isRuleIndexActionCategory;

        activate();

        function activate(){


            newRulesTable();

            manageRules();
        }



        function manageRules(){

            ruleService.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('rules');
                console.log(data);

                list.rules = data;
                list.loadingRules = false;

                refreshRules();
            });
        }





        function newRulesTable() {

            list.table = new NgTableParams({

                page: 1,            // show first page
                count: 10,          // count per page
                sorting: {
                    name: 'asc' // initial sorting
                }

            }, {

                total: function () { return list.getRules().length; }, // length of data
                getData: function($defer, params) {

                    var orderedData = params.sorting() ? $filter('orderBy')(list.getRules(), params.orderBy()) : list.getRules();
                    $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));

                },
                $scope: { $data: {} }

            });

            return list.table;

        }

        function getMetaRuleFromRule(rule) {

            if(_.has(rule, 'meta_rule')){
                return rule.meta_rule;
            }

            // if the call has not been made
            if(!_.has(rule, 'callMetaRuleInProgress')){

                rule.callMetaRuleInProgress = true;

                metaRuleService.findOneWithCallback(rule.meta_rule_id, function(meta_rule){

                    rule.callMetaRuleInProgress = false;
                    rule.meta_rule = meta_rule;

                });

            }

            // if the call is in progress return false
            return false;
        }


        /**
         * Prerequisite : meta Rule  should be completely loaded
         * @param index
         * @param rule
         */
        function getCategoryFromRuleIndex(index, rule){

            if(!_.has(rule, 'rule_value')){
                // setting an array which will contains every value of the category
                rule.rule_value = Array.apply(null, new Array(rule.rule.length)).map(function(){
                    return {
                        category: {}
                    }
                });
            }

            if(_.has(rule.rule_value[index], 'callCategoryInProgress') && !rule.rule_value[index].callCategoryInProgress ){
                return rule.rule_value[index].category;
            }

            // if the call has not been made
            if(!_.has(rule.rule_value[index], 'callCategoryInProgress')){

                rule.rule_value[index].callCategoryInProgress = true;

                var categoryId = 0;

                if(list.isRuleIndexSubjectCategory(index, rule)){

                    categoryId = rule.meta_rule.subject_categories[index];

                    dataService.subject.data.findOne(list.policy.id, categoryId, rule.rule[index], function(category){

                        rule.rule_value[index].callCategoryInProgress = false;
                        rule.rule_value[index].category = category;

                    });

                }else if(list.isRuleIndexObjectCategory(index, rule)){


                    categoryId = rule.meta_rule.object_categories[index - rule.meta_rule.subject_categories.length ];

                    dataService.object.data.findOne(list.policy.id, categoryId, rule.rule[index], function(category){

                        rule.rule_value[index].callCategoryInProgress = false;
                        rule.rule_value[index].category = category;

                    });


                }else if(list.isRuleIndexActionCategory(index, rule)){

                    categoryId = rule.meta_rule.action_categories[index - rule.meta_rule.subject_categories.length - rule.meta_rule.object_categories.length ];

                    dataService.action.data.findOne(list.policy.id, categoryId, rule.rule[index], function(category){

                        rule.rule_value[index].callCategoryInProgress = false;
                        rule.rule_value[index].category = category;

                    });

                }else{

                    rule.rule_value[index].callCategoryInProgress = false;
                    rule.rule_value[index].category = {
                        name : 'ERROR'
                    }
                }

            }
            // if the call is in progress return false
            return false;
        }

        function isRuleIndexSubjectCategory(index, rule){

            var ind = index + 1;

            return ind <= rule.meta_rule.subject_categories.length;

        }

        function isRuleIndexObjectCategory(index, rule){

            var ind = index + 1;

            return  rule.meta_rule.subject_categories.length < ind && ind <=  ( rule.meta_rule.object_categories.length + rule.meta_rule.subject_categories.length );

        }

        function isRuleIndexActionCategory(index, rule){

            var ind = index + 1;

            return ( rule.meta_rule.object_categories.length + rule.meta_rule.subject_categories.length ) < ind && ind <= ( rule.meta_rule.object_categories.length + rule.meta_rule.subject_categories.length + rule.meta_rule.action_categories.length);

        }

        function getRules() {
            return (list.rules) ? list.rules : [];
        }

        function hasRules() {
            return list.getRules().length > 0;
        }


        /**
         * Refresh the table
         */
        function refreshRules(){
            list.table.total(list.rules.length);
            list.table.reload();
        }

    }

})();