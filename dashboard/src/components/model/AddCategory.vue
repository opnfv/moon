<template>
  <div>
    <template v-if="categories.length > 0">
      <h4>Select category:</h4>
      <form data-vv-scope="select">
        <div class="form-group">
          <select v-model="selectedCategoryId" v-validate.initial="'required'">
            <option disabled value>Please select one</option>
            <option
              v-for="category in categories"
              :value="category.id"
              :key="category.id"
            >{{category.name}}</option>
          </select>
        </div>
        <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
        <span>&nbsp;</span>
        <button
          type="button"
          :disabled="errors.any('select')"
          class="btn btn-primary"
          @click="addCategory()"
        >Add</button>
      </form>
      <br>
      <br>
      <h4>Or create a new one:</h4>
    </template>
    <h4 v-else>Create a category:</h4>
    <form data-vv-scope="create">
      <div class="form-group">
        <label for="categoryName">Name</label>
        <input
          type="text"
          name="name"
          v-model="categoryCreate.name"
          v-validate.initial="'alpha_dash|required|min:3'"
          class="form-control"
          id="categoryName"
        >
      </div>
      <div class="form-group">
        <label for="modelDescription">Description</label>
        <textarea
          name="description"
          v-model="categoryCreate.description"
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
        @click="createCategory()"
      >Create</button>
    </form>
  </div>
</template>

<script>
import ModelService from "./../../services/Model.service.js";
import util from "./../../services/Util.service.js";

var categoryMap = {
  subject: {
    listName: "subject_categories",
    serviceListName: "subjectCategories"
  },
  object: {
    listName: "object_categories",
    serviceListName: "objectCategories"
  },
  action: {
    listName: "action_categories",
    serviceListName: "actionCategories"
  }
};

export default {
  name: "addCategory",
  data: function() {
    return {
      selectedCategoryId: null,
      categoryCreate: {
        name: "",
        description: ""
      }
    };
  },
  props: {
    metarule: Object,
    type: String
  },
  methods: {
    createCategory() {
      ModelService.createCategory(this.type, this.categoryCreate).then(category => {
        this.selectedCategoryId = category.id;
        this.addCategory();
      });
    },
    addCategory() {
      var category = ModelService.getCategory(this.type, this.selectedCategoryId);
      var metaRuleCopy = util.clone(this.metarule);
      metaRuleCopy[categoryMap[this.type].listName].push(category);
      ModelService.updateMetaRule(metaRuleCopy);
      this.close();
    },
    close() {
      this.$emit("close");
    }
  },
  computed: {
    categories() {
      return ModelService[categoryMap[this.type].serviceListName].filter(
        el => !this.metarule[categoryMap[this.type].listName].includes(el)
      );
    }
  }
};
</script>
