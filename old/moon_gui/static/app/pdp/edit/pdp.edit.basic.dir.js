(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonPDPEditBasic', moonPDPEditBasic);

    moonPDPEditBasic.$inject = [];

    function moonPDPEditBasic() {

        return {
            templateUrl : 'html/pdp/edit/pdp-edit-basic.tpl.html',
            bindToController : true,
            controller : moonPDPEditBasicController,
            controllerAs : 'edit',
            scope : {
                pdp : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonPDPEditBasicController', moonPDPEditBasicController);

    moonPDPEditBasicController.$inject = ['$scope', 'pdpService', 'formService', 'alertService', '$translate', 'utilService'];

    function moonPDPEditBasicController($scope, pdpService, formService, alertService, $translate, utilService){

        var edit = this;

        edit.editPdp = editPdp;
        edit.init = init;

        edit.form = {};

        activate();

        function activate(){

            edit.pdp = $scope.edit.pdp;

            edit.pdpToEdit = angular.copy(edit.pdp);

        }

        function editPdp(){

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            }else{

                edit.loading = true;

                pdpService.update(edit.pdpToEdit, updateSuccess, updateError);

            }

            function updateSuccess(data) {

                var updatedPdp = utilService.transformOne(data, 'pdps');

                $translate('moon.pdp.edit.basic.success', { pdpName: updatedPdp.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                edit.loading = false;

                $scope.$emit('event:pdpUpdatedSuccess', updatedPdp);

            }

            function updateError(reason) {

                $translate('moon.pdp.edit.basic.error', { pdpName: edit.pdp.name }).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                edit.loading = false;

            }
        }

        function init(){

            edit.pdpToEdit = angular.copy(edit.pdp);

        }
    }

})();
