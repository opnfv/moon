<template>
  <div class="">
    <template v-if="edit">
      <form>
        <div class="form-group">
          <label for="metaruleName">Name</label>
          <input
            type="text"
            name="name"
            v-model="metaruleEdit.name"
            v-validate="'alpha_dash|required|min:3'"
            class="form-control"
            id="metaruleName"
          >
        </div>
        <div class="form-group">
          <label for="modelDescription">Description</label>
          <textarea
            name="description"
            v-model="metaruleEdit.description"
            v-validate="'required|min:3'"
            class="form-control"
          ></textarea>
        </div>
        <ul>
          <li v-for="error in errors.all()" :key="error.id">{{ error }}</li>
        </ul>
        <button type="button" class="btn btn-secondary" @click="edit = false">Cancel</button>
        <span>&nbsp;</span>
        <button type="button" :disabled="errors.any()" class="btn btn-primary" @click="updateMetarule()">Update</button>
      </form>
    </template>
    <template v-else>
      <h3 class="list-group-item-heading inline">{{ metarule.name }}</h3>
      <div class="pull-right">
        <button
          type="button"
          class="fa fa-trash btn btn-dark btn-sm"
          @click="removeMetarule()"
          title="Remove Meta Rule"
        ></button>
        <button
          type="button"
          class="fa fa-edit btn btn-dark btn-sm"
          @click="updatingMetarule()"
          title="Edit Meta Rule"
        ></button>
      </div>
      <p class="list-group-item-text">{{ metarule.description }}</p>
      <p class="list-group-item-text"></p>
      <table class="table categories">
        <thead>
          <tr>
            <th>
              <span>Subjects</span>
              <i class="fa fa-question-circle" style="margin-left: 2%" v-if="metaruleHelpStrings.subject" data-toggle="tooltip"  :title="metaruleHelpStrings.subject"></i>
              <button
                type="button"
                class="fa fa-plus pull-right btn btn-dark btn-sm"
                @click="addSubjectCategory = true"
                title="Add Subject"
              ></button>
            </th>
            <th>
              <span>Objects</span>
              <i class="fa fa-question-circle" style="margin-left: 2%" v-if="metaruleHelpStrings.object" data-toggle="tooltip"  :title="metaruleHelpStrings.object"></i>
              <button
                type="button"
                class="fa fa-plus pull-right btn btn-dark btn-sm"
                @click="addObjectCategory = true"
                title="Add Object"
              ></button>
            </th>
            <th>
              <span>Actions</span>
              <i class="fa fa-question-circle" style="margin-left: 2%" v-if="metaruleHelpStrings.action" data-toggle="tooltip"  :title="metaruleHelpStrings.action"></i>
              <button
                type="button"
                class="fa fa-plus pull-right btn btn-dark btn-sm"
                @click="addActionCategory = true"
                title="Add Action"
              ></button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <AddCategory v-if="addSubjectCategory" :metarule="metarule" type="subject" @close="addSubjectCategory = false"></AddCategory>
              <Category v-else v-for="category in metarule.subject_categories" :key="category.id" :category="category" :metarule="metarule" :attributes="metarule.subjectAttributes" type="subject"></Category>
            </td>
            <td>
              <AddCategory v-if="addObjectCategory" :metarule="metarule" type="object" @close="addObjectCategory = false"></AddCategory>
              <Category v-else v-for="category in metarule.object_categories" :key="category.id" :category="category" :metarule="metarule" :attributes="metarule.objectAttributes" type="object"></Category>
            </td>
            <td>
              <AddCategory v-if="addActionCategory" :metarule="metarule" type="action" @close="addActionCategory = false"></AddCategory>
              <Category v-else v-for="category in metarule.action_categories" :key="category.id" :category="category" :metarule="metarule" :attributes="metarule.actionAttributes" type="action"></Category>
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </div>
</template>

<script>
import Category from './Category.vue'
import AddCategory from './AddCategory.vue'
import ModelService from "./../../services/Model.service.js";
import util from "./../../services/Util.service.js";
import helpstrings from "../../helpstrings";

export default {
  name: "metarule",
  data: function() {
    return {
      edit: false,
      metaruleEdit: {},
      addSubjectCategory: false,
      addObjectCategory: false,
      addActionCategory: false,
      metaruleHelpStrings: {}
    };
  },
  components: {
    Category, 
    AddCategory
  },
  props: {
    metarule: Object,
    model: Object,
  },
  mounted() {
    this.metaruleHelpStrings = helpstrings.metarule;
  },
  methods: {
    updatingMetarule() {
      this.metaruleEdit = util.clone(this.metarule);
      this.edit = true;
    },
    updateMetarule() {
      this.edit = false;
      ModelService.updateMetaRule(this.metaruleEdit);
    },
    removeMetarule() {
      if (confirm('Are you sure to remove this Meta Rule from model?')) {
        var modelCopy = util.clone(this.model);
        modelCopy.meta_rules.splice(modelCopy.meta_rules.indexOf(this.metarule), 1);
        ModelService.updateModel(modelCopy);
      }
    }
  }
};
</script>
