<template>
    <details class="list-group" >
        <summary @click="populatePolicy()">
            <h4 class="inline-block width-200">
                {{name}}
                <i class="fa fa-question-circle" style="margin-left: 2%" v-if="categoryHelpStrings[name.toLowerCase()]" data-toggle="tooltip"  :title="categoryHelpStrings[name.toLowerCase()]"></i>
            </h4>
        </summary>
        <div class="assignments-details">
            <FormHeader
                    :placeholder="placeholder"
                    v-model="filter"
                    needButton
                    :buttonText="buttonText"
                    @click="creatingData"
            ></FormHeader>
            <create-data
                    class="m-3"
                    @close="creatingDataOpen = false"
                    :policy="policy"
                    :type="name.toLowerCase()"
                    :categoryId="categoryId"
                    v-if="creatingDataOpen"
            ></create-data>
            <br/>
            <details class="list-group"  v-for="item in filteredData" :key="item.id">
                <summary @click="assignData(name.toLowerCase(), item)">
                    <h4 class="inline-block width-200">{{item.name}}</h4>
                </summary>
                <AssignPerimeter :policy="policy" :dataToAssign="dataToAssign"></AssignPerimeter>
            </details>
        </div>
    </details>
</template>

<script>
    import AssignPerimeter from "../policy/AssignPerimeter";
    import FormHeader from "../FormHeader";
    import CreateData from "./CreateData";
    import util from "../../services/Util.service";
    import PolicyService from "../../services/Policy.service";
    import helpstrings from "../../helpstrings";

    export default {
        props:{
            policy: Object,
            data: Array,
            name: String
        },
        name: "Assignment",
        components: {
            AssignPerimeter,
            FormHeader,
            CreateData
        },
        data() {
            return{
                placeholder: "",
                buttonText: "",
                creatingDataOpen: false,
                filter: "",
                dataToAssign: {},
                categoryId: "",
                categoryHelpStrings: {}
            }
        },
        created() {
            this.categoryHelpStrings = helpstrings.metarule;
            this.placeholder = "Filter by " + this.name;
            this.buttonText = "Create " + this.name;
            if (this.policy.model.meta_rules.length){
                let category = this.name.toLowerCase()+ "_categories";
                let metaRule = this.policy.model.meta_rules[0];
                this.categoryId = metaRule[category][0].id;
            }

        },
        methods: {
            populatePolicy() {
                PolicyService.populatePolicy(this.policy);
            },
            assignData(type, data) {
                this.dataToAssign = {
                    selectedData: data,
                    selectedDataType: type,
                };
            },
            creatingData(){
                this.creatingDataOpen = true;

            }
        },
        computed: {
            filteredData() {
                return util.filterAndSortByName(this.data, this.filter);
            }
        }
    }
</script>

<style scoped>

</style>