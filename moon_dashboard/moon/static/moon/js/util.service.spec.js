(function () {
    'use strict';

    describe('moon.util.service', function () {
        var service;

        beforeEach(module('horizon.app.core'));
        beforeEach(module('horizon.framework'));
        beforeEach(module('moon'));

        beforeEach(inject(function ($injector) {
            service = $injector.get('moon.util.service');
        }));

        it('should push all', function () {
            var a1 = [0, 1, 2];
            var a2 = [3, 4];
            service.pushAll(a1, a2)

            expect(a1.length).toBe(5);
            expect(a1).toEqual([0, 1, 2, 3, 4]);
        });

        it('should index of', function () {
            var a = [{ name: 'n0' }, { name: 'n1' }, { name: 'n2' }];
            var result = service.indexOf(a, 'name', 'n1');

            expect(result).toBe(1);
        });

        it('should map to array', function () {
            var map = { "a": { name: "a" }, "b": { name: "b" } };
            var result = service.mapToArray(map);

            expect(result.length).toBe(2);
        });

        it('should map ID to item', function () {
            var map = { "a": { name: "a" }, "b": { name: "b" } };
            var array = ["a", "b"];
            service.mapIdToItem(array, map);

            expect(array.length).toBe(2);
            expect(array[0].name).toBe("a");
            expect(array[1].name).toBe("b");
        });

        it('should map item to ID', function () {
            var array = [{ id: "a" }, { id: "b" }];
            service.mapItemToId(array);

            expect(array.length).toBe(2);
            expect(array[0]).toBe("a");
            expect(array[1]).toBe("b");
        });

        it('should add to map', function () {
            var map = { "a": { name: "a" }, "b": { name: "b" } };
            var array = [{ id: "c" }];
            service.addToMap(array, map);

            expect(map.c).toEqual({ id: "c" });
        });

        it('should update object', function () {
            var object = { a: 1, b: "test" };
            var update = { a: 2, c: "test2" };
            service.updateObject(object, update);

            expect(object.a).toBe(2);
            expect(object.b).toBe("test");
            expect(object.c).toBe("test2");
        });

        it('should clean object', function () {
            var object = { a: 1, b: "test" };
            service.cleanObject(object);

            expect(object.a).not.toBeDefined();
            expect(object.b).not.toBeDefined();
            expect(object).toEqual({});
        });
    });


})();