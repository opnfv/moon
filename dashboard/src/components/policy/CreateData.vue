<template>
  <div class="list-group-item row">
    <form>
      <div class="form-group">
        <label for="dataName">Name</label>
        <input
          type="text"
          name="name"
          v-model="dataCreate.name"
          v-validate.initial="'alpha_dash|required|min:3'"
          class="form-control"
          id="dataName"
        />
      </div>
      <div class="form-group">
        <label for="dataDescription">Description</label>
        <textarea
          name="description"
          v-model="dataCreate.description"
          v-validate.initial="'required|min:3'"
          class="form-control"
        ></textarea>
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
        @click="createData()"
      >Create</button>
    </form>
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";

export default {
  name: "createData",
  props: {
    policy: Object,
    type: String,
    category: Object,
  },
  data: function() {
    return {
      dataCreate: {
        name: "",
        description: ""
      }
    };
  },
  methods: {
    createData() {
      var self = this;
      PolicyService.createData(
        this.type,
        this.policy,
        this.category.id,
        this.dataCreate
      ).then(function(datas) {
        self.$emit("dataCreated", datas[0]);
        self.close();
      });
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>
