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
      <h3 class="list-group-item-heading inline " >{{ policy.name }}</h3>
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

      <unused-data :policy="policy" v-if="showAlert"  @close="allowAlert = false"></unused-data>

      <details class="list-group-item-text">
        <summary @click="populatePolicy()">
          <h4 class="inline-block width-200">
            Rules
            <i class="fa fa-question-circle" style="margin-left: 2%" v-if="policyHelpStrings.rules" data-toggle="tooltip"  :title="policyHelpStrings.rules"></i>
          </h4>
          <button
            type="button"
            class="fa fa-plus btn-dark btn-sm"
            @click="creatingRule = true"
            title="Add Rule"
          ></button>
        </summary>
        <create-rule v-if="creatingRule" @close="creatingRule = false" :policy="policy"></create-rule>
        <div class="list-group" v-else>
          <filter-rules  v-model="filter" ></filter-rules>
          <br/>
          <p v-if="!policy.rulesPopulated" class="list-group-item-text">Loading rules...</p>
          <div v-else>
            <rule
              v-for="rule in filteredRules"
              :key="rule.id"
              :rule="rule"
              :selected="selectedRule == rule"
              :policy="policy"
              @show="selectRule($event)"
            ></rule>
          </div>
        </div>
      </details>
    </template>
    <hr />
  </div>
</template>

<script>
import UnusedData from "./UnusedData.vue";
import PolicyService from "./../../services/Policy.service.js";
import util from "./../../services/Util.service.js";
import Rule from "./Rule.vue";
import CreateRule from "./CreateRule.vue";
import FilterRules from "./FilterRules.vue";

import Vue from "vue";
import helpstrings from "../../helpstrings";

var selectedRule = new Vue({data: {rule: null}});

export default {
  props: {
    policy: Object
  },
  data() {
    return {
      filter: "",
      edit: false,
      creatingRule: false,
      allowAlert: true,
      policyEdit: {},
      policyHelpStrings: {}
    };
  },
  mounted() {
    this.policyHelpStrings = helpstrings.policy;
  },
  computed: {
    filteredRules() {
      let filteredRules = PolicyService.filterByRules(this.policy.rules, this.filter);


      return filteredRules;
    },
    selectedRule() {
      return selectedRule.rule;
    },
    showAlert() {
      return (
        this.allowAlert &&
        (this.policy.unusedSubjectData.length ||
          this.policy.unusedObjectData.length ||
          this.policy.unusedActionData.length)
      );
    },
  },
  components: {
    UnusedData,
    Rule,
    CreateRule,
    FilterRules
  },
  methods: {
    populatePolicy() {
      PolicyService.populatePolicy(this.policy);
    },
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
    selectRule(rule) {
      selectedRule.rule = rule;
    }
  }
};
</script>