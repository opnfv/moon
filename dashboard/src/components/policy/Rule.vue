<template>
  <div class="list-group-item">
    <details >
        <summary class="list-group-item-heading" :style="ruleIsGrant ? 'background-color: var(--green)' : 'background-color: Tomato'" >

        <b>Rule: </b>
        <data-list :list="rule.subjectData"></data-list> |
        <data-list :list="rule.actionData"></data-list> |
        <data-list :list="rule.objectData"></data-list>
        <span v-if="rule.attributeData.length"> | <data-list :list="rule.attributeData"></data-list></span>
        <div class="pull-right" style="background-color: white">
          <button
                type="button"
                class="fa fa-trash pull-right btn-dark btn-sm"
                @click="removeRuleFromPolicy()"
                title="Remove Rule"
          ></button>
          <button type="button"
                  :class="ruleIsGrant ? buttonRuleIsGrant : buttonRuleIsDeny"
                  @click="changeRuleDecision()"
                  title="Change Decision"
          ></button>
        </div>
      </summary>
      <div  >
        <p class="list-group-item-text"></p>
        <table class="table">
          <thead>
          <tr>
            <th>
              <span>
                Subjects data 
                <i class="fa fa-question-circle" v-if="ruleHelpStrings.subjectsData" data-toggle="tooltip"  :title="ruleHelpStrings.subjectsData"></i>
              </span>
            </th>
            <th>
              <span>
                Objects data
                <i class="fa fa-question-circle" v-if="ruleHelpStrings.objectsData" data-toggle="tooltip"  :title="ruleHelpStrings.objectsData"></i>
              </span>
            </th>
            <th>
              <span>
                Actions data
                <i class="fa fa-question-circle" v-if="ruleHelpStrings.actionsData" data-toggle="tooltip"  :title="ruleHelpStrings.actionsData"></i>
              </span>
            </th>
            <th v-if="rule.attributeData.length">
              <span>
                Attributes
                <i class="fa fa-question-circle" v-if="ruleHelpStrings.attributes" data-toggle="tooltip"  :title="ruleHelpStrings.attributes"></i>
              </span>
            </th>
            <th>
              <span>
                Instructions
                <i class="fa fa-question-circle" v-if="ruleHelpStrings.instructions" data-toggle="tooltip"  :title="ruleHelpStrings.instructions"></i>
              </span>
            </th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>
              <p
                      v-for="data in rule.subjectData"
                      :key="data.id"
                      :class="{'selected-data': selectedData == data}"
              >
                <span :title="data.description">{{ data.name }}</span>
                <button
                        v-if="selectedData != data"
                        type="button"
                        class="fa fa-exchange pull-right btn-dark btn-sm"
                        @click="assignData('subject', data)"
                        title="Assign to perimeters"
                ></button>
                <button
                        v-if="selectedData == data"
                        type="button"
                        class="fa fa-times pull-right btn-dark btn-sm"
                        @click="unassignData()"
                        title="Close"
                ></button>
              </p>
            </td>
            <td>
              <p
                      v-for="data in rule.objectData"
                      :key="data.id"
                      :class="{'selected-data': selectedData == data}"
              >
                <span :title="data.description">{{ data.name }}</span>
                <button
                        v-if="selectedData != data"
                        type="button"
                        class="fa fa-exchange pull-right btn-dark btn-sm"
                        @click="assignData('object', data)"
                        title="Assign to perimeters"
                ></button>
                <button
                        v-if="selectedData == data"
                        type="button"
                        class="fa fa-times pull-right btn-dark btn-sm"
                        @click="unassignData()"
                        title="Close"
                ></button>
              </p>
            </td>
            <td>
              <p
                      v-for="data in rule.actionData"
                      :key="data.id"
                      :class="{'selected-data': selectedData == data}"
              >
                <span :title="data.description">{{ data.name }}</span>
                <button
                        v-if="selectedData != data"
                        type="button"
                        class="fa fa-exchange pull-right btn-dark btn-sm"
                        @click="assignData('action', data)"
                        title="Assign to perimeters"
                ></button>
                <button
                        v-if="selectedData == data"
                        type="button"
                        class="fa fa-times pull-right btn-dark btn-sm"
                        @click="unassignData()"
                        title="Close"
                ></button>
              </p>
            </td>
            <td v-if="rule.attributeData.length">
              <p
                      v-for="data in rule.attributeData"
                      :key="data.id"
                      :class="{'selected-data': selectedData == data}"
              >
                <span :title="data.description">{{data.id}} : {{ data.name }}</span>
              </p>
            </td>
            <td>
              <pre><code>{{rule.instructions}}</code></pre>
            </td>
          </tr>
          </tbody>
        </table>
        <assign-perimeter :policy="policy" :dataToAssign="dataToAssign"></assign-perimeter>

      </div>
    </details>
  </div>
</template>

<script>
  import AttributeService from "./../../services/Attribute.service"
  import PolicyService from "./../../services/Policy.service.js";
  import DataList from "./DataList.vue";
  import AssignPerimeter from "./AssignPerimeter.vue";
  import helpstrings from "../../helpstrings";

  export default {
    props: {
      rule: Object,
      selected: Boolean,
      policy: Object
    },
    data() {
      return {
        dataToAssign: {
          selectedData: null,
          selectedDataType: "",
        },
        selectedData: null,
        ruleIsGrant: false,
        buttonRuleIsGrant: 'fa fa-toggle-on pull-right btn-dark btn-sm',
        buttonRuleIsDeny: 'fa fa-toggle-off pull-right btn-dark btn-sm',
        ruleHelpStrings: {}

      }
    },
    components: {
      DataList,
      AssignPerimeter,
    },
    created() {
      AttributeService.initialize();
    },
    mounted() {
        this.ruleIsGrant = ("grant".localeCompare(this.rule.instructions[0].decision) == 0);
        this.ruleHelpStrings = helpstrings.rule;
    },
    watch: {
      selected() {
        if (!this.selected)
          this.unassignData();
      }
    },
    methods: {
      changeRuleDecision() {
        var decision = ("grant".localeCompare(this.rule.instructions[0].decision) == 0) ? "deny" : "grant";
        PolicyService.updateRule(this.policy, this.rule, decision).then(res => {
            this.ruleIsGrant = !this.ruleIsGrant;
            this.rule.instructions = res;
        });

      },
      showRule() {
        this.$emit("show", this.selected ? null : this.rule);
      },
      removeRuleFromPolicy() {
        if (confirm("Are you sure to delete this Rule?"))
          PolicyService.removeRuleFromPolicy(this.policy, this.rule);
      },
      assignData(type, data) {
        this.dataToAssign = {
          selectedData: data,
          selectedDataType: type,
        };
        this.selectedData = data;
      },
      unassignData() {
        this.assignData("", null);
      }
    }
  };
</script>

<style scoped>

</style>