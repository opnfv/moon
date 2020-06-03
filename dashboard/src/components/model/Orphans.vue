<template>
  <div>
    <div class="alert alert-dismissable alert-warning">
      <button type="button" class="close" data-dismiss="alert" @click="showOrphan = false; $emit('close')">×</button>
      <h4>Warning!</h4>
      <p>
        Some metarules or categories are orphan, please check them and delete them if necessary.
        <a
          href
          @click.prevent="showOrphan = true"
          v-show="!showOrphan"
        >Show orphans</a>
        <a href @click.prevent="showOrphan = false" v-show="showOrphan">Hide orphans</a>
      </p>
    </div>

    <div class="row" v-show="showOrphan">
      <div class="list-group col-lg-3" v-if="orphanMetaRules.length">
        <h3 class="list-group-item active">Orphan Meta rules</h3>
        <div v-for="metaRule in orphanMetaRules" class="list-group-item" :key="metaRule.id">
          <h4 class="list-group-item-heading inline">{{ metaRule.name }}</h4>
          <button
            type="button"
            class="fa fa-trash pull-right btn btn-dark btn-sm"
            @click="removeMetarule(metaRule)"
            title="Remove Meta rule"
          ></button>
          <p class="list-group-item-text">{{ metaRule.description }}</p>
        </div>
      </div>

      <OrphanCategory
        v-if="orphanSubjectCategories.length"
        type="subject"
        :categories="orphanSubjectCategories"
      ></OrphanCategory>
      <OrphanCategory
        v-if="orphanObjectCategories.length"
        type="object"
        :categories="orphanObjectCategories"
      ></OrphanCategory>
      <OrphanCategory
        v-if="orphanActionCategories.length"
        type="action"
        :categories="orphanActionCategories"
      ></OrphanCategory>
    </div>
  </div>
</template>

<script>
import ModelService from "./../../services/Model.service.js";
import OrphanCategory from "./OrphanCategory.vue";

export default {
  props: {
    orphanMetaRules: Array,
    orphanSubjectCategories: Array,
    orphanObjectCategories: Array,
    orphanActionCategories: Array
  },
  components: {
      OrphanCategory,
  },
  data() {
    return {
      showOrphan: false,
      allowAlert: true
    };
  },
  methods: {
    removeMetarule(metarule) {
      if (confirm("Are you sure to remove this Meta Rule?")) {
        ModelService.removeMetaRule(metarule);
      }
    }
  }
};
</script>