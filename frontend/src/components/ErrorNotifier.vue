<template>
  <v-alert
    :value="showNotification"
    class="global-notifier"
    dense
    transition="slide-y-transition"
    :type="type"
    :dismissible="timeout <= 0"
  >
    {{ message }}
  </v-alert>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class ErrorNotifier extends Vue {
  name = "ErrorNotifier";
  @Prop({ default: "Empty Message" }) message!: string;
  @Prop({ default: "info" }) type!: string;
  @Prop({ default: 3000 }) timeout!: number;
  private showNotification = false;

  show(): void {
    setTimeout(this.hide, this.timeout);
    this.showNotification = true;
  }

  hide(): void {
    this.showNotification = false;
  }
}
</script>

<style scoped>
.global-notifier {
  position: fixed;
  bottom: 3em;
  margin-left: auto;
  margin-right: auto;
}
</style>
