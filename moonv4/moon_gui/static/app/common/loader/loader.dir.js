(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonLoader', moonLoader);

    moonLoader.$inject = [];

    function moonLoader() {

        return {
            templateUrl : 'html/common/loader/loader.tpl.html',
            restrict : 'E'
        };
    }

})();
