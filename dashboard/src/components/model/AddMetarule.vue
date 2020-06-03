<template>
  <div>
    <hr>
    <template v-if="metarules.length > 0">
      <h4>Select metarule:</h4>
      <form data-vv-scope="select">
        <div class="form-group">
          <select v-model="selectedMetaruleId" v-validate.initial="'required'">
            <option disabled value>Please select one</option>
            <option
              v-for="metarule in metarules"
              :value="metarule.id"
              :key="metarule.id"
            >{{metarule.name}}</option>
          </select>
        </div>
        <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
        <span>&nbsp;</span>
        <button
          type="button"
          :disabled="errors.any('select')"
          class="btn btn-primary"
          @click="addMetarule()"
        >Add</button>
      </form>
      <br>
      <br>
      <h4>Or create a new one:</h4>
    </template>
    <h4 v-else>Create a metarule:</h4>
    <form data-vv-scope="create">
      <div class="form-group">
        <label for="metaruleName">Name</label>
        <input
          type="text"
          name="name"
          v-model="metaruleCreate.name"
          v-validate.initial="'alpha_dash|required|min:3'"
          class="form-control"
          id="metaruleName"
        >
      </div>
      <div class="form-group">
        <label for="modelDescription">Description</label>
        <textarea
          name="description"
          v-model="metaruleCreate.description"
          v-validate="'required|min:3'"
          class="form-control"
        ></textarea>
      </div>
      <ul>
        <li v-for="error in errors.all('create')" :key="error.id">{{ error }}</li>
      </ul>
      <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
      <span>&nbsp;</span>
      <button
        type="button"
        :disabled="errors.any('create')"
        class="btn btn-primary"
        @click="createMetarule()"
      >Create and add</button>
    </form>
  </div>
</template>

<script>
import ModelService from "./../../services/Model.service.js";
import util from "./../../services/Util.service.js";

export default {
  name: "addMetarule",
  data: function() {
    return {
      selectedMetaruleId: null,
      metaruleCreate: {
        name: "",
        description: ""
      }
    };
  },
  props: {
    model: Object
  },
  methods: {
    createMetarule() {
      ModelService.createMetaRule(this.metaruleCreate).then(metarule => {
        this.selectedMetaruleId = metarule.id;
        this.addMetarule();
      });
    },
    addMetarule() {
      var metaRule = ModelService.getMetaRule(this.selectedMetaruleId);
      var modelCopy = util.clone(this.model);
      modelCopy.meta_rules.push(metaRule);
      ModelService.updateModel(modelCopy);
      this.close();
    },
    close() {
      this.$emit("close");
    }
  },
  computed: {
    metarules() {
      return ModelService.metaRules.filter(
        el => !this.model.meta_rules.includes(el)
      );
    }
  }
};
</script>
