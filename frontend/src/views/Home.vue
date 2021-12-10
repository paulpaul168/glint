<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Who is the God?" v-bind="god"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src
import * as api from "@/services/TestAPI.ts";

let god = api.getGod();
console.log(god);

@Component({
  components: {
    HelloWorld,
  },
})
export default class Home extends Vue {}
</script>
