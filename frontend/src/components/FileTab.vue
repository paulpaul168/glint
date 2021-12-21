<template>
  <div class="d-flex flex-row" style="width: 100%">
    <!--<div class="tab-title">
      {{ title + (unsaved ? "*" : "") }}
    </div>-->
    <v-text-field
      style="margin-right: auto"
      class="tab-title"
      v-model="title"
      label="File Name"
      solo
      dense
      flat
      hide-details="auto"
      @focus="backgroundColor = 'bg_secondary'"
      @blur="backgroundColor = 'transparent'"
      :background-color="backgroundColor"
      :disabled="!active"
    ></v-text-field>
    <v-spacer></v-spacer>
    <v-btn
      v-if="active"
      class="tab-close"
      small
      elevation="0"
      color="transparent"
      @click="closeFile"
    >
      <v-icon small>mdi-window-close</v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class FileTab extends Vue {
  name = "FileTab";
  @Prop() title!: string;
  @Prop({ default: false }) unsaved!: boolean;
  @Prop({ default: false }) active!: boolean; //whether or not this tab is currently active
  private backgroundColor = "transparent";

  private closeFile(): void {
    this.$emit("file-close");
  }
}
</script>

<style scoped>
.tab-title {
  margin-left: -12px;
}

.tab-close {
  min-width: 28px !important;
  padding: 0 !important;
  margin-right: -8px;
  margin-left: 4px;
  margin-top: auto;
  margin-bottom: auto;
}
</style>
