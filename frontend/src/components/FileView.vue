<template>
  <prism-editor
    class="code-editor"
    v-model="code"
    :highlight="highlighter"
    line-numbers
  ></prism-editor>
</template>

<script lang="ts">
import Vue from "vue";
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css";

import { highlight, languages } from "prismjs";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-tomorrow.css";

export default Vue.extend({
  name: "FileView",
  components: {
    PrismEditor,
  },
  data: () => ({ code: "function(a){let a = b + 5;}" }),
  methods: {
    highlighter(code: string): string {
      return highlight(code, languages.javascript, "javascript");
    },
  },
});
</script>

<style scoped>
.code-editor {
  background: var(--bgprimary);
  color: var(--primary);

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 15px;
  line-height: 1.5;
  padding: 5px;
}
</style>
