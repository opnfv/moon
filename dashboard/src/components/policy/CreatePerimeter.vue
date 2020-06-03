<template>
  <div class="list-group-item row">
    <form>
      <div class="form-group">
        <label for="perimeterName">Name</label>
        <input
          type="text"
          name="name"
          v-model="perimeterCreate.name"
          v-validate.initial="'alpha_dash|required|min:3'"
          class="form-control"
          id="perimeterName"
        />
      </div>
      <div class="form-group">
        <label for="perimeterDescription">Description</label>
        <textarea
          name="description"
          v-model="perimeterCreate.description"
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
        @click="createPerimeter()"
      >Create</button>
    </form>
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";

export default {
  name: "createPerimeter",
  props: {
    policy: Object,
    type: String
  },
  data: function() {
    return {
      perimeterCreate: {
        name: "",
        description: ""
      }
    };
  },
  methods: {
    createPerimeter() {
      var self = this;
      PolicyService.createPerimeter(
        this.type,
        this.policy,
        this.perimeterCreate
      ).then(function(perimeters) {
        self.$emit("perimeterCreated", perimeters);
        self.close();
      });
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>
