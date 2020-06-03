<template>
    <span>
        <span v-for="(data, index) in list" :key="data.id">
            <span v-if="index > 0">,</span>
            <span>{{ data.name }}</span>
        </span>
    </span>    
</template>

<script>
export default {
    props: {
        list: Array
    }
}
</script>