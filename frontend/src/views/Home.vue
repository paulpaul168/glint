<template>
  <div class="d-flex flex-row main-pane">
    <div style="max-width: 400px; min-width: 200px; flew-grow: 3">
      <project-list />
    </div>
    <div style="flex-grow: 7">
      <content-view @notification="passNotification" />
    </div>
    <error-notifier :notification="notification"></error-notifier>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ContentView from "@/components/ContentView.vue";
import ProjectList from "@/components/ProjectList.vue";
import ErrorNotifier from "@/components/ErrorNotifier.vue";

import { Notification } from "@/components/types/interfaces";

@Component({
  components: {
    ContentView,
    ProjectList,
    ErrorNotifier,
  },
})
export default class Home extends Vue {
  name = "Home";

  private notification: Notification = {
    type: "info",
    message: "Empty Message",
    timeout: 3000,
  };
  private passNotification(newNotification: Notification) {
    this.notification = newNotification;
  }
}
</script>

<style>
.main-pane {
  width: 100%;
  margin: auto;
  height: 100%;
  /*height: calc(97vh - 56px);*/
}

.main-content-pane {
  height: 100%;
}
</style>
