import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: false,
        themes: {
            light: {
                primary: "#616161",
                secondary: "#6aa84f",
                third: "#91dc6f",
                forth: "#ececec"
                // primary: "#4d4d4d",
                // secondary: "#2eb82e"
            }
        }
    }
});
