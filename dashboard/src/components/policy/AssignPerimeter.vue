<template>
  <div >
    <div v-if="selectedData && loading" class="row padding-10">
      <h4>Loading...</h4>
    </div>
    <div v-if="selectedData && !loading">
      <div class="p-2">
        <h3>Assign perimeters to {{ selectedData.name }}</h3>
        <form-header
          placeholder="Filter"
          buttonText="Create Perimeter"
          @click="creatingPerimeter = true"
          v-model="filterPerimeter"
          need-button
        ></form-header>
      </div>
      <create-perimeter
        v-if="creatingPerimeter"
        :policy="policy"
        :type="selectedDataType"
        @close="creatingPerimeter = false"
        @perimeterCreated="createPerimeter"
      ></create-perimeter>
      <div class="row mt-3" v-else>
        <div class="col-sm">
          <h4>
            All perimeters
            <i class="fa fa-question-circle" style="margin-left: 2%" v-if="assignPerimeterHelpStrings.allPerimeters" data-toggle="tooltip"  :title="assignPerimeterHelpStrings.allPerimeters"></i>
          </h4>
          <div class="w-100 height-200 scroll list-group border">
            <button
              class="list-group-item"
              v-for="perimeter in allPerimetersFiltered"
              :title="perimeter.description"
              :key="perimeter.id"
              @click="addPerimeter(perimeter)"
            >{{ perimeter.name }}</button>
          </div>
          <p>Click to add</p>
        </div>
        <div class="col-sm">
          <h4>
            Policy perimeters
            <i class="fa fa-question-circle" style="margin-left: 2%" v-if="assignPerimeterHelpStrings.policyPerimeters" data-toggle="tooltip"  :title="assignPerimeterHelpStrings.policyPerimeters"></i>
          </h4>
          <div class="w-100 height-200 scroll list-group list-group-flush border">
            <div
              @click="assign(perimeter)"
              class="list-group-item"
              :key="perimeter.id"
              v-for="perimeter in perimetersFiltered"
            >
              <span :title="perimeter.description">{{ perimeter.name }}</span>
              <button
                type="button"
                class="fa fa-trash pull-right btn-dark btn-sm"
                @click.stop="removePerimeterFromPolicy(perimeter)"
                title="Remove Perimeter"
              ></button>
            </div>
          </div>
          <p>Click to assign</p>
        </div>
        <div class="col-sm">
          <h4>
            Assigned perimeters
            <i class="fa fa-question-circle" style="margin-left: 2%" v-if="assignPerimeterHelpStrings.assignedPerimeters" data-toggle="tooltip"  :title="assignPerimeterHelpStrings.assignedPerimeters"></i>
          </h4>
          <div class="w-100 list-group border height-200 scroll">
            <button
              class="list-group-item"
              :key="perimeter.id"
              v-for="perimeter in assignmentsFiltered"
              :title="perimeter.description"
              @click="unassign(perimeter)"
            >{{ perimeter.name }}</button>
          </div>
          <p>Click to unassign</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PolicyService from "./../../services/Policy.service.js";
import util from "./../../services/Util.service.js";
import FormHeader from "./../FormHeader.vue";
import CreatePerimeter from "./CreatePerimeter.vue";
import helpstrings from "../../helpstrings";

var categoryMap = {
  subject: {
    perimeterId: "subject_id"
  },
  object: {
    perimeterId: "object_id"
  },
  action: {
    perimeterId: "action_id"
  }
};

export default {
  props: {
    dataToAssign: Object,
    policy: Object
  },
  components: {
    FormHeader,
    CreatePerimeter
  },
  data() {
    return {
      selectedData: null,
      selectedDataType: "",
      loading: false,
      perimeters: [],
      allPerimeters: [],
      assignments: [],
      filterPerimeter: "",
      creatingPerimeter: false,
      assignPerimeterHelpStrings: {}
    };
  },
  mounted() {
    this.assignPerimeterHelpStrings = helpstrings.assignPerimeter;
  },
  computed: {
    allPerimetersFiltered() {
      return util.filterAndSortByName(this.allPerimeters, this.filterPerimeter);
    },
    perimetersFiltered() {
      return util.filterAndSortByName(this.perimeters, this.filterPerimeter);
    },
    assignmentsFiltered() {
      return util.filterAndSortByName(this.assignments, this.filterPerimeter);
    }
  },
  watch: {
    dataToAssign() {
      this.selectedData = this.dataToAssign.selectedData;
      this.selectedDataType = this.dataToAssign.selectedDataType;
      if (this.selectedData) {
        this.loadPerimeter();
      }
    }
  },
  methods: {
    createPerimeter(perimeters) {
      util.pushAll(this.perimeters, perimeters);
    },
    addPerimeter(perimeter) {
      var self = this;
      PolicyService.addPerimeterToPolicy(
        self.selectedDataType,
        self.policy,
        perimeter
      ).then(function() {
        self.allPerimeters.splice(self.allPerimeters.indexOf(perimeter), 1);
        self.perimeters.push(perimeter);
      });
    },
    assign(perimeter) {
      var self = this;
      PolicyService.createAssignment(
        self.selectedDataType,
        self.policy,
        perimeter,
        self.selectedData
      ).then(function() {
        self.assignments.push(perimeter);
        self.perimeters.splice(self.perimeters.indexOf(perimeter), 1);
      });
    },
    unassign(perimeter) {
      var self = this;
      PolicyService.removeAssignment(
        self.selectedDataType,
        self.policy,
        perimeter,
        self.selectedData
      ).then(function() {
        self.perimeters.push(perimeter);
        self.assignments.splice(self.assignments.indexOf(perimeter), 1);
      });
    },
    removePerimeterFromPolicy(perimeter) {
      if (
        confirm(
          "Are you sure to delete this Perimeter? (Associated assignments will be deleted too)"
        )
      ) {
        var self = this;
        PolicyService.removePerimeterFromPolicy(
          self.selectedDataType,
          self.policy,
          perimeter
        ).then(function() {
          self.perimeters.splice(self.perimeters.indexOf(perimeter), 1);
          perimeter.policy_list.splice(
            perimeter.policy_list.indexOf(self.policy.id),
            1
          );
          if (perimeter.policy_list.length > 0) {
            self.allPerimeters.push(perimeter);
          }
        });
      }
    },
    loadPerimeter() {
      var self = this;
      self.loading = true;
      self.perimeters = [];
      self.allPerimeters = [];
      self.assignments = [];

      PolicyService.loadPerimetersAndAssignments(
        self.selectedDataType,
        self.policy
      ).then(function(values) {
        var category = categoryMap[self.selectedDataType];
        self.loading = false;
        self.perimeters = values.perimeters;
        var index, perimeter;
        for (index = 0; index < values.allPerimeters.length; index++) {
          perimeter = values.allPerimeters[index];
          if (perimeter.policy_list.indexOf(self.policy.id) < 0) {
            self.allPerimeters.push(perimeter);
          }
        }
        for (index = 0; index < values.assignments.length; index++) {
          var assignment = values.assignments[index];
          if (assignment.assignments.indexOf(self.selectedData.id) >= 0) {
            perimeter = values.perimetersMap[assignment[category.perimeterId]];
            self.assignments.push(perimeter);
            self.perimeters.splice(self.perimeters.indexOf(perimeter), 1);
          }
        }
      });
    }
  }
};
</script>