<template>
  <div class="">
    <template v-if="edit">
      <form>
        <div class="form-group">
          <label for="pdpName">Name</label>
          <input
            type="text"
            name="name"
            v-model="pdpEdit.name"
            v-validate="'alpha_dash|required|min:3'"
            class="form-control"
            id="pdpName"
          >
        </div>
        <div class="form-group">
          <label for="pdpDescription">Description</label>
          <textarea
            name="description"
            v-model="pdpEdit.description"
            v-validate="'required|min:3'"
            class="form-control"
            id="pdpDescription"
          ></textarea>
        </div>
        <ul>
          <li v-for="error in errors.all()" :key="error.id">{{ error }}</li>
        </ul>
        <button type="button" class="btn btn-secondary" @click="edit = false">Cancel</button>
        <span>&nbsp;</span>
        <button type="button" :disabled="errors.any()" class="btn btn-primary" @click="updatePdp()">Update</button>
      </form>
    </template>
    <template v-else>
      <div>
        <h3 class="list-group-item-heading inline">{{ pdp.name }}</h3>
        <div class="pull-right">
          <button
            type="button"
            class="fa fa-trash btn btn-dark btn-sm"
            @click="removePdp(pdp)"
            title="Remove PDP"
          ></button>
          <button
            type="button"
            class="fa fa-edit btn btn-dark btn-sm"
            @click="updatingPdp(pdp)"
            title="Edit PDP"
          ></button>
        </div>
        <p class="list-group-item-text">{{ pdp.description }}</p>
        <h4 class="list-group-item-text">
          <div v-if="!changeProject">
            Project: {{ pdp.project ? pdp.project : 'none' }}
            <button
              type="button"
              class="fa fa-edit btn btn-dark btn-sm"
              @click="changingProject()"
              title="Change project"
            ></button>
          </div>
          <form class="form-inline" v-else>
            <label for="projectId">Project ID: </label>
            &nbsp;
            <input
              type="text"
              name="id"
              v-model="project"
              class="form-control"
              id="projectId"
            >
            &nbsp;
            <button type="button" class="btn btn-secondary" @click="changeProject = false">Cancel</button>
            <span>&nbsp;</span>
            <button
              type="button"
              class="btn btn-primary"
              @click="setProject()"
            >OK</button>
          </form>
        </h4>

        <UpdatePolicy v-if="updatePolicy" :pdp="pdp" @close="updatePolicy = false"></UpdatePolicy>
        <details class="list-group-item-text" v-else>
          <summary>
            <h4 class="inline">
              {{ pdp.security_pipeline.length }} {{ (pdp.security_pipeline.length > 1) ? "policies" : "policy"}}
            </h4>
            <button
              type="button"
              class="fa fa-edit  btn btn-dark btn-sm"
              @click="updatePolicy = true"
              title="Change Policy"
            ></button>
          </summary>
          <div class="list-group">
            <div
              v-for="policy in pdp.security_pipeline" :key="policy.id"
            >
              <h3 class="list-group-item-heading inline">{{ policy.name }}</h3>
             <!--<button
                type="button"
                class="fa fa-trash pull-right btn btn-dark btn-sm"
                @click="removePolicyFromPdp(policy)"
                title="Remove Policy"
              ></button>-->
              <p class="list-group-item-text">{{ policy.description }}</p>
            </div>
          </div>
        </details>
      </div>
    </template>
    <hr>
  </div>
</template>

<script>
import PdpService from './../../services/Pdp.service.js';
//import AddPolicy from "./AddPolicy.vue";
import UpdatePolicy from "./UpdatePolicy";
import util from "./../../services/Util.service.js";

export default {
  name: "pdp",
  data: function() {
    return {
      edit: false,
      updatePolicy: false,
      changeProject: false,
      project: "",
      pdpEdit: {}
    };
  },
  props: {
    pdp: Object
  },
  components: {
    //AddPolicy
    UpdatePolicy
  },
  methods: {
    changingProject() {
      this.project = this.pdp.project;
      this.changeProject = true;
    },
    removePdp() {
      if (confirm('Are you sure to delete this PDP?'))
        PdpService.removePdp(this.pdp);
    },
    updatingPdp() {
      this.pdpEdit = util.clone(this.pdp);
      this.edit = true;
    },
    updatePdp() {
      this.edit = false;
      PdpService.updatePdp(this.pdpEdit);
    },
    removePolicyFromPdp(policy) {
      if (confirm('Are you sure to remove this Policy from PDP?')) {
        //var pdpCopy = util.clone(this.pdp);
        this.pdp.security_pipeline.splice(this.pdp.security_pipeline.indexOf(policy), 1);
        PdpService.updatePdp(this.pdp);
      }
    },
    setProject() {
      var pdpCopy = util.clone(this.pdp);
      pdpCopy.project = this.project;
      PdpService.updatePdp(pdpCopy);
      this.changeProject = false;
    }
  }
};
</script>
