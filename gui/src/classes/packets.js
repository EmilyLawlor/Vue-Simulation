export default class Packet {
  constructor(x, y, state) {
    this.y = y;
    this.x = x;
    this.width = 8;
    this.height = 15;
    this.canvas = document.getElementById('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.state = state;
    if (this.state === 'waiting') { this.ctx.fillStyle = 'blue'; }
    this.render();
  }

  moveDown(dist) {
    this.y += 1;
    this.render('down');
    if (this.y < dist) {
      requestAnimationFrame(() => {
        this.moveDown(dist);
      });
    }
  }

  moveUp(dist) {
    this.y -= 1;
    this.render('up');
    if (this.y > dist) {
      requestAnimationFrame(() => {
        this.moveUp(dist);
      });
    }
  }

  render(direction) {
    if (direction === 'down' && this.y > 25) {
      this.ctx.clearRect(this.x, this.y - 1, this.width, this.height);
    } else if (direction === 'up' && this.y < 115) {
      this.ctx.clearRect(this.x, this.y + 1, this.width, this.height);
    }
    // create new rectangle in new location
    if (this.state === 'waiting') { this.ctx.fillStyle = 'blue'; }
    if (this.state === 'ACKed') { this.ctx.fillStyle = 'green'; }
    if (this.state === 'error') { this.ctx.fillStyle = 'red'; }
    if (this.state === 'lost') { this.ctx.fillStyle = 'white'; }
    this.ctx.beginPath();
    this.ctx.rect(this.x, this.y, this.width, this.height);
    this.ctx.fill();
  }

  setState(state) {
    this.state = state;
  }
}
