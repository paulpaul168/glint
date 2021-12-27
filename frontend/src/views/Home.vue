<template>
  <div class="d-flex flex-row main-pane">
    <div class="project-list">
      <project-list :projects="activeProjects" @linter-set="passLinter" />
    </div>
    <div class="content-view">
      <content-view
        :language="language"
        :linter="linter"
        @notification="passNotification"
        @new-project="addProject"
      />
    </div>
    <global-notifier :notification="notification"></global-notifier>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ContentView from "@/components/ContentView.vue";
import ProjectList from "@/components/ProjectList.vue";
import GlobalNotifier from "@/components/GlobalNotifier.vue";

import { Notification, Project } from "@/components/types/interfaces";

@Component({
  components: {
    ContentView,
    ProjectList,
    GlobalNotifier,
  },
})
export default class Home extends Vue {
  name = "Home";

  private activeProjects: Project[] = [];
  private language = "auto";
  private linter = "auto";

  private addProject(newProject: Project) {
    this.activeProjects.push(newProject);
  }

  private notification: Notification = {
    type: "info",
    message: "Empty Message",
    timeout: 3000,
  };
  private passNotification(newNotification: Notification) {
    this.notification = newNotification;
  }

  private passLinter(linter: string) {
    this.linter = linter;
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

.project-list {
  max-width: 250px;
  min-width: 250px;
  /*min-width: 200px; the automatic content based resizing doesn't quite work, fixed size is better for now*/
  flex: 1 1 content;
}

.content-view {
  flex-grow: 20;
}
</style>
