<template>
  <v-alert
    :value="show"
    class="global-notifier"
    dense
    :type="notification.type"
    :dismissible="notification.timeout <= 0 || notification.timeout > 5000"
    transition="scroll-y-transition"
  >
    {{ notification.message }}
  </v-alert>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { Notification } from "./types/interfaces";

@Component({
  components: {},
})
export default class GlobalNotifier extends Vue {
  name = "GlobalNotifier";
  @Prop({ default: { type: "info", message: "Empty Message", timeout: 5000 } })
  notification!: Notification;
  private show = false;
  private timeout = 0;

  @Watch("notification")
  displayNotification(): void {
    this.show = true;
    clearTimeout(this.timeout);
    if (
      this.notification.timeout == undefined ||
      this.notification.timeout > 0
    ) {
      this.timeout = setTimeout(
        this.hide,
        this.notification.timeout == undefined
          ? 5000
          : this.notification.timeout
      );
    }
  }

  hide(): void {
    this.show = false;
  }
}
</script>

<style scoped>
.global-notifier {
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 2em;
}
</style>
