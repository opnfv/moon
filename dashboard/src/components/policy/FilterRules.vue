<template>
    <div class="form-inline">
        <input
                type="search"
                class="form-control filter col mr-auto"
                placeholder="Filter rules"
                v-bind:value="value"
                v-on:input="$emit('input', $event.target.value)"
        >
    </div>
</template>

<script>
    export default {
        name: "FilterRules",
        props: {
            value: String
        }
    }
</script>

<style scoped>

</style>