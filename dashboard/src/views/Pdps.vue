<template>
  <div>
    <form-header
      placeholder="Filter"
      buttonText="Create PDP"
      @click="creatingPdp = true"
      v-model="filter"
      need-button
    ></form-header>
    <br />

    <CreatePdp v-if="creatingPdp" @close="creatingPdp = false"></CreatePdp>
    <div class="list-group row" v-else>
      <pdp v-for="pdp in filteredPdps" :key="pdp.id" :pdp="pdp"></pdp>
    </div>
  </div>
</template>

<script>
import PdpService from "./../services/Pdp.service.js";
import util from "./../services/Util.service.js";
import Pdp from "./../components/pdp/Pdp.vue";
import CreatePdp from "./../components/pdp/CreatePdp.vue";
import FormHeader from "./../components/FormHeader.vue";
import PolicyService from "../services/Policy.service";

export default {
  data() {
    return {
      filter: "",
      creatingPdp: false,
      pdps: []
    };
  },
  mounted() {
    PdpService.initialize();
    PolicyService.initialize();
    this.pdps = PdpService.pdps;
  },
  components: {
    Pdp,
    CreatePdp,
    FormHeader
  },
  computed: {
    filteredPdps() {
      return util.filterAndSortByName(this.pdps, this.filter);
    }
  }
};
</script>


