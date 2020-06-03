<template>
  <div class="list-group col-lg-3">
    <h3 class="list-group-item active">{{title}}</h3>
    <div v-for="category in categories" class="list-group-item" :key="category.id">
      <h4 class="list-group-item-heading inline">{{ category.name }}</h4>
      <button
        type="button"
        class="fa fa-trash pull-right btn btn-dark btn-sm"
        @click="removeCategory(category)"
        :title="buttonTitle"
      ></button>
      <p class="list-group-item-text">{{ category.description }}</p>
    </div>
  </div>
</template>

<script>
import ModelService from "./../../services/Model.service.js";

var categoryMap = {
  subject: {
    title: "Orphan Subject categories",
    removeButtonTitle: "Remove Subject category",
    removeTitle: "Are you sure to remove this Subject Category?",
    listName: "subject_categories",
    serviceListName: "subjectCategories"
  },
  object: {
    title: "Orphan Object categories",
    removeButtonTitle: "Remove Object category",
    removeTitle: "Are you sure to remove this Object Category?",
    listName: "object_categories",
    serviceListName: "objectCategories"
  },
  action: {
    title: "Orphan Action categories",
    removeButtonTitle: "Remove Action category",
    removeTitle: "Are you sure to remove this Action Category?",
    listName: "action_categories",
    serviceListName: "actionCategories"
  }
};

export default {
  props: {
    categories: Array,
    type: String
  },
  computed: {
    title() {
      return categoryMap[this.type].title;
    },
    buttonTitle() {
      return categoryMap[this.type].removeButtonTitle;
    }
  },
  methods: {
    removeCategory(category) {
      if (confirm(categoryMap[this.type].removeTitle)) {
        ModelService.removeCategory(this.type, category);
      }
    }
  }
};
</script>
