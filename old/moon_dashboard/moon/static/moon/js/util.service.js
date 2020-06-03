(function () {

    'use strict';

    angular
        .module('moon')
        .factory('moon.util.service', utilService);

    utilService.$inject = ['horizon.framework.widgets.toast.service'];

    function utilService(toast) {


        return {
            mapToArray: function mapToArray(map, action) {
                var result = []
                for (var key in map) {
                    if (map.hasOwnProperty(key)) {
                        var item = map[key];
                        item.id = key;
                        if (action != null) {
                            action(item);
                        }
                        result.push(item);
                    }
                }
                return result;
            },

            mapIdToItem: function mapIdToItem(array, map) {
                if (array) {
                    for (var index = 0; index < array.length; index++) {
                        var id = array[index];
                        array[index] = map[id];
                    }
                }
            },

            mapItemToId: function mapItemToId(array) {
                if (array) {
                    for (var index = 0; index < array.length; index++) {
                        var item = array[index];
                        array[index] = item.id;
                    }
                }
            },

            addToMap: function addToMap(array, map) {
                if (array) {
                    for (var index = 0; index < array.length; index++) {
                        var item = array[index];
                        map[item.id] = item;
                    }
                }
            },

            updateObject: function updateObject(object, newObject) {
                for (var key in newObject) {
                    if (newObject.hasOwnProperty(key)) {
                        object[key] = newObject[key];
                    }
                }
            },

            cleanObject: function cleanObject(object) {
                for (var key in object) {
                    if (object.hasOwnProperty(key)) {
                        delete object[key];
                    }
                }
            },

            pushAll: function pushAll(array, arrayToPush) {
                Array.prototype.push.apply(array, arrayToPush);
            },

            indexOf: function indexOf(array, property, value) {
                for (var i = 0; i < array.length; i += 1) {
                    if (array[i][property] === value) {
                        return i;
                    }
                }
                return -1;
            },

            createInternal: function createInternal(data, array, map, action) {
                var added = this.mapToArray(data, action)
                this.addToMap(added, map);
                this.pushAll(array, added);
                return added;
            },

            updateInternal: function updateInternal(data, map, action) {
                var updated = this.mapToArray(data, action)
                var result = []
                for (var index = 0; index < updated.length; index++) {
                    var item = updated[index];
                    this.updateObject(map[item.id], item)
                    result.push(map[item.id])
                }
                return result;
            },

            removeInternal: function removeInternal(id, array, map) {
                var old = map[id];
                delete map[old.id];
                array.splice(array.indexOf(old), 1);
                return old;
            },

            arrayToTitleMap: function arrayToTitleMap(array) {
                return array.map(function (item) {
                    return { value: item.id, name: item.name }
                }).sort(function (itemA, itemB) {
                    return itemA.name.localeCompare(itemB.name);
                })
            },

            displayErrorFunction: function displayErrorFunction(message) {
                return function(response) {
                    var text = gettext(message);
                    if (response && response.data && response.data.message) {
                        text += ' (' + response.data.message + ')'
                    }
                    toast.add('error', text);
                }
            },
    
            displaySuccess: function displaySuccess(message) {
                toast.add('success', gettext(message));
            },

            displayError: function displayError(message) {
                toast.add('error', gettext(message));
            },

        }

    }
})();