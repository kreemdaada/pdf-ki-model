<template>
  <div>
    <h2>Datei hochladen</h2>
    <form @submit.prevent="uploadFile">
      <input type="file" @change="onFileChange" accept=".csv, .json" />
      <button type="submit" :disabled="loading">
        {{ loading ? "Hochladen..." : "Hochladen" }}
      </button>
    </form>

    <div v-if="uploadStatus">
      <p>{{ uploadStatus }}</p>
      <button v-if="pdfLinks.length > 0" @click="goToGeneratedPDFs">Generierte PDFs anzeigen</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      uploadStatus: "",
      loading: false,
      pdfLinks: [],
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      const allowedExtensions = ["csv", "json"];
      const fileExtension = file.name.split(".").pop().toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        this.uploadStatus = "Nur CSV- und JSON-Dateien sind erlaubt.";
        this.selectedFile = null;
        return;
      }

      this.selectedFile = file;
      this.uploadStatus = ""; // Status zurücksetzen
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.uploadStatus = "Bitte wählen Sie eine Datei aus!";
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      this.loading = true;
      try {
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        if (response.data && response.data.pdf_links) {
          this.uploadStatus = "Datei erfolgreich hochgeladen!";
          this.pdfLinks = response.data.pdf_links;
          this.cachePDFLinks(this.pdfLinks); // Speichere die Links im Cache
        } else {
          this.uploadStatus = "Verarbeitung abgeschlossen, aber keine Links gefunden.";
        }
      } catch (error) {
        console.error("Fehler beim Hochladen:", error);
        this.uploadStatus = "Fehler beim Hochladen oder Verarbeiten der Datei.";
      } finally {
        this.loading = false;
      }
    },
    goToGeneratedPDFs() {
      this.$router.push({ path: "/generated-pdfs" });
    },
    cachePDFLinks(links) {
      const cacheData = {
        links,
        timestamp: Date.now(),
      };
      localStorage.setItem("cachedPDFLinks", JSON.stringify(cacheData));
    },
  },
};
</script>
