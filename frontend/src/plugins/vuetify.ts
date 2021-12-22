import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: "mdi",
  },
  theme: {
    dark: true,
    options: {
      customProperties: true,
    },
    themes: {
      dark: {
        primary: "#3f51b5",
        secondary: "#607d8b",
        bg_primary: "#121212",
        bg_secondary: "#1e1e1e",
        bg_tertiary: "#272727",
        accent: "#2196f3",
        error: "#f44336",
        warning: "#ff9800",
        info: "#5f71d5",
        success: "#4caf50",
      },
    },
  },
});
