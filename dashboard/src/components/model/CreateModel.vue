<template>
  <div class="list-group-item row">
      <form>
        <div class="form-group">
          <label for="modelName">Name</label>
          <input
            type="text"
            name="name"
            v-model="modelCreate.name"
            v-validate.initial="'alpha_dash|required|min:3'"
            class="form-control"
            id="modelName"
          >
        </div>
        <div class="form-group">
          <label for="modelDescription">Description</label>
          <textarea
            name="description"
            v-model="modelCreate.description"
            v-validate.initial="'required|min:3'"
            class="form-control"
          ></textarea>
        </div>
        <ul>
          <li v-for="error in errors.all()" :key="error.id">{{ error }}</li>
        </ul>
        <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
        <span>&nbsp;</span>
        <button type="button" :disabled="errors.any()" class="btn btn-primary" @click="createModel()">Create</button>
      </form>
  </div>
</template>

<script>
import ModelService from "./../../services/Model.service.js";

export default {
  name: "createModel",
  data: function() {
    return {
      modelCreate: {
        name: "",
        description: ""
      }
    };
  },
  methods: {
    createModel() {
      ModelService.createModel(this.modelCreate);
      this.close();
    },
    close() {
      this.$emit("close")
    }
  }
};
</script>
