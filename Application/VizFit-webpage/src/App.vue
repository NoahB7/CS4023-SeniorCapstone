<template>
  <v-app>
    <v-snackbar top color="success" v-model="showSnackbar">
      {{ snackbarMessage }}
    </v-snackbar>
    <v-app-bar app color="primary" dark ref="appbar">
      <v-app-bar-title
        class="white--text"
        :style="showDetails ? 'min-width: 50px' : ''"
      >
        <!-- <v-icon v-if="showDetails" color="secondary">mdi-heart-pulse</v-icon> -->
        {{ showDetails ? "VizFit" : "" }}
      </v-app-bar-title>
      <v-tabs
        :class="showDetails ? 'ml-10' : ''"
        :style="showDetails ? '' : 'margin-left: -10px'"
        v-model="tab"
        background-color="primary"
        dark
        icons-and-text
      >
        <v-tab>
          Home
          <v-icon>mdi-home</v-icon>
        </v-tab>
        <v-tab>
          {{ showDetails ? "Personal Achievements" : "Personal" }}
          <v-icon>mdi-trophy</v-icon>
        </v-tab>
        <v-tab>
          {{ showDetails ? "Global Achievements" : "Global" }}
          <v-icon>mdi-earth</v-icon>
        </v-tab>
      </v-tabs>
      <v-col>
        <v-menu
          offset-y
          :close-on-content-click="false"
          v-model="loginMenuOpen"
          v-if="!user.username"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-col>
              <div
                v-bind="attrs"
                v-on="on"
                :class="loggedInStyle ? 'mt-3' : ''"
              >
                <v-row>
                  <v-btn
                    elevation="0"
                    tile
                    text
                    color="primary lighten-5"
                    :height="appBarHeight"
                  >
                    <v-icon
                      v-if="showDetails"
                      color="primary lighten-5"
                      style=""
                      >mdi-login-variant</v-icon
                    >
                    Login
                  </v-btn>
                </v-row>
              </div>
            </v-col>
          </template>
          <v-list
            color="primary lighten-5"
            width="200px"
            :height="loginErrorMessage ? '250px' : ''"
          >
            <v-form ref="loginForm">
              <v-list-item class="mt-2">
                <v-text-field
                  solo
                  :rules="usernameRules"
                  v-model="username"
                  label="username"
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-text-field
                  solo
                  :rules="passwordRules"
                  v-model="password"
                  type="password"
                  label="password"
                  @keydown.enter="login()"
                  :style="loginErrorMessage ? 'margin-bottom: -15px' : ''"
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-col>
                  <v-row v-if="loginErrorMessage">
                    <div
                      style="
                        color: red;
                        width: 100%;
                        text-align: center;
                        font-size: 15px;
                      "
                    >
                      {{ loginErrorMessage }}
                    </div>
                  </v-row>
                  <v-row>
                    <v-spacer />
                    <v-btn
                      color="secondary"
                      style="black--text"
                      @click="login()"
                    >
                      login
                    </v-btn>
                    <v-spacer
                  /></v-row>
                </v-col>
              </v-list-item>
            </v-form>
          </v-list>
        </v-menu>
      </v-col>
      <v-col>
        <v-menu
          offset-y
          :close-on-content-click="false"
          v-model="registerMenuOpen"
          v-if="!user.username"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-col>
              <div
                :class="loggedInStyle ? 'mt-3' : ''"
                v-bind="attrs"
                v-on="on"
                style="margin-left: -24px; margin-right: -50px"
              >
                <v-row>
                  <v-btn
                    elevation="0"
                    tile
                    text
                    color="primary lighten-5"
                    :height="appBarHeight"
                  >
                    <v-icon
                      v-if="showDetails"
                      color="primary lighten-5"
                      style=""
                      >mdi-account-plus</v-icon
                    >
                    Register
                  </v-btn>
                </v-row>
              </div>
            </v-col>
          </template>
          <v-list color="primary lighten-5" min-width="200px">
            <v-form ref="registerForm">
              <v-list-item class="mt-2">
                <v-text-field
                  solo
                  v-model="registerUsername"
                  :rules="registerUsernameRules"
                  label="username"
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-text-field
                  solo
                  type="password"
                  v-model="registerPassword"
                  :rules="registerPasswordRules"
                  label="password"
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-text-field
                  solo
                  type="password"
                  v-model="registerPasswordConfirmation"
                  :rules="registerPasswordConfirmationRules"
                  label="confirm password"
                  @keydown.enter="register()"
                  :style="registerErrorMessage ? 'margin-bottom: -15px' : ''"
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-col>
                  <v-row v-if="registerErrorMessage">
                    <div
                      style="
                        color: red;
                        width: 100%;
                        text-align: center;
                        font-size: 15px;
                      "
                    >
                      {{ registerErrorMessage }}
                    </div>
                  </v-row>
                  <v-row>
                    <v-spacer />
                    <v-btn
                      color="secondary"
                      style="black--text"
                      @click="register()"
                      class="mb-2"
                    >
                      register
                    </v-btn>
                    <v-spacer
                  /></v-row>
                </v-col>
              </v-list-item>
            </v-form>
          </v-list>
        </v-menu>
      </v-col>
      <v-col>
        <div v-if="user.username" style="text-align: center">
          Welcome, {{ user.username }}!
        </div>
      </v-col>
      <v-col>
        <v-btn
          x-small
          v-if="user.username"
          color="secondary"
          @click="logoutCurrentUser()"
        >
          Logout
        </v-btn>
      </v-col>
    </v-app-bar>
    <v-main>
      <Main :tab="tab" :user="user" :windowSize="windowWidth" />
    </v-main>
    <footer class="primary">
      <p
        style="text-align: center; padding: 30px; width: 100%; margin: 0px"
      ></p>
    </footer>
  </v-app>
