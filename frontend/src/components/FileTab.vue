<template>
  <div class="d-flex flex-row" style="width: 100%">
    <div class="unsaved-indicator" v-if="unsaved">*</div>
    <v-text-field
      :class="
        'tab-title ' +
        (active ? (hasFocus ? 'title-focus' : 'title-active') : '')
      "
      v-model="internalTitle"
      label="File Name"
      solo
      dense
      flat
      hide-details="auto"
      :background-color="hasFocus ? 'bg_secondary' : 'transparent'"
      :disabled="!active"
      @focus="hasFocus = true"
      @blur="hasFocus = false"
      @change="emitRename"
    ></v-text-field>
    <v-spacer></v-spacer>
    <!--<div class="unsaved-indicator" v-if="unsaved">*</div>-->
    <v-btn
      v-if="active"
      class="tab-close"
      small
      elevation="0"
      color="transparent"
      @click="emitClose"
    >
      <v-icon small :color="active ? 'primary' : ''">mdi-window-close</v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

@Component({
  components: {},
})
export default class FileTab extends Vue {
  name = "FileTab";
  @Prop() title!: string;
  @Prop({ default: false }) unsaved!: boolean;
  @Prop({ default: false }) active!: boolean; //whether or not this tab is currently active
  private hasFocus = false;
  private internalTitle = "";

  created(): void {
    this.titleChanged();
  }

  @Watch("title")
  private titleChanged(): void {
    this.internalTitle = this.title;
  }

  private emitClose(): void {
    this.$emit("file-close");
  }

  private emitRename(): void {
    this.$emit("file-rename", this.internalTitle);
  }
}
</script>

<style scoped>
.tab-title {
  margin-left: -12px;
  margin-right: auto;
  transition: color 0.1s;
}

.unsaved-indicator {
  margin-top: 0.5em;
  margin-left: -0.6em;
  margin-right: 0.1em;
  font-size: 1.1em;
  z-index: 10;
}

.tab-close {
  min-width: 28px !important;
  padding: 0 !important;
  margin-right: -12px;
  margin-left: 4px;
  margin-top: auto;
  margin-bottom: auto;
}

.title-active {
  margin-bottom: 3px;
}

.title-active::v-deep input {
  color: var(--v-primary-base);
  transition: color 0.2s;
}

.title-focus {
  margin-bottom: 3px;
}

.title-focus::v-deep input {
  color: lightgrey;
  transition: color 0.2s;
}
</style>
