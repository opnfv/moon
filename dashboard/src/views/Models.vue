<template>
  <div>
    <orphans
      @close="allowAlert = false"
      v-if="showAlert"
      :orphanMetaRules="orphanMetaRules"
      :orphanSubjectCategories="orphanSubjectCategories"
      :orphanObjectCategories="orphanObjectCategories"
      :orphanActionCategories="orphanActionCategories"
    ></orphans>

    <br />
    <form-header
      placeholder="Filter"
      buttonText="Create Model"
      @click="creatingModel = true"
      v-model="filter"
      need-button
    ></form-header>
    <br />

    <CreateModel v-if="creatingModel" @close="creatingModel = false"></CreateModel>
    <div class="list-group row" v-else>
      <Model v-for="model in filteredModels" :key="model.id" :model="model"></Model>
    </div>
  </div>
</template>

<script>
import Model from "./../components/model/Model.vue";
import CreateModel from "./../components/model/CreateModel.vue";
import ModelService from "./../services/Model.service.js";
import util from "./../services/Util.service.js";
import Orphans from "./../components/model/Orphans.vue";
import FormHeader from "./../components/FormHeader.vue";

export default {
  name: "models",
  components: {
    Model,
    CreateModel,
    FormHeader,
    Orphans
  },
  mounted() {
    ModelService.initialize();
    this.models = ModelService.models;
    this.orphanMetaRules = ModelService.orphanMetaRules;
    this.orphanSubjectCategories = ModelService.orphanSubjectCategories;
    this.orphanObjectCategories = ModelService.orphanObjectCategories;
    this.orphanActionCategories = ModelService.orphanActionCategories;
  },
  data() {
    return {
      filter: "",
      creatingModel: false,
      allowAlert: true,
      orphanMetaRules: [],
      orphanSubjectCategories: [],
      orphanActionCategories: [],
      orphanObjectCategories: [],
      models: []
    };
  },
  computed: {
    showAlert() {
      return (
        this.allowAlert &&
        (this.orphanMetaRules.length ||
          this.orphanSubjectCategories.length ||
          this.orphanActionCategories.length ||
          this.orphanObjectCategories.length)
      );
    },
    filteredModels() {
      return util.filterAndSortByName(this.models, this.filter);
    }
  }
};
</script>
