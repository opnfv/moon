/**
 * @author Samy Abdallah
 */
(function() {

    'use strict';

    angular
        .module('moon')
        .controller('AuthenticationController', AuthenticationController);

    AuthenticationController.$inject = ['authenticationService', '$translate', 'alertService', '$state', '$rootScope'];

    function AuthenticationController(authenticationService, $translate, alertService, $state, $rootScope) {

        var vm = this;

        vm.login = login;
        vm.loading = false;

        vm.credentials = {
            username : '',
            password : ''
        };

        activate();

        function activate(){
            if($rootScope.connected){
                $state.go('moon.dashboard');
            }
        }

        function login(){
            vm.loading = true;
            authenticationService.Login(vm.credentials, loginSuccess, loginError);
        }

        function loginSuccess() {

            $translate('moon.login.success').then( function(translatedValue) {
                alertService.alertSuccess(translatedValue);
                $state.go('moon.dashboard');
                vm.loading = false;
            });

        }

        function loginError(reason) {

            $translate('moon.login.error', { errorCode: reason.status }).then( function(translatedValue) {
                alertService.alertError(translatedValue);
                vm.loading = false;
            });

        }
    }
})();