<template>
  <div id="app">
    <h1>HandWriting Recognition</h1>
    <Board></Board>
  </div>
</template>

<script>
import Board from './components/Board';

export default {
  name: 'app',
  components: {
    Board,
  },
};
</script>

<style>
html,body{
    width: 100%;
    height: 100%;
    margin: 0;
    font-size: 60px;
    user-select:none;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 20px;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}
h1{
    font-size: 30px;
    margin: 0 auto 20px;
}
</style>
