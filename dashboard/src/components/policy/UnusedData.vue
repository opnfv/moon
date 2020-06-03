<template>
  <div>
    <div
      v-if="policy.unusedSubjectData.length  
            || policy.unusedObjectData.length
            || policy.unusedActionData.length"
      class="alert alert-dismissable alert-warning"
    >
      <button type="button" class="close" data-dismiss="alert" @click="showUnused = false; $emit('close')">×</button>
      <h4>Warning!</h4>
      <p>
        Some data are unused, please check them and delete them if necessary.
        <a
          href
          @click.prevent="showUnused = true"
          v-show="!showUnused"
        >Show unused data</a>
        <a href @click.prevent="showUnused = false" v-show="showUnused">Hide unused data</a>
      </p>
    </div>

    <div v-if="showUnused" class="row overflow-hidden mb-3">
      <div class="list-group col" v-if="policy.unusedSubjectData.length">
        <h3 class="list-group-item active">Unused Subject data</h3>
        <div v-for="subject in policy.unusedSubjectData" :key="subject.id" class="list-group-item">
          <h4 class="list-group-item-heading inline" :title="subject.description">{{ subject.name }}</h4>
          <button
            type="button"
            class="fa fa-trash pull-right btn-dark btn-sm"
            @click="removeData('subject', policy, subject)"
            title="Remove Subject data"
          ></button>
        </div>
      </div>

      <div class="list-group col" v-if="policy.unusedObjectData.length">
        <h3 class="list-group-item active">Unused Object data</h3>
        <div v-for="object in policy.unusedObjectData" :key="object.id" class="list-group-item">
          <h4 class="list-group-item-heading inline" :title="object.description">{{ object.name }}</h4>
          <button
            type="button"
            class="fa fa-trash pull-right btn-dark btn-sm"
            @click="removeData('object', policy, object)"
            title="Remove Object data"
          ></button>
        </div>
      </div>

      <div class="list-group col" v-if="policy.unusedActionData.length">
        <h3 class="list-group-item active">Unused Action data</h3>
        <div v-for="action in policy.unusedActionData" :key="action.id" class="list-group-item">
          <h4 class="list-group-item-heading inline" :title="action.description">{{ action.name }}</h4>
          <button
            type="button"
            class="fa fa-trash pull-right btn-dark btn-sm"
            @click="removeData('action', policy, action)"
            title="Remove Action data"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";


export default {
  props: {
    policy: Object
  },
  data() {
    return {
      showUnused: false
    };
  },
  methods: {
    removeData(type, policy, data) {
      if (
        confirm(
          "Are you sure to delete this Data? (Associated assignments and rules will be deleted too)"
        )
      )
        PolicyService.removeData(type, policy, data);
    }
  }
};
</script>