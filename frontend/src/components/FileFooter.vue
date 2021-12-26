<template>
  <div class="file-footer"></div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class FileFooter extends Vue {
  name = "FileFooter";
}
</script>

<style scoped>
.file-footer {
  height: 36px;
  background-color: var(--v-bg_tertiary-base);
}
</style>
