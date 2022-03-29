export default class Packet {
  constructor(x, y) {
    this.y = y;
    this.x = x;
    this.state = 'waiting';
    this.canvas = document.getElementById('canvas');
    this.ctx = this.canvas.getContext('2d');
    if (this.state === 'waiting') { this.ctx.fillStyle = 'blue'; }
    this.render();
  }

  moveDown(dist) {
    this.y += 1;
    this.render();
    if (this.y < dist) {
      requestAnimationFrame(() => {
        this.moveDown(dist);
      });
    }
  }

  moveUp(dist) {
    this.y -= 1;
    this.render();
    if (this.y > dist) {
      requestAnimationFrame(() => {
        this.moveUp(dist);
      });
    }
  }

  render() {
    // delete previous rectangle
    this.ctx.clearRect(this.x, this.y - 1, 12, 25);
    // create new rectangle in new location
    if (this.state === 'waiting') { this.ctx.fillStyle = 'blue'; }
    if (this.state === 'ACKed') { this.ctx.fillStyle = 'green'; }
    if (this.state === 'error') { this.ctx.fillStyle = 'red'; }
    this.ctx.beginPath();
    this.ctx.rect(this.x, this.y, 8, 15);
    this.ctx.fill();
  }

  setState(state) {
    this.state = state;
  }
}
