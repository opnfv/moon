<template>
  <div class="list-group-item row">
      <form>
        <div class="form-group">
          <label for="modelName">Name</label>
          <input
            type="text"
            name="name"
            v-model="pdpCreate.name"
            v-validate.initial="'alpha_dash|required|min:3'"
            class="form-control"
            id="modelName"
          >
        </div>
        <div class="form-group">
          <label for="modelDescription">Description</label>
          <textarea
            name="description"
            v-model="pdpCreate.description"
            v-validate.initial="'required|min:3'"
            class="form-control"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="pdpVpi">Vim project id</label>
          <input
                  type="text"
                  name="vim_project_id"
                  v-model="pdpCreate.vim_project_id"
                  class="form-control"
                  id="pdpVpi"
          >
        </div>
        <div class="form-group">
          <label for="pdpPolicy">Policy</label>
          <select v-model="selectedPolicy" class="form-control" id="pdpPolicy" v-validate.initial="'required'" name="policy">
            <option v-for="policy in policies" :key="policy.id" :value="policy.id">{{ policy.name }}</option>
          </select>
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
import PdpService from "./../../services/Pdp.service.js";
import PolicyService from "../../services/Policy.service";
import util from "../../services/Util.service";

export default {
  data: function() {
    return {
      selectedPolicy: null,
      pdpCreate: {
        name: "",
        description: "",
        security_pipeline: [],
        vim_project_id: ""
      }
    };
  },
  computed:{
    policies() {
      return util.sortByName(PolicyService.policies);
    }
  },
  methods: {
    createModel() {
      this.pdpCreate.security_pipeline.push(this.selectedPolicy);
      PdpService.createPdp(this.pdpCreate);
      this.close();
    },
    close() {
      this.$emit("close")
    }
  }
};
</script>
