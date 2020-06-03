<template>
  <div>
    <template v-if="edit">
      <form>
        <div class="form-group">
          <label for="modelName">Name</label>
          <input
            type="text"
            name="name"
            v-model="modelEdit.name"
            v-validate="'alpha_dash|required|min:3'"
            class="form-control"
            id="modelName"
          >
        </div>
        <div class="form-group">
          <label for="modelDescription">Description</label>
          <textarea
            name="description"
            v-model="modelEdit.description"
            v-validate="'required|min:3'"
            class="form-control"
          ></textarea>
        </div>
        <ul>
          <li v-for="error in errors.all()" :key="error.id">{{ error }}</li>
        </ul>
        <button type="button" class="btn btn-secondary" @click="edit = false">Cancel</button>
        <span>&nbsp;</span>
        <button type="button" :disabled="errors.any()" class="btn btn-primary" @click="updateModel()">Update</button>
      </form>
    </template>
    <template v-else>
      <h3 class="list-group-item-heading inline">{{ model.name }}</h3>
      <div class="pull-right">
        <button type="button" class="fa fa-trash btn btn-dark btn-sm" @click="removeModel()" title="Remove Model"></button>
        <button type="button" class="fa fa-edit btn btn-dark btn-sm" @click="updatingModel()" title="Edit Model"></button>
      </div>
      <p class="list-group-item-text">{{ model.description }}</p>

      <AddMetarule v-if="addMetarule" :model="model" @close="addMetarule = false"></AddMetarule>
      <details class="list-group-item-text" v-else>
        <summary>
          <h4 class="inline-block width-200">
            {{ model.meta_rules.length + ' meta rule' + (model.meta_rules.length > 1 ? 's' : '&nbsp;') }}
            <i class="fa fa-question-circle" v-if="modelHelpStrings.metarule" data-toggle="tooltip"  :title="modelHelpStrings.metarule"></i>
          </h4>
          <button
            type="button"
            class="fa fa-plus btn btn-dark btn-sm"
            @click="addMetarule = true"
            title="Add Meta Rule"
          ></button>
        </summary>
        <div class="list-group">
          <Metarule
            v-for="metarule in model.meta_rules"
            :key="metarule.id"
            :metarule="metarule"
            :model="model"
          ></Metarule>
        </div>
      </details>
    </template>
    <hr>
  </div>
</template>

<script>
import Metarule from "./Metarule.vue";
import ModelService from "./../../services/Model.service.js";
import AddMetarule from "./AddMetarule.vue";
import util from "./../../services/Util.service.js";
import helpstrings from "../../helpstrings";

export default {
  name: "model",
  data: function() {
    return {
      edit: false,
      addMetarule: false,
      modelEdit: {},
      modelHelpStrings: {}
    };
  },
  components: {
    Metarule,
    AddMetarule
  },
  props: {
    model: Object
  },
  mounted() {
    this.modelHelpStrings = helpstrings.model;
  },
  methods: {
    updatingModel() {
      this.modelEdit = util.clone(this.model);
      this.edit = true;
    },
    updateModel() {
      this.edit = false;
      ModelService.updateModel(this.modelEdit);
    },
    removeModel() {
      if (confirm('Are you sure to delete this Model?')) {
        ModelService.removeModel(this.model);
      }
    }
  }
};
</script>
