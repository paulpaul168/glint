<template>
  <div class="file-footer d-flex flex-row">
    <v-spacer></v-spacer>
    <v-select
      v-model="languageSelect"
      :class="'dropdown ' + selectLabelClass"
      dense
      :label="'auto: ' + languageLabel"
      placeholder="auto"
      hide-details="auto"
      clearable
      :menu-props="{ top: true, offsetY: true, nudgeTop: 16 }"
      :items="languageList"
      @change="emitLanguageSet"
      @blur="selectLabelClass = 'hide-label'"
      @focus="selectLabelClass = ''"
    >
      <v-icon slot="append-inner" small>mdi-window-close</v-icon>
    </v-select>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import { supportedLanguages } from "@/services/LanguageDetection";

@Component({
  components: {},
})
export default class FileFooter extends Vue {
  name = "FileFooter";
  private languageList = supportedLanguages;
  private languageSelect = "auto";
  @Prop({ default: "Language" }) languageLabel!: string;
  private selectLabelClass = "";

  private emitLanguageSet() {
    if (this.languageSelect == null) {
      this.languageSelect = "auto";
    }
    this.$emit("language-set", this.languageSelect);
  }
}
</script>

<style scoped>
.file-footer {
  height: 26px;
  background-color: var(--v-bg_tertiary-base);
}

.dropdown {
  max-width: 10em;
  margin-top: auto;
  margin-bottom: 0.1em;
  margin-right: 0.7em;
}

.dropdown::v-deep .v-input__icon--clear .v-icon {
  font-size: 1em;
}

.dropdown::v-deep .v-input__append-inner {
  margin-top: auto;
  margin-bottom: auto;
}

.dropdown::v-deep label.v-label {
  top: auto;
}

.dropdown::v-deep div.v-select__selection {
  margin-top: auto;
  margin-bottom: auto;
}

.hide-label::v-deep label.v-label--active {
  visibility: hidden;
  transition: 0.1s;
}
</style>
