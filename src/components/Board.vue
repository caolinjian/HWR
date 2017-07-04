<template lang="html">
    <div  class="clearfix">
        <div class="board" @mousedown="handleMousedown($event)">
            <div class="board-row" v-for="(boardRow, i) in data" >
                <div class="board-item"  v-for="(boardItem, j) in boardRow" :row="i" :col="j" :style="{background:data[i][j]==0?'#fff':'#333'}"></div>
            </div>
        </div>
        <button @click="clear">clear</button>
        <button @click="send">send</button>
        <span>{{result}}</span>
    </div>
</template>

<script>
function getDefaultData() {
  return new Array(32).fill(0).map(() => {
    return new Array(32).fill(0)
  })
}
const DefaultData = getDefaultData();
export default {
  data() {
    return {
      data: DefaultData,
      writing: false,
      result: ''
    }
  },
  methods: {
    handleMousedown(ev) {
      this.writing = true;
      const self = this;

      const $board = ev.currentTarget;
      let startX = parseInt(ev.target.getAttribute('row'), 10);
      let startY = parseInt(ev.target.getAttribute('col'), 10);

      function drawline(endX, endY) {
        if (!startX || !startY) {
          startX = endX;
          startY = endY;
        }
        if (startX == endX) {
          for (let i = startY; i != endY; i += (startY > endY ? -1 : 1)) {
            self.setData(endX, i, 1);
          }
          startX = endX;
          startY = endY;
          return
        } else if (startY == endY) {
          for (let i = startX; i != endX; i += (startX > endX ? -1 : 1)) {
            self.setData(i, endY, 1);
          }
          startX = endX;
          startY = endY;
          return
        }
        const XLen = Math.abs(endX - startX) + 1;
        const YLen = Math.abs(endY - startY) + 1;
        const rect = [];
        const XDirect = startX < endX;
        const YDirect = startY < endY;

        if (XLen < YLen) {
          let y = 1;
          for (let j = 0; j < YLen; j++) {
            const x = j * XLen / YLen;
            if (x > y) {
              rect.push([y, y * YLen / XLen]);
              y++;
              rect.push([x, j]);
            } else {
              rect.push([x, j]);
            }
          }
        } else {
          let x = 1;
          for (let i = 0; i < XLen; i++) {
            const y = i * YLen / XLen;
            if (y > x) {
              rect.push([x * XLen / YLen, x]);
              x++;
              rect.push([i, y]);
            } else {
              rect.push([i, y]);
            }
          }
        }

        self.setData(startX, startY, 1);
        for (let i = 1; i < rect.length; i++) {
          if ((rect[i][0] - rect[i - 1][0]) * (rect[i][1] - rect[i - 1][1]) >= 1 / 4) {
            self.setData(self.data[Math.floor(rect[i][0]) * (XDirect ? 1 : -1) + startX], Math.floor(rect[i][1]) * (YDirect ? 1 : -1) + startY, 1);
          }
        }
        self.setData(endX, endY, 1);
        startX = endX;
        startY = endY;
      }
      const handleMouseover = (event) => {
        if (event.target.className == 'board-item') {
          const endX = parseInt(event.target.getAttribute('row'), 10);
          const endY = parseInt(event.target.getAttribute('col'), 10);
          drawline(endX, endY)
        }
      };


      const handleMouseleaveOrMouseUp = () => {
        $board.removeEventListener('mousemove', handleMouseover);
        $board.removeEventListener('mouseup', handleMouseleaveOrMouseUp);
        $board.removeEventListener('mouseleave', handleMouseleaveOrMouseUp);
      };
      $board.addEventListener('mousemove', handleMouseover);
      $board.addEventListener('mouseup', handleMouseleaveOrMouseUp);
      $board.addEventListener('mouseleave', handleMouseleaveOrMouseUp);
    },
    setData(x, y) {
      // 加粗 3倍
      for (let i = x - 1; i <= x + 1; i++) {
        if (i >= 0 && i < 32) {
          for (let j = y - 1; j <= y + 1; j++) {
            if (j >= 0 && j < 32) {
              this.$set(this.data[i], j, 1);
            }
          }
        }
      }
    },

    clear() {
      this.data = getDefaultData();
      const canvas = document.querySelector('canvas');
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, 300, 300);
    },
    send() {
      const self = this;
      self.result = 'Reckoning...'
      window.fetch('/recognition', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          data: self.data
        })
      }).then((res) => {
        if (res.ok) {
          return res.json();
        }
        throw new Error('Network response was not ok.');
      }).then((json) => {
        self.result = json.test
      }).catch((error) => {
        console.log(`There has been a problem with your fetch operation:  ${error.message}`);
      });
    }
  }
}
</script>

<style lang="css">
    .board{
        border:1px solid #eee;
        width: 160px;
        margin: 50px 0 20px 120px;
        float: left;
    }
    .board-row{
        font-size: 0;
        width: 160px;
    }
    .board-item{
        display: inline-block;
        width: 5px;
        height: 5px;
        background: #fff;
    }
    canvas{
        border:1px solid #eee;
        width: 160px;
        height: 160px;
        margin: 50px 0 20px 120px;
        float: left;
    }
</style>
