<template>
  <div>
    <span :title="category.description">{{ category.name }}</span>
    <button type="button" class="fa fa-trash pull-right btn btn-dark btn-sm" @click="removeCategory()" title="Remove"></button>
    <div  v-for="attribute in attributes" :key="attribute.id">
      <b>attributes: </b> {{attribute.id}}
    </div>
  </div>
</template>

<script>
import ModelService from "./../../services/Model.service.js";
import util from "./../../services/Util.service.js";

var categoryMap = {
  subject: {
    addTitle: "Add Subject Category",
    removeTitleFromMetaRule:
      "Are you sure to remove from meta rule this Subject Category?",
    removeTitle: "Are you sure to remove this Subject Category?",
    listName: "subject_categories",
    serviceListName: "subjectCategories"
  },
  object: {
    addTitle: "Add Object Category",
    removeTitleFromMetaRule:
      "Are you sure to remove from meta rule this Object Category?",
    removeTitle: "Are you sure to remove this Object Category?",
    listName: "object_categories",
    serviceListName: "objectCategories"
  },
  action: {
    addTitle: "Add Action Category",
    removeTitleFromMetaRule:
      "Are you sure to remove from meta rule this Action Category?",
    removeTitle: "Are you sure to remove this Action Category?",
    listName: "action_categories",
    serviceListName: "actionCategories"
  }
};

export default {
  name: "category",
  props: {
    metarule: Object,
    category: Object,
    attributes: Array,
    type: String
  },
  methods: {
    removeCategory() {
      var typeValue = categoryMap[this.type];
      if (confirm(typeValue.removeTitleFromMetaRule)) {
        var metaruleCopy = util.clone(this.metarule);
        metaruleCopy[typeValue.listName].splice(
          metaruleCopy[typeValue.listName].indexOf(this.category),
          1
        );
        ModelService.updateMetaRule(metaruleCopy);
      }
    }
  }
};
</script>
