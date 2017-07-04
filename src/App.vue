<template>
<div id="app">
  <h1>HandWriting Recognition</h1>
  <h2>Simple KNN</h2>
  <Board></Board>
  <h2>canvas to png  todo...</h2>
  <canvas width="160" height="160" @mousedown="drawCanvas($event)"></canvas>
</div>
</template>

<script>
import Board from './components/Board';

export default {
  name: 'app',
  components: {
    Board,
  },
  methods: {
    drawCanvas(ev) {
      const canvas = document.querySelector('canvas');
      const context = canvas.getContext('2d');
      let startX;
      let startY;
      let endX;
      let endY;
      startX = ev.offsetX;
      startY = ev.offsetY;
      const handleMouseover = function(e) {
        endX = e.offsetX;
        endY = e.offsetY;
        context.beginPath()
        context.moveTo(startX, startY);
        context.lineTo(endX, endY);
        context.lineWidth = 15;
        context.strokeStyle = '#000';
        context.stroke();
        context.closePath()
        startX = endX;
        startY = endY;
      }
      const handleMouseleaveOrMouseUp = () => {
        canvas.removeEventListener('mousemove', handleMouseover);
        canvas.removeEventListener('mouseup', handleMouseleaveOrMouseUp);
        canvas.removeEventListener('mouseleave', handleMouseleaveOrMouseUp);
      };
      canvas.addEventListener('mousemove', handleMouseover);
      canvas.addEventListener('mouseup', handleMouseleaveOrMouseUp);
      canvas.addEventListener('mouseleave', handleMouseleaveOrMouseUp);
    },
  }
};
</script>

<style>
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  font-size: 60px;
  user-select: none;
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

h1 {
  font-size: 30px;
  margin: 0 auto 20px;
}

h2 {
  font-size: 25px;
  margin: 20px 120px;
  text-align: left;
}

.clearfix:after {
  content: ' ';
  display:table;
  clear: both;
}
</style>
