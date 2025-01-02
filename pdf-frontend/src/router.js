import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import FileUpload from './components/FileUpload.vue';
import GeneratedPDFs from './components/GeneratedPDFs.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/upload', component: FileUpload },
  { path: '/generated-pdfs', component: GeneratedPDFs },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
