<template>
  <tr>
    <td v-for="header in headers" :key="header.value">
      <div>
        <template>
          <div v-if="header.value == 'workoutStartTime'">
            {{ formatTimestamp(item.workoutStartTime) }}
          </div>
          <div v-if="header.value == 'ranked'">
             <v-icon class="mr-4" v-if="item.ranked == 1" color="#FFD700">mdi-numeric-1</v-icon>
             <v-icon v-else-if="item.ranked == 2" color="#C0C0C0">mdi-numeric-2</v-icon>
             <v-icon v-else-if="item.ranked == 3" color="#CD7F32">mdi-numeric-3</v-icon>
             <div class="ml-2" v-else>{{ item.ranked }}</div>
          </div>
          <div v-else-if="header.value == 'workoutEndTime'">
            {{ formatTimestamp(item.workoutEndTime) }}
          </div>
          <div v-else-if="header.value == 'duration'">
            {{ totalTime(item.workoutEndTime, item.workoutStartTime) }}
          </div>
          <div v-else-if="header.value == 'date'">
            {{ formatDate(item.workoutStartTime) }}
          </div>
          <div v-else>{{ item[header.value] }}</div>
        </template>
      </div>
    </td>
  </tr>
</template>
<script>
export default {
  name: "Workout",
  data() {
    return {};
  },
  methods: {
    totalTime(timestamp1, timestamp2) {
      var diff =
        new Date(timestamp1).getTime() - new Date(timestamp2).getTime();
      var minutes = Math.floor(diff / 60000);
      var seconds = ((diff % 60000) / 1000).toFixed(0);
      return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
    },
    formatDate(timestamp) {
      var d = new Date(timestamp);
      return d.getMonth() + "/" + d.getDate() + "/" + d.getFullYear();
    },
    formatTimestamp(timestamp) {
      var d = new Date(timestamp);
      return d.toLocaleTimeString();
    },
  },
  created() {},
  watch: {},
  props: {
    item: Object,
    headers: Array,
  },
};
</script>
<style scoped>
#no-background-hover::before {
   background-color: transparent !important;
}
.min-button::before {
  display: none;
}
</style>

