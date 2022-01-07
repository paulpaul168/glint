<template>
  <div class="file-footer d-flex flex-row">
    <v-spacer></v-spacer>
    <v-select
      v-model="languageSelect"
      :class="'dropdown ' + languageSelectLabelClass"
      dense
      :label="'auto: ' + detectedLanguage"
      placeholder="auto"
      hide-details="auto"
      clearable
      append-icon="mdi-chevron-down"
      :menu-props="{
        top: true,
        offsetY: true,
        nudgeTop: 16,
        transition: 'scroll-y-reverse-transition',
      }"
      :items="languageList"
      @change="emitLanguageSet"
      @blur="languageSelectLabelClass = 'hide-label'"
      @focus="languageSelectLabelClass = ''"
    >
      <!--<template v-slot:append>
        <v-icon small>mdi-chevron-down</v-icon>
      </template>-->
    </v-select>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

import { supportedLanguages } from "@/services/LanguageDetection";

@Component({
  components: {},
})
export default class FileFooter extends Vue {
  name = "FileFooter";
  private languageList = supportedLanguages;
  private languageSelect: string | null = "auto";
  @Prop({ default: "auto" }) language!: string;
  @Prop({ default: "Language" }) detectedLanguage!: string;
  private languageSelectLabelClass = "hide-label";

  created(): void {
    this.languageChange();
  }

  @Watch("language")
  private languageChange(): void {
    if (this.language != "auto") {
      this.languageSelect = this.language;
    } else {
      this.languageSelect = null;
    }
    this.$forceUpdate();
  }

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
  margin-top: 0;
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

<style>
div.v-menu__content {
  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_tertiary-base);
}

.v-list-item__content {
  color: white;
}

.v-select-list {
  background-color: var(--v-bg_tertiary-base) !important;
  /*TODO is there a better way to do this than a global important style?*/
}
</style>
