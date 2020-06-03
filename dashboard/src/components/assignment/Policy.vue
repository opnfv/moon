<template>
  <div>
    <template v-if="edit">
      <form>
        <div class="form-group" >
          <label for="policyName">Name</label>
          <input
            type="text"
            name="name"
            v-model="policyEdit.name"
            v-validate="'alpha_dash|required|min:3'"
            class="form-control"
            id="policyName"
          />
        </div>
        <div class="form-group">
          <label for="policyDescription">Description</label>
          <textarea
            name="description"
            v-model="policyEdit.description"
            v-validate="'required|min:3'"
            class="form-control"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="policyGenre">Genre</label>
          <select
            v-model="policyEdit.genre"
            class="form-control"
            id="policyGenre"
            v-validate.initial="'required'"
            name="genre"
          >
            <option>admin</option>
            <option>authz</option>
          </select>
        </div>
        <ul>
          <li v-for="error in errors.all()" :key="error.id">{{ error }}</li>
        </ul>
        <button type="button" class="btn btn-secondary" @click="edit = false">Cancel</button>
        <span>&nbsp;</span>
        <button
          type="button"
          :disabled="errors.any()"
          class="btn btn-primary"
          @click="updatePolicy()"
        >Update</button>
      </form>
    </template>
    <template v-else>
      <h3 class="list-group-item-heading inline " data-toggle="tooltip" data-placement="top" title="Tooltip on top">{{ policy.name }}</h3>
      <div class="pull-right">
        <button
          type="button"
          class="fa fa-trash btn-dark btn-sm"
          title="Remove Policy"
          @click="removePolicy()"
        ></button>
        <button
          type="button"
          class="fa fa-edit btn-dark btn-sm"
          title="Edit Policy"
          @click="updatingPolicy()"
        ></button>
      </div>
      <p class="list-group-item-text">{{ policy.description }}</p>

        <Category :policy="policy" :data="policy.subjectData" name="Subject" ></Category>
        <Category :policy="policy" :data="policy.objectData" name="Object" ></Category>
        <Category :policy="policy" :data="policy.actionData" name="Action" ></Category>
    </template>
    <hr />
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";
import util from "./../../services/Util.service.js";
import Category from "./Category";

export default {
  props: {
    policy: Object
  },
  data() {
    return {
      filter: "",
      edit: false,
      policyEdit: {},
      assignments: []
    };
  },
  computed: {

  },
  components: {
    Category
  },
  methods: {

    removePolicy() {
      if (
        confirm(
          "Are you sure to delete this Policy? (Associated perimeter, data an PDP will be deleted too)"
        )
      )
        PolicyService.removePolicy(this.policy);
    },
    updatingPolicy() {
      this.policyEdit = util.clone(this.policy);
      this.edit = true;
    },
    updatePolicy() {
      this.edit = false;
      PolicyService.updatePolicy(this.policyEdit);
    },
    showAssignments(data){
      this.assignments = this.policy[data];
    }
  }
};
</script>