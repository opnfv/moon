/**
# Copyright 2015 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
 */

(function() {

	'use strict';

	var moon = angular
	
		.module('moon', ['ngResource',
		                 'ngRoute',                                            
	                     'ui.router',
						 'ngMessages',
	                     'ui.bootstrap',
	                     'ngTable',
	                     'ngCookies',
						 'ngStorage',
	                     'pascalprecht.translate',
	                     'ngAnimate',
	                     'mgcrea.ngStrap',
	                     'NgSwitchery',
	                     'ui.select',
	                     'toaster'])
	
	                     .config(configure)
	                     .run(runner);
	
	/*
	 * configure
	 */

    configure.$inject = ['$urlRouterProvider', '$translateProvider', '$stateProvider', 'uiSelectConfig'];
	
	function configure($urlRouterProvider, $translateProvider, $stateProvider, uiSelectConfig) {
		
	    /*
	     * translate
	     */
	    
	    $translateProvider
	        .useStaticFilesLoader({
	            prefix: 'assets/i18n/',
	            suffix: '.json'
		    })
		    .preferredLanguage('en')
		    .useCookieStorage();
	    
	    /*
	     * ui-select
	     */
	    
	    uiSelectConfig.theme = 'selectize';
	    
	    /*
	     * routes
	     */
	    
	    $urlRouterProvider.when('', '/model');
        $urlRouterProvider.when('/', '/model');
	    $urlRouterProvider.otherwise('/404');
	    
	    configureDefaultRoutes($stateProvider);

	    configureDashboard($stateProvider);

        configureAuthRoutes($stateProvider);

	    configureProjectRoutes($stateProvider);

	    configureModelRoutes($stateProvider);
	    
	    configurePDPRoutes($stateProvider);

        configurePolicyRoutes($stateProvider);

	    configureLogsRoutes($stateProvider);
	   		
	}
	
	function configureDefaultRoutes($stateProvider) {
		
		$stateProvider
	    
		    .state('moon', {
		        abstract: true,
		        template: '<div ui-view></div>'
		    })
		    
		    .state('moon.404', {
	    		url: '/404',
	            templateUrl: 'html/common/404/404.tpl.html'
	        });
		
		return $stateProvider;
		
	}

	function configureDashboard($stateProvider){

        $stateProvider

		.state('moon.dashboard',{
			url: '/dashboard',
			templateUrl: 'html/dashboard/dashboard.tpl.html'
		});

        return $stateProvider;

    }

	function configureAuthRoutes($stateProvider){

        $stateProvider

			.state('moon.auth', {
				abstract: true,
				template: '<div ui-view></div>'
			})

			.state('moon.auth.login', {
				url: '/login',
				templateUrl: 'html/authentication/authentication.tpl.html',
				controller: 'AuthenticationController',
				controllerAs: 'auth'
			});

        return $stateProvider;
	}

    function configureModelRoutes($stateProvider) {

        $stateProvider

            .state('moon.model', {
                abstract: true,
                template: '<div ui-view></div>'
            })

            .state('moon.model.list', {
                url: '/model',
                templateUrl: 'html/model/model-list.tpl.html',
                controller: 'ModelListController',
                controllerAs: 'list',
                resolve: {
                    models: ['modelService', function(modelService) {
                        return modelService.findAll();
                    }]
                }
            })

			.state('moon.model.edit', {
                url: '/model/:id',
				templateUrl: 'html/model/edit/model-edit.tpl.html',
				controller: 'ModelEditController',
				controllerAs: 'edit',
                resolve: {
                    model: ['$stateParams','modelService', function($stateParams, modelService) {
                        return modelService.findOneWithMetaRules($stateParams.id);
                    }]
				}
			});


        return $stateProvider;

    }

	function configureProjectRoutes($stateProvider) {
		
		 $stateProvider
	        
	        .state('moon.project', {
				abstract: true,
		        template: '<div ui-view></div>'
	        })
	        		
			.state('moon.project.list', {
				url: '/project',
				templateUrl: 'html/project/project-list.tpl.html',
				controller: 'ProjectListController',
				controllerAs: 'list',
	            resolve: {
	            	projects: ['projectService', function(projectService) {
	            		return projectService.findAll();
	            	}]
	            }
			});

		 return $stateProvider;
		
	}
	
	function configurePDPRoutes($stateProvider) {
		
		$stateProvider
		
			.state('moon.pdp', {
				abstract: true,
		        template: '<div ui-view></div>'
	        })
			
			.state('moon.pdp.list', {
				url: '/pdp',
	            templateUrl: 'html/pdp/pdp-list.tpl.html',
	            controller: 'PDPListController',
	            controllerAs: 'list',
	            resolve: {
	            	pdps: ['pdpService', function(pdpService) {
                        return pdpService.findAll();
	            	}]
	            }
	        })

            .state('moon.pdp.edit', {
                url: '/pdp/:id',
                templateUrl: 'html/pdp/edit/pdp-edit.tpl.html',
                controller: 'PDPEditController',
                controllerAs: 'edit',
                resolve: {
                    pdp: ['$stateParams','pdpService', function($stateParams, pdpService) {
                        return pdpService.findOne($stateParams.id);
                    }]
                }
            });
		
		return $stateProvider;
		
	}

    function configurePolicyRoutes($stateProvider) {

        $stateProvider

            .state('moon.policy', {
                abstract: true,
                template: '<div ui-view></div>'
            })

            .state('moon.policy.list', {
                url: '/policy',
                templateUrl: 'html/policy/policy-list.tpl.html',
                controller: 'PolicyListController',
                controllerAs: 'list',
                resolve: {
                    policies: ['policyService', function(policyService) {
                        return policyService.findAll();
                    }]
                }
            })

            .state('moon.policy.edit', {
                url: '/policy/:id',
                templateUrl: 'html/policy/edit/policy-edit.tpl.html',
                controller: 'PolicyEditController',
                controllerAs: 'edit',
                resolve: {
                    policy: ['$stateParams','policyService', function($stateParams, policyService) {
                        return policyService.findOne($stateParams.id);
                    }]
                }
            });


        return $stateProvider;

    }

	function configureLogsRoutes($stateProvider){

        $stateProvider

            .state('moon.logs', {
                url: '/logs',
                templateUrl: 'html/logs/logs.tpl.html',
                controller: 'LogsController',
                controllerAs: 'logs'
            });

        return $stateProvider;
	}
	
	/*
	 * runner
	 */
	
	runner.$inject = ['$rootScope', '$modal', '$translate', 'alertService', 'authenticationService', '$sessionStorage', '$location'];
	
	function runner($rootScope, $modal, $translate, alertService, authenticationService, $sessionStorage, $location) {

        $rootScope.connected = authenticationService.IsConnected();

		$rootScope.transitionModal = $modal({ scope: $rootScope, template: 'html/common/waiting/waiting.tpl.html', backdrop: 'static', show: false });

		$rootScope.$on('$stateChangeStart', stateChangeStart);
		$rootScope.$on('$stateChangeSuccess', stateChangeSuccess);
		$rootScope.$on('$stateChangeError', stateChangeError);
        $rootScope.$on('$locationChangeStart', locationChangeStart);

        // keep user logged in after page refresh
        if (authenticationService.IsConnected()) {
            authenticationService.SetTokenHeader(authenticationService.GetTokenHeader());
        }

        // redirect to login page if not logged in and trying to access a restricted pages
        function locationChangeStart(event, next, current) {
            var publicPages = ['/login'];
            var restrictedPage = publicPages.indexOf($location.path()) === -1;
            if (restrictedPage && !$sessionStorage.currentUser) {
                $location.path('/login');
            }
        }

        function stateChangeStart() {
        	$rootScope.connected = authenticationService.IsConnected();
        	$rootScope.transitionModal.$promise.then($rootScope.transitionModal.show);
	    }
	    
	    function stateChangeSuccess() {
			$rootScope.transitionModal.hide();
	    }
	    
	    function stateChangeError(event, toState, toParams, fromState, fromParams, error) {
	    	
	    	var stacktrace = getStacktrace(event, toState, toParams, fromState, fromParams, error);

	    	$translate('moon.global.error', { stacktrace: stacktrace }).then(function (translatedValue) {
    			alertService.alertError(translatedValue);
            });
	    	
			$rootScope.transitionModal.hide();
						
	    }
	    
	    function getStacktrace(event, toState, toParams, fromState, fromParams, error) {
	    	
	    	var stacktrace = {};
	    	
	    	stacktrace.status = error.status;
	    	stacktrace.message = error.statusText;
	    	stacktrace.state = toState;
	    	stacktrace.params = toParams;
	    	
	    	return stacktrace;

	    }

    }
	
})();
