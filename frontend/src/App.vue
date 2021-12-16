<template>
  <v-app>
    <v-app-bar app color="primary" elevation="0">
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="30"
        />
        glint
      </div>

      <v-spacer></v-spacer>

      <v-btn href="/help" target="_blank" text>
        <span class="mr-2">Help</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main style="height: 100vh">
      <v-container style="height: 100%">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "App",

  data: () => ({
    //
  }),
});
</script>

<style>
html {
  scrollbar-color: #252525 #121212;
  overflow-y: hidden !important; /*remove in case scrolling becomes necessary at some point*/
}

html::-webkit-scrollbar {
  width: 15px;
}

html::-webkit-scrollbar-track {
  background: #121212;
  border-left: 1px solid #121212;
}

html::-webkit-scrollbar-track:hover {
  background: #171717;
  border-left: 1px solid #171717;
}

html::-webkit-scrollbar-thumb {
  background: #252525;
  border: solid 4px #121212;
  border-radius: 7px;
}

html::-webkit-scrollbar-thumb:hover {
  background: #333333;
  border: solid 4px #171717;
}
</style>
