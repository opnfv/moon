<template>
  <div class="list-group-item row">
    <form>
      <div class="form-group">
        <label for="policyName">Name</label>
        <input
          type="text"
          name="name"
          v-model="policyCreate.name"
          v-validate.initial="'alpha_dash|required|min:3'"
          class="form-control"
          id="policyName"
        />
      </div>
      <div class="form-group">
        <label for="policyDescription">Description</label>
        <textarea
          name="description"
          v-model="policyCreate.description"
          v-validate.initial="'required|min:3'"
          class="form-control"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="policyGenre">Genre</label>
        <select v-model="policyCreate.genre" class="form-control" id="policyGenre" v-validate.initial="'required'" name="genre">
          <option>admin</option>
          <option>authz</option>
        </select>
      </div>
      <div class="form-group">
        <label for="policyModel">Model</label>
        <select v-model="policyCreate.model_id" class="form-control" id="policyModel" v-validate.initial="'required'" name="model">
          <option v-for="model in models" :key="model.id" :value="model.id">{{ model.name }}</option>
        </select>
      </div>
      <ul>
        <li v-for="error in errors.all()" :key="error.id">{{ error }}</li>
      </ul>
      <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
      <span>&nbsp;</span>
      <button
        type="button"
        :disabled="errors.any()"
        class="btn btn-primary"
        @click="createPolicy()"
      >Create</button>
    </form>
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";
import ModelService from "./../../services/Model.service.js";
import util from "./../../services/Util.service.js";

export default {
  name: "createPolicy",
  data: function() {
    return {
      policyCreate: {
        name: "",
        description: "",
        genre: "",
        model_id: ""
      }
    };
  },
  computed: {
    models() {
      return util.sortByName(ModelService.models);
    }
  },
  methods: {
    createPolicy() {
      PolicyService.createPolicy(this.policyCreate);
      this.close();
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>
