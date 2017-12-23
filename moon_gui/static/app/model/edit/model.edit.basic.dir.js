(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonModelEditBasic', moonModelEditBasic);

    moonModelEditBasic.$inject = [];

    function moonModelEditBasic() {

        return {
            templateUrl : 'html/model/edit/model-edit-basic.tpl.html',
            bindToController : true,
            controller : moonModelEditBasicController,
            controllerAs : 'edit',
            scope : {
                model : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonModelEditBasicController', moonModelEditBasicController);

    moonModelEditBasicController.$inject = ['$scope', 'modelService', 'formService', 'alertService', '$translate', 'utilService'];

    function moonModelEditBasicController($scope, modelService, formService, alertService, $translate, utilService){

        var edit = this;

        edit.editModel = editModel;
        edit.init = init;

        edit.form = {};

        activate();

        function activate(){

            edit.model = $scope.edit.model;

            edit.modelToEdit = angular.copy(edit.model);

        }

        function editModel(){

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            }else{

                edit.loading = true;

                modelService.update(edit.modelToEdit, updateSuccess, updateError);

            }

            function updateSuccess(data) {

                var updatedModel = utilService.transformOne(data, 'models');

                $translate('moon.model.edit.basic.success', { modelName: updatedModel.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                edit.loading = false;

                $scope.$emit('event:modelUpdatedSuccess', updatedModel);

            }

            function updateError(reason) {

                $translate('moon.model.edit.basic.error', { modelName: edit.model.name }).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                edit.loading = false;

            }
        }

        function init(){

            edit.modelToEdit = angular.copy(edit.model);

        }
    }

})();
