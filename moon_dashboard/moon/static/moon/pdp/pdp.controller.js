(function () {
  'use strict';

  angular
    .module('moon')
    .controller('moon.pdp.controller',
      controller);

  controller.$inject = ['moon.util.service', 'moon.pdp.service', 'horizon.framework.widgets.form.ModalFormService'];

  function controller(util, pdpService, ModalFormService) {
    var self = this;
    self.model = pdpService;
    pdpService.initialize();

    self.createPdp = function createPdp() {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") }
        }
      };
      var pdp = { name: '', description: '' };
      var config = {
        title: gettext('Create PDP'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }],
        model: pdp
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        pdpService.createPdp(form.model);
      }
    }

    self.updatePdp = function updatePdp(pdp) {
      var schema = {
        type: "object",
        properties: {
          name: { type: "string", minLength: 2, title: gettext("Name") },
          description: { type: "string", minLength: 2, title: gettext("Description") }
        }
      };
      var config = {
        title: gettext('Update PDP'),
        schema: schema,
        form: ['name', { key: 'description', type: 'textarea' }],
        model: angular.copy(pdp)
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        pdpService.updatePdp(form.model);
      }
    }

    self.removePdp = function removePdp(pdp) {
      if (confirm(gettext('Are you sure to delete this PDP?')))
        pdpService.removePdp(pdp);
    }

    self.addPolicy = function addPolicy(pdp) {
      var schema = {
        type: "object",
        properties: {
          id: { type: "string", title: gettext("Select a Policy:") }
        }
      };
      var titleMap = util.arrayToTitleMap(pdpService.policies)
      var config = {
        title: gettext('Add Policy'),
        schema: schema,
        form: [{ key: 'id', type: 'select', titleMap: titleMap }],
        model: {}
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        var pdpCopy = angular.copy(pdp);
        pdpCopy.security_pipeline.push(pdpService.getPolicy(form.model.id));
        pdpService.updatePdp(pdpCopy);
      }
    }

    self.removePolicyFromPdp = function removePolicyFromPdp(pdp, policy) {
      if (confirm(gettext('Are you sure to remove this Policy from PDP?'))) {
        var pdpCopy = angular.copy(pdp);
        pdpCopy.security_pipeline.splice(pdp.security_pipeline.indexOf(policy), 1);
        pdpService.updatePdp(pdpCopy);
      }
    }

    self.changeProject = function changeProject(pdp) {
      var schema = {
        type: "object",
        properties: {
          id: { type: "string", title: gettext("Select a Project:") }
        }
      };
      var model = {id : pdp.keystone_project_id};

      var titleMap = util.arrayToTitleMap(pdpService.projects)
      var config = {
        title: gettext('Change Project'),
        schema: schema,
        form: [{ key: 'id', type: 'select', titleMap: titleMap }],
        model: model
      };
      ModalFormService.open(config).then(submit);

      function submit(form) {
        var pdpCopy = angular.copy(pdp);
        pdpCopy.project = pdpService.getProject(form.model.id);
        pdpService.updatePdp(pdpCopy);
      }
    }

  }
})();