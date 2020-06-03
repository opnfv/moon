<template>
  <div id="app">

    <nav role="navigation" class="navbar navbar-expand-sm" v-if="$route.name != 'auth' && $route.name != 'error'">
      <ul class="navbar-nav" >
        <li class="nav-item">
          <router-link to="/models" class="nav-link" active-class="o-active">Models</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/rules" class="nav-link" active-class="o-active">Rules</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/assignments" class="nav-link" active-class="o-active">Assignments</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/pdp" class="nav-link" active-class="o-active">PDP</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin" class="nav-link" active-class="o-active">Admin</router-link>
        </li>
      </ul>
      <a href="#" class="btn btn-primary btn-sm active ml-auto" role="button" aria-pressed="true" @click="logout()">logout</a>
    </nav>
    <br>

    <router-view/>
  </div>
</template>


<script>
export default {
  methods: {
    logout: function() {
      localStorage.setItem("auth-key", null);
      this.$router.push('auth');
    }
  }
}
</script>

