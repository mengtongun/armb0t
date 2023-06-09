<template>
  <v-app id="inspire">
    <v-system-bar>
      <v-spacer></v-spacer>

      <v-icon>mdi-square</v-icon>

      <v-icon>mdi-circle</v-icon>

      <v-icon>mdi-triangle</v-icon>
    </v-system-bar>

    <v-navigation-drawer v-model="drawer">
      <v-sheet color="grey-lighten-4" class="pa-4">
        <v-avatar class="mb-4" color="grey-darken-1" size="64"></v-avatar>

        <div>john@google.com</div>
      </v-sheet>

      <v-divider></v-divider>

      <v-list>
        <v-list-item v-for="[icon, text] in links" :key="icon" link>
          <template v-slot:prepend>
            <v-icon>{{ icon }}</v-icon>
          </template>

          <v-list-item-title>{{ text }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container class="py-8 px-6 overflow-y-auto chat-box" fluid>
        <v-row>
          <v-col cols="12">
            <v-card>
              <v-list lines="two">
                <v-list-subheader>Bot ARM Conversation</v-list-subheader>
                <template v-for="msg in messages" :key="msg.id">
                  <v-list-item v-if="msg.from == 'bot'">
                    <template v-slot:prepend>
                      <v-avatar color="grey-darken-1"></v-avatar>
                    </template>

                    <v-list-item-title>{{
                      msg.from == "bot" ? "Bot" : "User"
                    }}</v-list-item-title>

                    <v-list-item-subtitle>
                      {{ msg.content }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-else>
                    <template v-slot:append>
                      <v-avatar color="grey-darken-1"></v-avatar>
                    </template>

                    <v-list-item-title class="text-right">{{
                      msg.from == "bot" ? "Bot" : "User"
                    }}</v-list-item-title>

                    <v-list-item-subtitle class="text-right">
                      {{ msg.content }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <div class="chat-input-box" ref="chatInputBox">
      <v-container>
        <v-row align="center">
          <v-col cols="10 pl-16">
            <v-text-field
              :disabled="loading"
              v-model="userInput"
              label="Enter your message"
              @keyup.enter="sendMessage"
            ></v-text-field>
          </v-col>
          <v-col cols="2">
            <v-btn :disabled="loading" :loading="loading" @click="sendMessage"
              >Send</v-btn
            >
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-app>
</template>

<script setup >
import { ref } from "vue";
import {
  decideQuestions,
  movingToBaseResponse,
  pickingRedColorResponse,
  startingEngineResponse,
} from "@/services/chatgpt";
import {
  moveToRedBin,
  MOVE_BASE,
  PICK_BLUE,
  PICK_GREEN,
  PICK_RED,
  PICK_YELLOW,
  startPickRed,
  START_ENGINE,
} from "@/services/choice";
import { detectedColors } from "@/services/detection";
const links = ref([
  ["mdi-inbox-arrow-down", "Inbox"],
  ["mdi-send", "Send"],
  ["mdi-delete", "Trash"],
  ["mdi-alert-octagon", "Spam"],
]);
const drawer = ref(null);
const messages = ref([]);
const userInput = ref("");
const loading = ref(false);
const sendMessage = () => {
  if (!userInput.value) return;

  messages.value.push({
    id: messages.value.length,
    from: "user",
    content: userInput.value,
  });

  console.log(userInput.value);
  loading.value = true;
  detectedColors().then((c) => {
    console.log(c);
  });
  if (userInput.value == "move red") {
    moveToRedBin();
    return;
  }
  decideQuestions(userInput.value)
    .then((res) => {
      console.log("Response form chatgpt", res);
      switch (res) {
        case START_ENGINE:
          startingEngineResponse().then((res) => {
            console.log(res);
            messages.value.push({
              id: messages.value.length,
              from: "bot",
              content: res,
            });
          });
          break;
        case MOVE_BASE:
          movingToBaseResponse().then((res) => {
            console.log(res);
            messages.value.push({
              id: messages.value.length,
              from: "bot",
              content: res,
            });
          });
          break;
        case PICK_RED:
          pickingRedColorResponse("red").then((resRed) => {
            startPickRed();
            messages.value.push({
              id: messages.value.length,
              from: "bot",
              content: resRed,
            });
          });
          break;
        case PICK_BLUE:
          pickingRedColorResponse("blue").then((res) => {
            console.log(res);
            messages.value.push({
              id: messages.value.length,
              from: "bot",
              content: res,
            });
          });
          break;
        case PICK_YELLOW:
          pickingRedColorResponse("yellow").then((res) => {
            console.log(res);
            messages.value.push({
              id: messages.value.length,
              from: "bot",
              content: res,
            });
          });
          break;
        case PICK_GREEN:
          pickingRedColorResponse("green").then((res) => {
            console.log(res);
            messages.value.push({
              id: messages.value.length,
              from: "bot",
              content: res,
            });
          });
          break;
        default:
          messages.value.push({
            id: messages.value.length,
            from: "bot",
            content: res,
          });
          break;
      }
    })
    .finally(() => {
      setTimeout(() => {}, 1000);
      loading.value = false;
    });

  userInput.value = "";
};
</script>
<style  >
.chat-input-box {
  box-shadow: 0 -2px 5px 0 rgba(0, 0, 0, 0.26);
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 16px;
}
.chat-box {
  padding-bottom: 150px;
  margin-bottom: 150px;
}
</style>
