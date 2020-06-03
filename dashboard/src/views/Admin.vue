<template>
  <div>
    <div v-if="isLoading" >
      <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
    <div  v-else class="row justify-content-center">
      <label for="file" class="label-file btn btn-primary">
        <span class="fa fa-upload"></span>
        Import
      </label>
      <input
              id="file"
              class="input-file"
              type="file"
              @change="readFile"
              accept="application/json, .json"
      />


  </div>
  </div>
</template>

<script>
import ImportService from "./../services/Import.service.js";

export default {
  data(){
    return {
      isLoading: false
    }
  },
  methods: {
     readFile(event) {
      var reader = new FileReader();
      reader.onload = async function() {
        this.isLoading = true;
        var fileContents = reader.result;
        await ImportService.importData(JSON.parse(fileContents));
        this.isLoading = false;
      }.bind(this);
       reader.readAsText(event.target.files[0]);
    },
  }
};
</script>


