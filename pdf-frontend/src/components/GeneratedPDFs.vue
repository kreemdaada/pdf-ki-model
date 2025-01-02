<template>
  <div>
    <h2>Generierte PDFs</h2>
    <div v-if="sessions.length > 0">
      <div v-for="(session, index) in sessions" :key="index">
        <h3>Sitzung {{ index + 1 }}</h3>
        <ul>
          <li v-for="(link, idx) in session" :key="idx">
            <a :href="link" target="_blank">PDF {{ idx + 1 }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <p>Keine PDFs verfügbar. Bitte laden Sie zuerst eine Datei hoch.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sessions: [],
    };
  },
  mounted() {
    this.loadCachedPDFLinks();
  },
  methods: {
    loadCachedPDFLinks() {
      const cachedData = localStorage.getItem("cachedPDFLinks");
      if (cachedData) {
        const { links, timestamp } = JSON.parse(cachedData);
        const oneHour = 60 * 60 * 1000;

        // Prüfe, ob der Cache noch gültig ist
        if (Date.now() - timestamp < oneHour) {
          this.sessions.push(links);
        } else {
          localStorage.removeItem("cachedPDFLinks");
        }
      }
    },
  },
};
</script>
