(function() {

    'use strict';

    angular
        .module('moon')
        .controller('ModelListController', ModelListController);

    ModelListController.$inject = ['$scope', '$rootScope', 'models', 'NgTableParams', '$filter', '$modal'];

    function ModelListController($scope, $rootScope, models, NgTableParams, $filter, $modal) {

        var list = this;

        list.models = models;

        list.table = {};

        list.search = { query: '',
            find: searchModel,
            reset: searchReset };

        list.getModels = getModels;
        list.hasModels = hasModels;
        list.deleteModel = deleteModel;
        list.refreshModels = refreshModels;

        list.add = { modal: $modal({ template: 'html/model/action/model-add.tpl.html', show: false }),
            showModal: showAddModal };

        list.view = { modal: $modal({ template: 'html/model/action/model-view.tpl.html', show: false }),
            showModal: showViewModal };

        list.del = { modal: $modal({ template: 'html/model/action/model-delete.tpl.html', show: false }),
            showModal: showDeleteModal };

        activate();

        function activate(){
            newModelsTable();
        }


        /*
         * ---- events
         */
        var rootListeners = {

            'event:modelCreatedSuccess': $rootScope.$on('event:modelCreatedSuccess', modelCreatedSuccess),
            'event:modelCreatedError': $rootScope.$on('event:modelCreatedError', modelCreatedError),

            'event:modelDeletedSuccess': $rootScope.$on('event:modelDeletedSuccess', modelDeletedSuccess),
            'event:modelDeletedError': $rootScope.$on('event:modelDeletedError', modelDeletedError)


        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }


        function newModelsTable() {

            list.table = new NgTableParams({

                page: 1,            // show first page
                count: 10,          // count per page
                sorting: {
                    name: 'asc' // initial sorting
                }

            }, {

                total: function () { return list.getModels().length; }, // length of data
                getData: function($defer, params) {

                    var orderedData = params.sorting() ? $filter('orderBy')(list.getModels(), params.orderBy()) : list.getModels();
                    $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));

                },
                $scope: { $data: {} }

            });

            return list.table;

        }

        function getModels() {
            return (list.models) ? list.models : [];
        }

        function hasModels() {
            return list.getModels().length > 0;
        }

        /**
         * Blank the search field
         */
        function searchReset() {
            list.search.query = '';
        }

        /*
         * ---- search
         */

        function searchModel(model){
            return (model.name.indexOf(list.search.query) !== -1 || model.description.indexOf(list.search.query) !== -1);
        }

        /*
         * ---- add
         */
        function showAddModal() {
            list.add.modal.$promise.then(list.add.modal.show);
        }

        function addModel(model) {
            list.models.push(model);
        }

        /**
         * Refresh the table
         */
        function refreshModels(){
            list.table.total(list.models.length);
            list.table.reload();
        }

        /**
         * This function will add a model to the current list of models and refresh the table
         * @param event
         * @param model
         */
        function modelCreatedSuccess(event, model) {
            addModel(model);
            refreshModels();
            list.add.modal.hide();
        }

        /**
         * This function hide the add modal
         * @param event
         */
        function modelCreatedError(event) {
            list.add.modal.hide();
        }

        /*
         * ---- view
         */

        function showViewModal(model) {

            list.view.modal.$scope.model = model;
            list.view.modal.$promise.then(list.view.modal.show);

        }


        /*
         * ---- delete
         */

        function showDeleteModal(model) {

            list.del.modal.$scope.model = model;
            list.del.modal.$promise.then(list.del.modal.show);

        }

        function deleteModel(model) {
            list.models = _.chain(list.models).reject({id: model.id}).value();
        }


        function modelDeletedSuccess(event, model) {

            list.deleteModel(model);
            list.refreshModels();

            list.del.modal.hide();

        }

        function modelDeletedError(event, model) {
            list.del.modal.hide();
        }


    }

})();
