<template>
  <v-container fluid style="width: 90%">
    <v-row dense>
      <v-col cols="2">
        <project-list />
      </v-col>
      <v-col cols="10">
        <file-view />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import FileView from "../components/ContentView.vue";
import ProjectList from "../components/ProjectList.vue";

export default Vue.extend({
  name: "Home",

  components: {
    FileView,
    ProjectList,
  },
});
</script>
