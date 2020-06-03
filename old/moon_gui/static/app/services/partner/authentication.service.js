/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('authenticationService', authenticationService);

    authenticationService.$inject = ['$resource', 'REST_URI', '$sessionStorage', '$http', '$location'];

    function authenticationService($resource, REST_URI, $sessionStorage, $http, $location) {

        return {
            data: $resource(REST_URI.KEYSTONE + 'auth/tokens', {}, {
                login: { method: 'POST' ,
                    /**
                     * Transform Response is needed to add headers into the response object
                     * @param data
                     * @param headersGetter
                     * @returns {{}}
                     */
                  transformResponse : function (data, headersGetter) {
                        var response = {};
                        response.data =  angular.fromJson(data) ;
                        response.headers = headersGetter();
                        return response;
                    }
                },
                logout: { method: 'DELETE' }
            }),

            /**
             *
             * @param credentials object : {username : '', password : ''}
             * @param callbackSuccess
             * @param callbackError
             * @constructor
             */
            Login : function (credentials, callbackSuccess, callbackError){
                var requestData = {
                    auth:{
                        identity:{
                            methods:[
                                'password'
                            ],
                            password:{
                                user:{
                                    name: credentials.username,
                                    domain:{
                                        name:'Default'
                                    },
                                    password: credentials.password
                                }
                            }
                        },
                        scope: {
                            project: {
                                name:'admin',
                                domain:{
                                    name:'Default'
                                }
                            }
                        }
                    }
                };
                this.data.login({}, requestData, function (response){
                    $sessionStorage.currentUser =  response.data;
                    $sessionStorage.currentUser.connectionToken = response.headers['x-subject-token'];
                    SetTokenHeader(response.headers['x-subject-token']);
                    callbackSuccess();
                }, callbackError);
            },
            IsConnected : IsConnected,
            SetTokenHeader : SetTokenHeader,
            GetTokenHeader : GetTokenHeader,
            GetUser : GetUser,
            Logout : Logout
        };

        function IsConnected(){
            return _.has($sessionStorage, 'currentUser');
        }

        function Logout(){
            delete $sessionStorage.currentUser;
            $http.defaults.headers.common['X-Auth-Token'] = '';
            $location.path('/');
        }

        function GetUser(){
            return $sessionStorage.currentUser;
        }

        function GetTokenHeader(){
            return $sessionStorage.currentUser.connectionToken;
        }

        function SetTokenHeader(token){
            $http.defaults.headers.common['X-Auth-Token'] = token;
        }
    }
})();