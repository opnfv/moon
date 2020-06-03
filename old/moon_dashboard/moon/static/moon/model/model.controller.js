(function () {
  'use strict';

  angular
    .module('moon')
    .directive('onReadFile', directive)
    .controller('moon.model.controller', controller);

  controller.$inject = ['moon.util.service', 'moon.model.service', 'moon.import.service', 'horizon.framework.widgets.form.ModalFormService'];

  directive.$inject = ['$parse'];

  function directive($parse) {
    return {
      restrict: 'A',
      scope: false,
      link: function (scope, element, attrs) {
        element.bind('change', function (e) {

          var onFileRead = $parse(attrs.onReadFile);
          var reader = new FileReader();

          reader.onload = function () {
            var fileContents = reader.result;
            scope.$apply(function () {
              onFileRead(scope, {
                'contents': fileContents
              });
            });
          };
          reader.readAsText(element[0].files[0]);
        });
      }
    };
  }

  var categoryMap = {
    'subject': {
      addTitle: 'Add Subject Category',
      removeTitleFromMetaRule: 'Are you sure to remove from meta rule this Subject Category?',
      removeTitle: 'Are you sure to remove this Subject Category?',
      listName: 'subject_categories',
      serviceListName: 'subjectCategories'
    },
    'object': {
      addTitle: 'Add Object Category',
      removeTitleFromMetaRule: 'Are you sure to remove from meta rule this Object Category?',
      removeTitle: 'Are you sure to remove this Object Category?',
      listName: 'object_categories',
      serviceListName: 'objectCategories'
    },
    'action': {
      addTitle: 'Add Action Category',
      removeTitleFromMetaRule: 'Are you sure to remove from meta rule this Action Category?',
      removeTitle: 'Are you sure to remove this Action Category?',
      listName: 'action_categories',
      serviceListName: 'actionCategories'
    },
  }

  function controller(util, modelService, importService, ModalFormService) {
    var self = this;
    self.model = modelService;
    self.showOrphan = false;
    modelService.initialize();

    self.importData = function importData(text) {
      horizon.modals.modal_spinner(gettext("Loading"))
      importService.importData(JSON.parse(text)).then(function () {
        modelService.initialize();
        horizon.modals.spinner.modal('hide');
      })
    }

    self.createModel = function createModel() {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") }
        },
        required: ['name', 'description']
      };
      var model = { name: '', description: '' };
      var config = {
        title: gettext('Create Model'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }],
        model: model
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        modelService.createModel(form.model);
      }
    }

    self.updateModel = function updateModel(model) {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") }
        },
        required: ['name', 'description']
      };
      var config = {
        title: gettext('Update Model'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }],
        model: angular.copy(model)
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        modelService.updateModel(form.model);
      }
    }

    self.removeModel = function removeModel(model) {
      if (confirm(gettext('Are you sure to delete this Model?')))
        modelService.removeModel(model);
    }

    self.createMetaRuleFunction = function createMetaRuleFunction(model, titleMap) {
      return function () {
        var schema = {
          type: "object",
          properties: {
            name: { type: "string", minLength: 2, title: gettext("Name") },
            description: { type: "string", minLength: 2, title: gettext("Description") },
          },
          required: ['name', 'description']
        };
        var metaRule = { name: '', description: '' };
        var config = {
          title: gettext('Create Meta Rule'),
          schema: schema,
          form: [
            'name',
            { key: 'description', type: 'textarea' }
          ],
          model: metaRule
        };
        ModalFormService.open(config).then(submit);

        function submit(form) {
          modelService.createMetaRule(form.model).then(function (metaRule) {
            titleMap.push({ value: metaRule.id, name: metaRule.name })
            model.id = metaRule.id
          })
        }
      }
    }

    self.addMetaRule = function addMetaRule(model) {
      var schema = {
        type: "object",
        properties: {
          id: { type: "string", title: gettext("Select a Meta Rule:") }
        },
        required: ['id']
      };
      var titleMap = util.arrayToTitleMap(modelService.metaRules)
      var formModel = { id: null }
      var config = {
        title: gettext('Add Meta Rule'),
        schema: schema,
        form: [
          { key: 'id', type: 'select', titleMap: titleMap },
          {
            key: 'createButton',
            type: 'button',
            title: gettext('Create Meta Rule'),
            icon: 'fa fa-plus',
            onClick: self.createMetaRuleFunction(formModel, titleMap)
          }
        ],
        model: formModel
      };
      if (modelService.metaRules.length == 1) {
        formModel.id = modelService.metaRules[0].id
      }

      ModalFormService.open(config).then(submit);

      function submit(form) {
        var metaRule = modelService.getMetaRule(form.model.id);
        var modelCopy = angular.copy(model);
        modelCopy.meta_rules.push(metaRule);
        modelService.updateModel(modelCopy);
      }
    }

    self.updateMetaRule = function updateMetaRule(metaRule) {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") }
        },
        required: ['name', 'description']
      };
      var metaRuleCopy = angular.copy(metaRule);
      var config = {
        title: gettext('Update Meta Rule'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }],
        model: metaRuleCopy
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        modelService.updateMetaRule(form.model);
      }
    }

    self.removeMetaRuleFromModel = function removeMetaRuleFromModel(model, metaRule) {
      if (confirm(gettext('Are you sure to remove this Meta Rule from model?'))) {
        var modelCopy = angular.copy(model);
        modelCopy.meta_rules.splice(model.meta_rules.indexOf(metaRule), 1);
        modelService.updateModel(modelCopy);
      }
    }

    self.removeMetaRule = function removeMetaRule(metaRule) {
      if (confirm(gettext('Are you sure to remove this Meta Rule?'))) {
        modelService.removeMetaRule(metaRule);
      }
    }

    self.createCategoryFunction = function createCategoryFunction(type, formModel, titleMap) {
      return function () {
        var schema = {
          type: "object",
          properties: {
            name: { type: "string", minLength: 2, title: gettext("Name") },
            description: { type: "string", minLength: 2, title: gettext("Description") },
          },
          required: ['name', 'description']
        };
        var metaRule = { name: '', description: '' };
        var config = {
          title: gettext('Create Category'),
          schema: schema,
          form: [
            'name',
            { key: 'description', type: 'textarea' }
          ],
          model: metaRule
        };
        ModalFormService.open(config).then(submit);

        function submit(form) {
          modelService.createCategory(type, form.model).then(function (category) {
            titleMap.push({ value: category.id, name: category.name })
            formModel.id = category.id
          })
        }
      }
    }

    self.addCategory = function addCategory(type, metaRule) {
      var typeValue = categoryMap[type];
      var schema = {
        type: "object",
        properties: {
          id: { type: "string", title: gettext("Select a Category:") }
        },
        required: ['id']
      };
      var titleMap = util.arrayToTitleMap(modelService[typeValue.serviceListName])
      var formModel = { id: null }
      var config = {
        title: gettext(typeValue.addTitle),
        schema: schema,
        form: [
          { key: 'id', type: 'select', titleMap: titleMap },
          {
            key: 'createButton',
            type: 'button',
            title: gettext('Create Category'),
            icon: 'fa fa-plus',
            onClick: self.createCategoryFunction(type, formModel, titleMap)
          }],
        model: formModel
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        var category = modelService.getCategory(type, form.model.id);
        var metaRuleCopy = angular.copy(metaRule);
        metaRuleCopy[typeValue.listName].push(category);
        modelService.updateMetaRule(metaRuleCopy)
      }
    }

    self.removeCategoryFromMetaRule = function removeCategoryFromMetaRule(type, metaRule, category) {
      var typeValue = categoryMap[type];
      if (confirm(gettext(typeValue.removeTitleFromMetaRule))) {
        var metaRuleCopy = angular.copy(metaRule);
        metaRuleCopy[typeValue.listName].splice(metaRule[typeValue.listName].indexOf(category), 1);
        modelService.updateMetaRule(metaRuleCopy);
      }
    }

    self.removeCategory = function removeCategory(type, category) {
      var typeValue = categoryMap[type];
      if (confirm(gettext(typeValue.removeTitle))) {
        modelService.removeCategory(type, category);
      }
    }


  }
})();