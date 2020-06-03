<template>
  <div class="list-group-item row">
    <form v-if="!metaruleId">
      <div class="form-group">
        <label for="metarule">Select a Metarule:</label>
        <select v-model="metaruleId" class="form-control" id="metarule" name="metarule">
          <option
            v-for="metarule in policy.model.meta_rules"
            :key="metarule.id"
            :value="metarule.id"
          >{{ metarule.name }}</option>
        </select>
      </div>
      <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
    </form>
    <form v-else>
      <div
        class="form-group"
        v-for="(categoryWrapper, index) in ruleData"
        :key="categoryWrapper.id"
      >
        <label
          :for="categoryWrapper.category.name"
        >{{ 'Select ' + categoryWrapper.type + ' data of ' + categoryWrapper.category.name + ' category' }}</label>
        <select
          v-model="ruleCreate.rule[index]"
          class="form-control"
          :id="categoryWrapper.category.name"
          :name="categoryWrapper.category.name"
          v-validate.initial="'required'"
        >
          <option
            v-for="data in categoryWrapper.data"
            :key="data.id"
            :value="data.id"
          >{{ data.name }}</option>
        </select>
        <create-data
          class="m-3"
          @close="creatingDataCategory = null"
          @dataCreated="dataCreated(categoryWrapper, $event, index)"
          :policy="policy"
          :type="categoryWrapper.type"
          :category="categoryWrapper.category"
          v-if="creatingDataCategory == categoryWrapper.category"
        ></create-data>
        <button
          v-else
          type="button"
          class="btn btn-primary mt-3"
          @click="creatingDataCategory = categoryWrapper.category"
        >Or Create one</button>
      </div>
      <div  v-for='(attribute, index) in policy.attributes' :key="attribute.id" class="form-group">
        <label for="ruleAttributes">Attribute {{attribute.id}}</label>
        <select
                v-model="attributes[index]"
                class="form-control"
                v-validate.initial="'required'"
        >
          <option
                  v-for="value in attribute.values"
                  :key="value"
                  :value="value"
          >{{ value }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="ruleInstructions">Instructions</label>
        <select
                v-model="ruleCreate.instructions"
                class="form-control"
                v-validate.initial="'required'"
        >
          <option
                  v-for="data in instructions"
                  :key="data"
                  :value="data"
          >{{ data }}</option>
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
        @click="createRule()"
      >Create</button>
    </form>
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";
import ModelService from "./../../services/Model.service.js";
import CreateData from "./CreateData.vue";

function addCategories(type, categories, data, mapArray, initArray) {
  var dataFiltered = [];

  for (var i = 0; i < categories.length; i++) {
    var category = categories[i];
    for (var j = 0; j < data.length; j++) {
      var element = data[j];
      if (element.category_id == category.id) {
        dataFiltered.push(element);
      }
    }

    mapArray.push({
      id: category.id,
      category: category,
      data: dataFiltered,
      type: type
    });
    initArray.push(dataFiltered.length > 0 ? dataFiltered[0].id : null);
  }
}


export default {
  name: "createRule",
  props: {
    policy: Object
  },
  components: {
    CreateData
  },
  data: function() {
    return {
      metarule: null,
      metaruleId: null,
      creatingDataCategory: null,
      ruleData: [],
      ruleCreate: {
        instructions: 'grant',
        rule: [],
      },
      instructions: ['grant', 'deny'],
      attributes: [],
      attribute: '',
    };
  },
  watch: {
    policy() {
      if (this.policy) {
        this.metaruleId = null;
        if (this.policy.model.meta_rules.length == 1) {
          this.metaruleId = this.policy.model.meta_rules[0].id;
        }
      }
    },
    metaruleId() {
      if (this.metaruleId) {
        this.metarule = ModelService.getMetaRule(this.metaruleId);
        if (this.metarule){
          for (let i = 0; i < this.policy.attributes.length; i++){
            let attrs = this.policy.attributes[i].default;
            this.attributes.push(attrs);
          }
        }
        addCategories(
          "subject",
          this.metarule.subject_categories,
          this.policy.subjectData,
          this.ruleData,
          this.ruleCreate.rule
        );
        addCategories(
          "object",
          this.metarule.object_categories,
          this.policy.objectData,
          this.ruleData,
          this.ruleCreate.rule
        );
        addCategories(
          "action",
          this.metarule.action_categories,
          this.policy.actionData,
          this.ruleData,
          this.ruleCreate.rule
        );
      }
    }
  },
  methods: {
    createRule() {
      this.ruleCreate.enabled =  true;
      const instruction = "[{\n\t\"decision\": " + "\"" + this.ruleCreate.instructions + "\"" + "\n}]";
      this.ruleCreate.instructions = JSON.parse(instruction);
      this.ruleCreate.meta_rule_id = this.metarule.id;
      this.ruleCreate.policy_id = this.policy.id;
      for (let i = 0; i < this.attributes.length; i++) {
        this.ruleCreate.rule.push("attributes:" + this.attributes[i]);
      }

      PolicyService.addRuleToPolicy(this.policy, this.ruleCreate);
      this.close();
    },
    dataCreated(wrapper, data, index) {
      wrapper.data.push(data);
      this.$set(this.ruleCreate.rule, index, data.id);
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>
