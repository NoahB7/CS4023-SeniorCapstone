<template>
  <v-container
    ><v-snackbar top v-model="showSnackbar" :color="snackBarColor">{{
      snackBarMessage
    }}</v-snackbar>
    <div v-show="tab == 0" class="pt-1">
      <v-row class="mt-4">
        <v-col cols="2"> </v-col>
        <v-col cols="4">
          <v-card width="100%" elevation="0">
            <div>
              <div
                :style="
                  showDetails
                    ? 'font-size: 180px; text-align: center'
                    : 'font-size: 30px; text-align: center'
                "
                class="secondary--text mt-10"
              >
                VizFit
              </div>
              <div style="font-size: 20px; text-align: center" class="mt-1">
                Computer vision made for fitness
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-img width="90%" src="../assets/8.jpg" />
        </v-col>
        <v-col cols="2"> </v-col
      ></v-row>
      <v-row class="mt-16 mb-8">
        <v-col cols="2"> </v-col>
        <v-col cols="8">
          <v-card
            min-height="350px"
            style="font-size: 20px; text-align: center"
            width="100%"
            color="primary"
            class="white--text"
          >
            <v-row>
              <v-col>
                <v-row>
                  <v-col cols="12">
                    <v-card
                      elevation="0"
                      color="primary"
                      class="mt-3 ml-5 mr-5 secondary--text"
                      style="font-size: 30px; text-align: center"
                    >
                      Computer Vision
                    </v-card>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <div class="mt-3 ml-5 mr-5">
                      Using your webcam on your computer, our application is
                      able to track three different types of exercises just by
                      watching your movements!
                    </div>
                  </v-col>
                </v-row>
              </v-col>
              <v-col>
                <v-row>
                  <v-col cols="12">
                    <v-card
                      elevation="0"
                      color="primary"
                      class="mt-3 ml-5 mr-5 secondary--text"
                      style="font-size: 30px; text-align: center"
                    >
                      Deep Learning
                    </v-card>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <div class="mt-3 ml-5 mr-5">
                      With the help of deep learning, we are able to train a
                      neural network model to identify points on your body!
                    </div>
                  </v-col>
                </v-row>
              </v-col>
              <v-col>
                <v-row>
                  <v-col>
                    <v-card
                      elevation="0"
                      color="primary"
                      class="mt-3 ml-5 mr-5 secondary--text"
                      style="font-size: 30px; text-align: center"
                    >
                      Founders
                    </v-card>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <div class="mt-3 ml-5 mr-5">
                      This fantastic application was brought to you by Noah
                      Buchanan, Sam Donaldson, Sasha Lawson, and Alana Matheny.
                    </div>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3"> </v-col>
              <v-col cols="6">
                <v-img
                  src="../assets/green.png"
                  alt="Green Line"
                  height="100%"
                  width="100%"
                />
              </v-col>
              <v-col cols="3"> </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="2"> </v-col>
      </v-row>
    </div>
    <v-card v-show="tab == 1" elevation="0" style="positon: relative" tile>
      <div style="width: 100%; text-align: center; color: #2c3e50">
        <div
          style="
            width: 100%;
            padding: 0px;
            color: #6aa84f;
            font-size: 40px;
            position: static;
          "
        >
          Personal Achievements
        </div>

        <div style="width: 100%; color: black; font-size: 20px">
          See your workout history!
        </div>
        <p style="padding: 2px"></p>
        <center>
          <v-card elevation="10" style="max-width: 80%">
            <v-sheet
              style="padding: 15px"
              class="v-sheet--offset mx-auto"
              elevation="0"
              max-width="90%"
            >
              <v-sparkline
                :labels="labels"
                :value="value"
                :gradient="gradient"
                line-width="2"
                padding="16"
              ></v-sparkline>
            </v-sheet>
            <center>
              <hr width="100%" />
            </center>
            <v-card-text class="pt-0" style="background-color: #ececec">
              <div
                class="text-h6 font-weight-light mb-2"
                style="color: black; padding: 20px"
              >
                <b style="font-size: 25px">Last Workout Performance</b>
              </div>

              <v-col>
                <v-row>
                  <v-col>
                    <div>
                      <span style="color: black; font-size: 20px">
                        <v-icon style="color: #6aa84f; padding-right: 10px">
                          mdi-clock</v-icon
                        >{{ workoutTime }} minutes</span
                      >
                    </div>
                  </v-col>

                  <v-col>
                    <div>
                      <span style="color: black; font-size: 20px"
                        ><v-icon style="color: #6aa84f; padding-right: 10px">
                          mdi-arm-flex</v-icon
                        >{{ workoutPushups }} pushups</span
                      >
                    </div>
                  </v-col>

                  <v-col>
                    <div>
                      <span style="color: black; font-size: 20px"
                        ><v-icon style="color: #6aa84f; padding-right: 10px">
                          mdi-dumbbell</v-icon
                        >{{ workoutSitups }} situps</span
                      >
                    </div>
                  </v-col>

                  <v-col>
                    <div>
                      <span style="color: black; font-size: 20px">
                        <v-icon style="color: #6aa84f; padding-right: 10px">
                          mdi-yoga</v-icon
                        >{{ workoutSquats }} squats</span
                      >
                    </div>
                  </v-col>
                </v-row>
              </v-col>
            </v-card-text>
          </v-card>
        </center>
      </div>
      <p style="padding: 10px"></p>
      <v-card-title
        style="
          width: 100%;
          padding-top: 0px;
          padding-bottom: 0px;
          padding-left: 62px;
        "
      >
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          solo
          single-line
        ></v-text-field>
        <p
          style="
            vertical-align: middle;
            padding-bottom: 10px;
            padding-left: 10px;
          "
        >
          <v-btn
            icon
            @click="getAllWorkoutsForUserId(user.userId)"
            color="secondary"
          >
            <v-icon large> mdi-refresh </v-icon>
          </v-btn>
        </p>
      </v-card-title>
      <v-card
        elevation="20"
        height="100%"
        style="padding-bottom: 10px; bottom: 20px"
      >
        <v-data-table
          mobile-breakpoint="0"
          :items-per-page="10"
          :headers="workoutTableHeaders"
          :items="usersWorkouts"
          :search="search"
          :footer-props="{
            showFirstLastPage: true,
            firstIcon: 'mdi-arrow-collapse-left',
            lastIcon: 'mdi-arrow-collapse-right',
            prevIcon: 'mdi-arrow-left',
            nextIcon: 'mdi-arrow-right',
          }"
        >
          <template v-slot:item="{ item }">
            <Workout :item="item" :headers="workoutTableHeaders" />
          </template>
        </v-data-table>
      </v-card>
    </v-card>
    <v-card v-show="tab == 2" elevation="0" style="positon: relative" tile>
      <div style="width: 100%; text-align: center; color: #2c3e50">
        <div
          style="
            width: 100%;
            padding-top: 0px;
            color: #6aa84f;
            font-size: 40px;
            position: static;
          "
        >
          Global Ranking
        </div>

        <div
          style="width: 100%; position: static; color: black; font-size: 20px"
        >
          See where you rank!
        </div>
        <p style="padding: 10px"></p>
        <center>
          <v-card
            elevation="20"
            height="100%"
            style="padding-bottom: 10px; bottom: 20px"
          >
            <v-data-table
              mobile-breakpoint="0"
              :items-per-page="10"
              :headers="workoutTableHeaders"
              :items="displayedWorkout"
              :footer-props="{
                showFirstLastPage: true,
                firstIcon: 'mdi-arrow-collapse-left',
                lastIcon: 'mdi-arrow-collapse-right',
                prevIcon: 'mdi-arrow-left',
                nextIcon: 'mdi-arrow-right',
              }"
            >
              <template v-slot:item="{ item }">
                <Workout :item="item" :headers="leaderboardTableHeaders" />
              </template>
            </v-data-table>
            <div style="vertical-align: middle; padding: 0px; margin: 0px">
              <v-btn icon @click="setLeaderboard()" color="secondary">
                <v-icon large> mdi-refresh </v-icon>
              </v-btn>
            </div>
          </v-card>
        </center>
      </div>
      <p style="padding: 5px"></p>
    </v-card>
  </v-container>
