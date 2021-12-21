<template>
  <div class="d-flex flex-row">
    <div class="tab-title">
      {{ title }}<p v-if="unsaved">*</p>
    </div>
    <v-icon class="tab-close">mdi-window-close</v-icon>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class CodeView extends Vue {
  @Prop() title!: string;
  @Prop({ default: false }) unsaved!: boolean;
}
</script>

<style scoped>
.tab-title {
  align-self: flex-start;
}

.tab-close {
  align-self: flex-end;
}
</style>
