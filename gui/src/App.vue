<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/stop-and-wait">Stop And Wait</router-link> |
      <router-link to="/go-back-n">Go Back N</router-link> |
      <router-link to="/selective-repeat">Selective Repeat</router-link> |
      <b-dropdown id="dropdown" text="Others" variant="outline-primary" size="sm">
        <b-dropdown-item>
          <router-link :to="{ name: 'Others', params: { protocol: 'rdt2.2' } }">
            Rdt2.2
          </router-link>
        </b-dropdown-item>
        <b-dropdown-item>
          <router-link :to="{ name: 'Others', params: { protocol: 'rdt2.1' } }">
            Rdt2.1
          </router-link>
        </b-dropdown-item>
        <b-dropdown-item>
          <router-link :to="{ name: 'Others', params: { protocol: 'rdt2.0' } }">
            Rdt2.0
          </router-link>
        </b-dropdown-item>
        <b-dropdown-item>
          <router-link :to="{ name: 'Others', params: { protocol: 'rdt1.0' } }">
            Rdt1.0
          </router-link>
        </b-dropdown-item>
      </b-dropdown>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
  background-color: lightgray;
  margin-bottom: 5;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
