<template>

  <div id="app" class="container my-3">
    <h3>AI-API-Frontend</h3>

    <div class="card-group">
      <div class="card mt-3">
        <div class="card-header">Neue Chat-UUID erhalten (POST)</div>
        <div class="card-body">
          <div class="form-group">
            <p>
              Alle Eingaben und Daten aus der Nutzung des Chatbots werden
              gespeichert und weiterverarbeitet (<a href="">Datenschutzerklärung und Nutzungsbedingungen</a>).
              Wenn du damit einverstanden bist, schreibe "Einverstanden" in den Chat.
            </p>
            <input type="text" class="form-control mb-2" ref="post_einverstanden" placeholder="Eingabe?"
              @keypress.enter="postData" />
          </div>
          <div class="input-group input-group-sm mb-2">
            <button class="btn btn-sm btn-primary" @click="postData">
              Eingabe absenden
            </button>
            <button class="btn btn-sm btn-warning ml-2" @click="clearPostOutput">
              Antwort löschen
            </button>
          </div>
          <div v-if="postResult" class="alert alert-secondary mt-2" role="alert">
            <pre>{{ postResult }}</pre>
          </div>
        </div>
      </div>

      <div class="card mt-3">
        <div class="card-header">Mit dem Chatbot reden (POST)</div>
        <div class="card-body">
          <div class="form-group">
            <p>
              Hier muss eine gültige Chat-UUID und ein Text für den Chatbot
              eingegeben werden.
            </p>
            <input v-model="the_new_chat_uuid" type="text" class="form-control mb-2" ref="post2_chat_uuid"
              placeholder="Chat-UUID?" />
            <input type="text" class="form-control mb-2" ref="post2_chat_input"
              placeholder="Deine Nachricht an den Chatbot..." @keypress.enter="post2Data" />
          </div>
          <div class="input-group input-group-sm">
            <button class="btn btn-sm btn-primary" @click="post2Data">
              Nachricht absenden
            </button>
            <button class="btn btn-sm btn-warning ml-2" @click="clear2PostOutput">
              Antwort löschen
            </button>
          </div>
          <div v-if="post2Result" class="alert alert-secondary mt-2" role="alert">
            <pre>{{ post2Result }}</pre>
          </div>
        </div>
      </div>


      <div class="card mt-3">
        <div class="card-header">Chatverlauf</div>
        <div class="card-body">
          <div class="input-group input-group-sm">
            <button class="btn btn-sm btn-danger ml-2" @click="clearChatLog">
              Chatverlauf löschen
            </button>
          </div>
          <div v-if="chatLog" class="mt-2">
            <p class="text-left font-monospace" v-html="chatLog"></p>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import http from "./http-common";

export default {
  name: "App",
  data() {
    return {
      postResult: null,
      post2Result: null,
      chatLog: null,
      the_new_chat_uuid: null,
    };
  },
  methods: {
    fortmatResponse(res) {
      return JSON.stringify(res, null, 2);
    },


    async postData() {
      const postData = {
        agreed: this.$refs.post_einverstanden.value,
      };

      try {
        const res = await http.post("/newchatuuid/", postData, {});

        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };

        this.postResult = this.fortmatResponse(result);
        this.the_new_chat_uuid = res.data['chatuuid'];

      } catch (err) {
        this.postResult = this.fortmatResponse(err.response?.data) || err;
      }
    },

    async post2Data() {
      const post2Data = {
        chatuuid: this.$refs.post2_chat_uuid.value,
        input: this.$refs.post2_chat_input.value,
      };

      try {
        const res = await http.post("/input/", post2Data, {});

        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };

        this.post2Result = this.fortmatResponse(result);
        if (this.chatLog == null) { this.chatLog = ""; }
        this.chatLog = "<b>Eingabe:</b> " + post2Data.input + "<br>\n" + "<b>Antwort:</b> " + res.data['output'] + "<br><br>\n\n" + this.chatLog;

      } catch (err) {
        this.post2Result = this.fortmatResponse(err.response?.data) || err;
      }
    },


    clearChatLog() {
      this.chatLog = null;
    },


    clearPostOutput() {
      this.postResult = null;
    },

    clear2PostOutput() {
      this.post2Result = null;
    },
  },
};
</script>

<style>
#app {
  max-width: 95%;
  margin: auto;
}
</style>
