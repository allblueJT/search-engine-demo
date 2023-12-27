<template>
  <div class="title">
    <img src="@/assets/Noodle Search.jpg" alt="logo" style="height: 100px;margin-top: auto;margin-bottom: auto;" />
    <div class="text">
      <p style="color: #ffba18;;line-height: 16px; font-size: 60px;margin-left: 20px;font-family: fantasy">N</p>
      <p style="margin-left: 3px;color: #ff6a2b;line-height: 16px;font-size: 60px;font-family: fantasy">O</p>
      <p style="margin-left: 3px;color: #0d9782;line-height: 16px;font-size: 60px;font-family: fantasy">O</p>
      <p style="margin-left: 3px;color: #00dfc5;line-height: 16px;font-size: 60px;font-family: fantasy">D</p>
      <p style="margin-left: 3px;color: #255fb1;line-height: 16px;font-size: 60px;font-family: fantasy">L</p>
      <p style="margin-left: 3px;color: #992df7;line-height: 16px;font-size: 60px;font-family: fantasy">E</p>
      <p style="margin-left: 20px;color: #c30a76;line-height: 16px;font-size: 60px;font-family: fantasy">S</p>
      <p style="margin-left: 3px;color: #4e068d;line-height: 16px;font-size: 60px;font-family: fantasy">E</p>
      <p style="margin-left: 3px;color: #757ff3;line-height: 16px;font-size: 60px;font-family: fantasy">A</p>
      <p style="margin-left: 3px;color: #fe0b0b;line-height: 16px;font-size: 60px;font-family: fantasy">R</p>
      <p style="margin-left: 3px;color: #a1a100;line-height: 16px;font-size: 60px;font-family: fantasy">C</p>
      <p style="margin-left: 3px;color: #f72d63;line-height: 16px;font-size: 60px;font-family: fantasy">H</p>
    </div>
  </div>
  <div class="search-container">
    <div class="search-box">
      <input v-model="searchQuery" type="text" placeholder="Search..." class="search-input" />
      <button @click="performSearch" class="search-button">SEARCH</button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
// ... 之前的脚本代码保持不变
export default {
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    const performSearch = () => {
      router.push({ path: '/result', query: { msg: searchQuery.value } })
    }
    return {
      performSearch,
      searchQuery,
    }
  },
};
</script>

<style scoped>
.title {
  display: flex;
  justify-content: center;
  caret-color: rgba(0, 0, 0, 0);
  margin-top: 250px;
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