</template>
<script>
const gradients = [
  ["#222"],
  ["#42b3f4"],
  ["red", "orange", "yellow"],
  ["purple", "violet"],
  ["#00c6ff", "#F0F", "#FF0"],
  ["#ffd200", "#1feaea", "red"],
];
import { api } from "../utilities/api";
import Workout from "./Workout.vue";
export default {
  components: { Workout },
  name: "Main",
  data() {
    return {
      workoutSitups: "",
      workoutSquats: "",
      workoutPushups: "",
      workoutTime: "",
      showSnackbar: false,
      snackBarColor: "",
      snackBarMessage: "",
      search: "",
      sortBy: "date",
      labels: [],
      gradient: gradients[5],
      gradients,
      leaderboardTableHeaders: [
        {
          align: "start",
          class: "third",
        },
        { text: "Rank", value: "ranked", class: "third" },
        { text: "User", value: "username", class: "third" },
        { text: "Pushups", value: "pushups", class: "third" },
        { text: "Situps", value: "situps", class: "third" },
        { text: "Squats", value: "squats", class: "third" },
        { text: "Total", value: "total", class: "third" },
      ],
      workoutTableHeaders: [
        {
          align: "start",
          class: "third",
        },
        { text: "Pushups", value: "pushups", class: "third" },
        { text: "Situps", value: "situps", class: "third" },
        { text: "Squats", value: "squats", class: "third" },
        { text: "Duration", value: "duration", class: "third" },
        { text: "Date", value: "date", class: "third" },
        { text: "Total", value: "total", class: "third" },
      ],
      usersWorkouts: [],
      displayedWorkout: [],
      value: [],
      windowWidth: window.innerWidth,
      loading: false,
    };
  },
  methods: {
    async getAllWorkoutsForUserId(id) {
      if (id) {
        var resp = await api.getAllWorkoutsForUserId(id);
        this.usersWorkouts = resp.data;
        var current = new Date();
        this.value = [this.labels.length];
        for (var i = 0; i < this.labels.length; i++) {
          this.value[i] = 0;
        }
        for (var j = 0; j < this.usersWorkouts.length; j++) {
          if (this.usersWorkouts[j].workoutEndTime) {
            var date = new Date(this.usersWorkouts[j].workoutEndTime);
            if (
              current.getFullYear() == date.getFullYear() &&
              current.getMonth() == date.getMonth()
            ) {
              this.value[date.getDate() - 1] +=
                this.usersWorkouts[j].squats +
                this.usersWorkouts[j].situps +
                this.usersWorkouts[j].pushups;

              this.workoutSitups = this.usersWorkouts[j].situps;
              this.workoutSquats = this.usersWorkouts[j].squats;
              this.workoutPushups = this.usersWorkouts[j].pushups;

              var start = new Date(this.usersWorkouts[j].workoutStartTime);
              var end = new Date(this.usersWorkouts[j].workoutEndTime);
              var diffMs = end - start; // milliseconds between now & Christmas
              var diffMins = Math.round(
                ((diffMs % 86400000) % 3600000) / 60000
              ); // minutes
              this.workoutTime = diffMins;
            }
          }
        }
      } else {
        this.showSnackbar = true;
        this.snackBarColor = "warning";
        this.snackBarMessage = "You must login to view workout history";
      }
    },
    async setLeaderboard() {
      var resp = await api.getLeaderboard();
      this.displayedWorkout = resp.data;
    },
    createDayArray() {
      var days = this.daysInThisMonth();
      var temp = [];
      for (var i = 0; i < days; i++) {
        temp[i] = i + 1;
      }
      this.labels = temp;
    },
    daysInThisMonth() {
      var now = new Date();
      return new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    },
    testAPI() {
      api.makeGetRequest();
    },
    async testAPIUsers() {
      await api.getAllUsers();
    },
    async setWorkoutForUserId(userId) {
      if (userId) {
        await this.getAllWorkoutsForUserId(userId);
      }
    },
  },
  computed: {
    showDetails() {
      if (this.windowSize > 1000) {
        return true;
      }
      return false;
    },
  },
  mounted() {},
  created() {
    this.setLeaderboard();
    this.createDayArray();
  },
  watch: {
    "user.username": function () {
      this.setWorkoutForUserId(this.user.userId);
    },
  },
  props: {
    tab: Number,
    user: Object,
    windowSize: Number,
  },
};
</script>
<style scoped>
</style>