</template>

<script>
import Main from "./components/Main";
import { api } from "./utilities/api";
export default {
  name: "App",

  components: {
    Main,
  },
  data() {
    return {
      passwordRules: [(v) => !!v || "required"],
      usernameRules: [(v) => !!v || "required"],
      registerUsernameRules: [(v) => !!v || "required"],
      registerPasswordRules: [(v) => !!v || "required"],
      registerPasswordConfirmationRules: [
        (v) => !!v || "required",
        (v) => (!!v && this.passwordsMatch) || "Passwords must match",
      ],
      loginMenu: false,
      text: "blank",
      tab: 0,
      passwordsMatch: true,
      loggedIn: false,
      windowWidth: window.innerWidth,
      username: "",
      password: "",
      registerUsername: "",
      registerPassword: "",
      registerPasswordConfirmation: "",
      loginErrorMessage: "",
      registerMenuOpen: false,
      loginMenuOpen: false,
      registerErrorMessage: "",
      loggedInStyle: true,
      showSnackbar: false,
      snackbarMessage: "",
      user: {
        userId: null,
        username: "",
      },
    };
  },
  methods: {
    logoutCurrentUser() {
      this.user = {
        userId: null,
        username: "",
      };
      var session = {
        username: null,
        userId: 0,
        token: "",
      };

      this.$cookies.set("session", session);
      this.loggedInStyle = false;
    },
    async login() {
      this.loginErrorMessage = "";
      if (this.$refs.loginForm.validate()) {
        this.loginWithCredentials(this.username, this.password);
      }
    },
    async loginWithCredentials(username, password) {
      var resp = await api.login(username, password);
      var user = resp.data;
      if (user.username) {
        this.user.username = user.username;
        this.user.userId = user.userId;

        var session = {
          username: user.username,
          userId: user.userId,
          token: user.token,
        };

        this.$cookies.set("session", session);
        this.snackbarMessage =
          "Successfully logged in as " + this.user.username;
        this.showSnackbar = true;
      } else {
        this.loginErrorMessage = "Incorrect username and/or password";
      }
    },
    async register() {
      this.registerErrorMessage = "";
      if (this.$refs.registerForm.validate()) {
        var resp = await api.register(
          this.registerUsername,
          this.registerPassword
        );
        if (resp.data == 1) {
          this.snackbarMessage =
            "Successfully registered as " + this.registerUsername;
          this.showSnackbar = true;
        } else if (resp.data == -999) {
          this.registerErrorMessage = "Username already taken";
        }
      }
    },
    async loginWithCookie(cookie) {
      var resp = await api.loginWithCookie(cookie);
      if (resp.data && resp.data.username && resp.data.userId) {
        var session = {
          username: resp.data.username,
          userId: resp.data.userId,
          token: resp.data.token,
        };

        this.$cookies.set("session", session);
        this.user.username = resp.data.username;
        this.user.userId = resp.data.userId;
      }
    },
  },
  mounted() {
    window.onresize = () => {
      this.windowWidth = window.innerWidth;
    };
  },

  async created() {
    var cookie = this.$cookies.get("session");
    await this.loginWithCookie(cookie);
  },
  watch: {
    registerMenuOpen: function () {
      if (this.registerMenuOpen == false) {
        this.$refs.registerForm.reset();
      }
    },
    loginMenuOpen: function () {
      if (this.loginMenuOpen == false) {
        this.$refs.loginForm.reset();
      }
    },
    registerPassword: function () {
      if (this.registerPassword == this.registerPasswordConfirmation) {
        this.passwordsMatch = true;
      } else {
        this.passwordsMatch = false;
      }
    },
    registerPasswordConfirmation: function () {
      if (this.registerPassword == this.registerPasswordConfirmation) {
        this.passwordsMatch = true;
      } else {
        this.passwordsMatch = false;
      }
    },
  },
  computed: {
    showDetails() {
      if (this.windowWidth > 1000) {
        return true;
      }
      return false;
    },
    appBarHeight() {
      if (
        this.$refs.appbar &&
        this.$refs.appbar.styles &&
        this.$refs.appbar.styles.height
      ) {
        return this.$refs.appbar.styles.height;
      }
      return "0px";
    },
  },
};
</script>
<style>
</style>
