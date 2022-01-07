<template>
  <v-item-group style="padding-left: 12px">
    <v-row>
      <v-col class="header-col" cols="9">
        <v-card-title class="header">
          <span style="color: grey">Secret:&nbsp;</span>
          {{ pattern.patternName }}
        </v-card-title>
      </v-col>
      <v-col class="header-col text-right" style="padding-right: 0">
        <v-tooltip bottom open-delay="1000">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              text
              small
              elevation="0"
              class="file-btn"
              v-bind="attrs"
              v-on="on"
              @click="goToFile"
            >
              {{ result.source.name }}: {{ result.line }}
            </v-btn>
          </template>
          <span>Jump to location</span>
        </v-tooltip>
      </v-col>
    </v-row>
    <v-row>
      <v-card outlined elevation="2" class="snippet rounded-md">
        <v-card-text
          class="text"
          style="background-color: var(--v-bg_tertiary-base)"
        >
          <div class="d-flex flex-row">
            Found secret in {{ result.source.name }} at line {{ result.line }}
            <v-spacer></v-spacer>
            <span style="text-align: right">Query:&nbsp;</span>
            <span style="text-align: right; color: var(--v-primary-base)">
              {{ pattern.regex }}
            </span>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <code-view
          :lineNumbers="false"
          :readonly="true"
          :fileState="{
            language: 'auto',
            detectedLanguage: getLanguagePassthrough(result.source.name),
            file: {
              name: result.source.name,
              path: result.source.path,
              content: result.snippet,
            },
            unsaved: false,
            edited: false,
          }"
          :height="'auto'"
          :language="'auto'"
        ></code-view>
      </v-card>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import CodeView from "@/components/CodeView.vue";
import { SearchPattern, SearchResult } from "./types/interfaces";
import { getLanguage } from "@/services/LanguageDetection";

@Component({
  components: {
    CodeView,
  },
})
export default class SecretCard extends Vue {
  name = "SecretCard";
  @Prop() pattern!: SearchPattern;
  @Prop() result!: SearchResult;

  private getLanguagePassthrough(name: string): string {
    return getLanguage(name);
  }

  private goToFile(): void {
    this.$emit("go-to-source", {
      filePath: this.result.source.path,
      line: this.result.line,
    });
  }
}
</script>

<style scoped>
.header {
  padding: 0.2em 0;
  padding-bottom: 0;
  text-align: left;
}

.snippet {
  width: 100%;
  margin-bottom: 1em;
  margin-right: 1em;
}

.text {
  text-align: left;
  padding: 0.7em;
}

.header-col {
  height: auto;
  margin-top: auto;
  margin-bottom: 0;
  padding-bottom: 0.2em;
}

.file-btn {
  margin-right: 1.3em;
  text-transform: none;
  color: var(--v-primary-base);
  transition: 0.1s;
}

.file-btn:hover {
  text-transform: none;
  color: var(--v-accent-base);
  transition: 0.2s;
}
</style>
