<template>
  <v-item-group>
    <v-row>
      <v-col>
        <project-list />
      </v-col>
      <v-col>
        <file-view />
      </v-col>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import Vue from "vue";
import FileView from "../components/FileView.vue";
import ProjectList from "../components/ProjectList.vue";

export default Vue.extend({
  name: "Home",

  components: {
    FileView,
    ProjectList,
  },
});
</script>
