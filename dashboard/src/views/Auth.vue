<template>
  <div class="row justify-content-center">
    <form>
      <div class="form-group">
        <label for="login">Login</label>
        <input
          type="text"
          name="login"
          v-model="name"
          v-validate.initial="'required'"
          class="form-control"
          id="login"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          name="password"
          v-model="password"
          v-validate.initial="'required'"
          class="form-control"
          id="password"
        />
      </div>
      <button type="button" class="btn btn-primary btn-xlg col-auto" @click="login()">Login</button>
    </form>

  </div>
</template>

<script>
import Vue from "vue";
import util from "./../services/Util.service.js";
import config from '../config.js'

var host = config.host;

export default {
  name: "auth",
  data() {
    return {
      name: "",
      password: ""
    };
  },
  methods: {
    login() {
      Vue.http.headers.common["Authorization"] =
        "Basic " + btoa(this.name + ":" + this.password);
      Vue.http.get(host + "/auth").then(
        response => {
          Vue.http.headers.common["Authorization"] = "Basic ";
          Vue.http.headers.common["x-api-key"] = response.data;
          localStorage.setItem("auth-key", response.data);
          this.$router.push("models");
        },
        response => {
          util.displayError("Unable to log in " + response);
        }
      );
    }
  }
};
</script>
