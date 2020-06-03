<template>
    <div class="form-inline row">
      <input
        type="search"
        class="form-control filter col-9 mr-auto"
        :placeholder="placeholder"
        v-bind:value="value"
        v-on:input="$emit('input', $event.target.value)"
      >
      <div class="col"></div>
      <button v-if="needButton" type="button" class="btn btn-primary col-auto " @click="$emit('click')">
        <span class="fa fa-plus"></span>
        {{ buttonText }}
      </button>
    </div>
</template>

<script>
export default {
    props: {
        value: String,
        needButton: Boolean,
        buttonText: String,
        placeholder: String,
    }
}
</script>