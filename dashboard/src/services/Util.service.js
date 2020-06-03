import Vue from 'vue'

export default {
    sortByName(items) {
        return items
            .sort((item1, item2) => {
                return item1.name.localeCompare(item2.name);
            });
    },
    filterAndSortByName(items, filter) {
        return items
            .filter(item => {
                return filter == null || item.name.indexOf(filter) >= 0;
            })
            .sort((item1, item2) => {
                return item1.name.localeCompare(item2.name);
            });
    },
    clone: function clone(src) {
        return JSON.parse(JSON.stringify(src));
    },

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
                if (map[id])
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
        for (var i = 0; i < arrayToPush.length; i += 1) {
            array.push(arrayToPush[i]);
        }
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
        return function (response) {
            var text = message;
            if (response && response.data && response.data.message) {
                text += ' (' + response.data.message + ')'
            }
            console.log(text);
            Vue.toasted.global.toast({message: text, type: 'danger', title: 'Error'});
        }
    },

    displaySuccess: function displaySuccess(message) {
        Vue.toasted.global.toast({message: message, type: 'success', title: 'Success'});
    },

    displayError: function displayError(message) {
        Vue.toasted.global.toast({message: message, type: 'danger', title: 'Error'});
    },

    

}