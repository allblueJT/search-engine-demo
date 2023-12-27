<template>
  <router-view></router-view>
</template>

<script>
</script>

<style scoped>
.title {
  display: flex;
  justify-content: center;
  caret-color: rgba(0, 0, 0, 0);
  margin-top: 150px;
}

.search-container {
  text-align: center;
  padding: 20px;
  caret-color: rgba(0, 0, 0, 0)
}

.search-box {
  display: inline-block;
  margin-top: 20px;
  caret-color: rgba(0, 0, 0, 0)
}

.search-input {
  height: 30px;
  width: 600px;
  padding: 10px;
  padding-left: 20px;
  margin-right: -4px;
  /* Remove space between input and button */
  border: 1px solid #dfe1e5;
  border-radius: 24px 0 0 24px;
  outline: none;
}

.search-input:focus {
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-color: rgba(223, 225, 229, 0);
}

.text {
  display: flex;
  justify-content: center;
}

.search-button {
  height: 55px;
  width: 100px;
  background-color: #b3d5f7;
  border: 1px solid #f8f9fa;
  border-left: none;
  border-radius: 0 24px 24px 0;
  color: #000000;
  text-align: center;
  line-height: 46px;
  outline: none;
  cursor: pointer;
  font-size: medium;
  font-weight: 500;
}

.search-button:hover {
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  background-color: #f8f9fa;
  border-color: #c6c6c6;
}

.search-results {
  margin-top: 20px;
  text-align: left;
  text-align: left;
  width: 500px;
  margin-left: auto;
  margin-right: auto;
  caret-color: rgba(0, 0, 0, 0)
}

.search-item {
  padding: 10px;
  list-style-type: none;
  border-bottom: 1px solid #eee;
}

.no-results {
  margin-top: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
  text-align: center;
  caret-color: rgba(0, 0, 0, 0)
}
</style>
