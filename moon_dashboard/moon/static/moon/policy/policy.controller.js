(function () {
  'use strict';

  angular
    .module('moon')
    .controller('moon.policy.controller',
      controller);

  controller.$inject = ['moon.util.service', 'moon.policy.service', 'moon.model.service', 'horizon.framework.widgets.form.ModalFormService'];

  function controller(util, policyService, modelService, ModalFormService) {
    var self = this;
    var genres = [{ value: 'admin', name: gettext('admin') }, { value: 'authz', name: gettext('authz') }];
    self.model = policyService;
    self.selectedRule = null;
    self.currentData = null;
    policyService.initialize();

    var dataTitleMaps = {};

    var categoryMap = {
      subject: {
        perimeterId: 'subject_id'
      },
      object: {
        perimeterId: 'object_id'
      },
      action: {
        perimeterId: 'action_id'
      },
    }

    function createAddDataButton(type, index, category, config, policy) {
      config.form.push({
        "key": type + index + "Button",
        "type": "button",
        "title": "Add",
        onClick: createDataFunction(type, category, policy)
      })
    }

    function createDataFunction(type, category, policy) {
      return function () {
        var schema = {
          type: "object",
          properties: {
            name: { type: "string", minLength: 2, title: gettext("Name") },
            description: { type: "string", minLength: 2, title: gettext("Description") },
          }
        };
        var data = { name: '', description: '' };
        var config = {
          title: gettext('Create Data of ' + category.name + ' category'),
          schema: schema,
          form: ['name', { key: 'description', type: 'textarea' }],
          model: data
        };
        ModalFormService.open(config).then(submit);

        function submit(form) {
          policyService.createData(type, policy, category, form.model).then(
            function (data) {
              util.pushAll(dataTitleMaps[category.id], util.arrayToTitleMap(data));
            }
          );
        }
      }
    }

    function getOrCreateDataTitleMap(category, data, policy) {
      var result = dataTitleMaps[category.id];
      if (!result) {
        result = util.arrayToTitleMap(data);
        dataTitleMaps[category.id] = result;
      }
      return result;
    }

    function createDataSelect(type, categories, data, config, policy) {
      for (var i = 0; i < categories.length; i++) {
        var category = categories[i];
        var titleMap = getOrCreateDataTitleMap(category, data, policy);
        config.schema.properties[type + i] = { type: "string", title: gettext('Select ' + type + ' data of ' + category.name + ' category') };
        config.form.push({ key: type + i, type: 'select', titleMap: titleMap });
        createAddDataButton(type, i, category, config, policy);
      }
    }

    function pushData(type, model, array) {
      var i = 0;
      while ((type + i) in model) {
        array.push(model[type + i]);
        i++;
      }
    }

    self.createPolicy = function createPolicy() {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") },
          genre: { type: "string", title: gettext("genre") },
          model_id: { type: "string", title: gettext("Select a Model:") }
        }
      };
      var policy = { name: '', description: '', model_id: null, genre: '' };
      var titleMap = util.arrayToTitleMap(modelService.models)
      var config = {
        title: gettext('Create Policy'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }, { key: 'genre', type: 'select', titleMap: genres }, { key: 'model_id', type: 'select', titleMap: titleMap }],
        model: policy
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        policyService.createPolicy(form.model);
      }
    }

    self.updatePolicy = function updatePolicy(policy) {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") },
          genre: { type: "string", title: gettext("Genre") },
        }
      };
      var config = {
        title: gettext('Update Policy'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }, { key: 'genre', type: 'select', titleMap: genres }],
        model: { name: policy.name, description: policy.description, model_id: policy.model_id, id: policy.id, genre: policy.genre }
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        policyService.updatePolicy(form.model);
      }
    }

    self.addRuleWithMetaRule = function addRuleWithMetaRule(policy, metaRule) {
      var schema = {
        type: "object",
        properties: {
          instructions: { type: "string", title: gettext("Instructions") }
        }
      };

      var config = {
        title: gettext('Add Rule'),
        schema: schema,
        form: [],
        model: {
          instructions: '[{"decision": "grant"}]'
        }
      };
      dataTitleMaps = {};
      createDataSelect('subject', metaRule.subject_categories, policy.subjectData, config, policy);
      createDataSelect('object', metaRule.object_categories, policy.objectData, config, policy);
      createDataSelect('action', metaRule.action_categories, policy.actionData, config, policy);
      config.form.push({ key: 'instructions', type: 'textarea' })

      ModalFormService.open(config).then(submit);

      function submit(form) {
        var rule = { enabled: true };
        rule.instructions = JSON.parse(form.model.instructions);
        rule.meta_rule_id = metaRule.id;
        rule.policy_id = policy.id;
        rule.rule = [];
        pushData('subject', form.model, rule.rule);
        pushData('object', form.model, rule.rule);
        pushData('action', form.model, rule.rule);
        policyService.addRuleToPolicy(policy, rule);
      }
    }

    self.addRule = function addRule(policy) {
      var schema = {
        type: "object",
        properties: {
          metaRuleId: { type: "string", title: gettext("Select a Metarule:") }
        }
      };
      var rule = { metaRuleId: null };
      var titleMap = util.arrayToTitleMap(policy.model.meta_rules);
      var config = {
        title: gettext('Add Rule'),
        schema: schema,
        form: [{ key: 'metaRuleId', type: 'select', titleMap: titleMap }],
        model: rule
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        self.addRuleWithMetaRule(policy, modelService.getMetaRule(form.model.metaRuleId));
      }
    }

    self.removePolicy = function removePolicy(policy) {
      if (confirm(gettext('Are you sure to delete this Policy?')))
        policyService.removePolicy(policy);
    }

    self.populatePolicy = function populatePolicy(policy) {
      policyService.populatePolicy(policy);
    }

    self.removeRuleFromPolicy = function removeRuleFromPolicy(policy, rule) {
      if (confirm(gettext('Are you sure to delete this Rule?')))
        policyService.removeRuleFromPolicy(policy, rule);
    }

    self.showRule = function showRule(rule) {
      self.selectedRule = rule;
    }

    self.hideRule = function hideRule() {
      self.selectedRule = null;
      self.currentData = null;
    }

    self.assignData = function assignData(type, policy, data) {
      self.currentData = {
        data: data,
        type: type,
        loading: true,
        perimeters: [],
        assignments: []
      }

      policyService.loadPerimetersAndAssignments(type, policy).then(function (values) {
        var category = categoryMap[type];
        self.currentData.loading = false;
        self.currentData.perimeters = values.perimeters;
        for (var index = 0; index < values.assignments.length; index++) {
          var assignment = values.assignments[index];
          if (assignment.assignments.indexOf(data.id) >= 0) {
            var perimeter = values.perimetersMap[assignment[category.perimeterId]];
            self.currentData.assignments.push(perimeter);
            self.currentData.perimeters.splice(self.currentData.perimeters.indexOf(perimeter), 1);
          }
        }
      })
    }

    self.createPerimeter = function createPerimeter(type, policy) {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") },
        }
      };
      if (type == 'subject') {
        schema.properties.email = { type: "email", "type": "string", "pattern": "^\\S+@\\S+$", title: gettext("Email") }
      }
      var perimeter = { name: '', description: '' };
      var config = {
        title: gettext('Create Perimeter'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }],
        model: perimeter
      };
      if (type == 'subject') {
        config.form.push('email');
      }
      
      ModalFormService.open(config).then(submit);

      function submit(form) {
        policyService.createPerimeter(type, policy, form.model).then(function (perimeters) {
          util.pushAll(self.currentData.perimeters, perimeters);
        })
      }
    }

    self.assign = function assign(type, policy, perimeter, data) {
      policyService.createAssignment(type, policy, perimeter, data).then(function () {
        self.currentData.assignments.push(perimeter);
        self.currentData.perimeters.splice(self.currentData.perimeters.indexOf(perimeter), 1);
      })
    }

    self.unassign = function unassign(type, policy, perimeter, data) {
      policyService.removeAssignment(type, policy, perimeter, data).then(function () {
        self.currentData.perimeters.push(perimeter);
        self.currentData.assignments.splice(self.currentData.assignments.indexOf(perimeter), 1);
      })
    }
  }
})();