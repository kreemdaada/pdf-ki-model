<template>
  <nav class="navbar">
    <h1>PDF KI-Generator</h1>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/upload">Upload</a></li>
      <li><a href="/generated-pdfs">Generated PDFs</a></li>
    </ul>
  </nav>
</template>

<script>
export default {};
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  background-color: #2c3e50;
  padding: 1rem;
  color: white;
}
.navbar ul {
  list-style: none;
  display: flex;
  gap: 1rem;
}
.navbar a {
  color: white;
  text-decoration: none;
}
</style>
