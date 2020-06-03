<template>
  <div>
    <hr>
      <h4>Select policy:</h4>
      <form data-vv-scope="select">
        <div class="form-group">
          <select v-model="selectedPolicyId" v-validate.initial="'required'">
            <option disabled value>Please select one</option>
            <option
              v-for="policy in policies"
              :value="policy.id"
              :key="policy.id"
            >{{policy.name}}</option>
          </select>
        </div>
        <button type="button" class="btn btn-secondary" @click="close()">Cancel</button>
        <span>&nbsp;</span>
        <button
          type="button"
          :disabled="errors.any('select')"
          class="btn btn-primary"
          @click="updatePolicy()"
        >Update</button>
      </form>
      <br>
      <br>
  </div>
</template>

<script>
import PdpService from "./../../services/Pdp.service.js";
import util from "./../../services/Util.service.js";

export default {
  name: "updatePolicy",
  data: function() {
    return {
      selectedPolicyId: null,
    };
  },
  props: {
    pdp: Object
  },
  methods: {
    updatePolicy() {
      var policy = PdpService.getPolicy(this.selectedPolicyId);
      var pdpCopy = util.clone(this.pdp);
      pdpCopy.security_pipeline = [policy];
      PdpService.updatePdp(pdpCopy);
      this.close();
    },
    close() {
      this.$emit("close");
    }
  },
  computed: {
    policies() {
      return PdpService.policies.filter(
        el => !this.pdp.security_pipeline.includes(el)
      );
    }
  }
};
</script>
