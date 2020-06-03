<template>
    <div>
        <form-header
                placeholder="Filter by Policy"
                needButton
                buttonText="Create Policy"
                @click="creatingPolicy = true"
                v-model="filter"
        ></form-header>
        <br/>

        <CreatePolicy v-if="creatingPolicy" @close="creatingPolicy = false"></CreatePolicy>
        <div class="list-group row" v-else>
            <policy v-for="policy in filteredPolicies" :key="policy.id" :policy="policy"></policy>
        </div>
    </div>
</template>

<script>
    import PolicyService from './../services/Policy.service.js'
    //import util from './../services/Util.service.js'
    import FormHeader from "./../components/FormHeader.vue"
    import Policy from "./../components/assignment/Policy.vue"
    import CreatePolicy from "./../components/policy/CreatePolicy.vue"
    import util from "../services/Util.service";

    export default {
        data() {
            return {
                filter: "",
                creatingPolicy: false,
                policies: []
            };
        },
        mounted() {
            PolicyService.initialize();
            this.policies = PolicyService.policies;
        },
        components: {
            FormHeader,
            Policy,
            CreatePolicy,
        },
        computed: {
            filteredPolicies() {
                return util.filterAndSortByName(this.policies, this.filter);
            }
        }
    }
</script>

<style scoped>

</style>