/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('utilService', utilService);

    utilService.$inject = [];

    function utilService() {

        return {


            /**
             * Transforms an answer from server and return an array of objects instead the @param data

             * @param data    object : {
             *      'typeOfTheRreturnedObject' : {
             *          'idObject1' : {....},
             *          'idObject2' : {....}
             *      }
             * }
             * @param typeOfObject
             * @returns {Array}
             */
            transform : function(data, typeOfObject){

                var result = [];

                _.each(data[typeOfObject],function(item, key){
                    item.id = key;
                    result.push(item);
                });

                return result;
            },

            /**
             * same as transform but with only one object
             * @param data
             * @param typeOfObject the first elem of the dictonnary
             */
            transformOne : function(data, typeOfObject){

                var result = [];

                _.each(data[typeOfObject], function (item, key) {
                    item.id = key;
                    result.push(item);
                });

                return result[0];

            }

        };

    }

})();
