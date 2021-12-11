import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    options: {
      customProperties: true,
    },
    themes: {
      dark: {
        primary: "#607d8b",
        secondary: "#3f51b5",
        accent: "#2196f3",
        error: "#f44336",
        warning: "#ff9800",
        info: "#ffeb3b",
        success: "#4caf50",
      },
    },
  },
});
