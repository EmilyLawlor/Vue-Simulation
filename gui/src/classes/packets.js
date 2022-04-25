export default class PacketVisualistion {
  constructor(x, y, state) {
    this.y = y;
    this.x = x;
    this.width = 8;
    this.height = 15;
    this.canvas = document.getElementById('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.state = state;
    this.render();
  }

  moveDown(dist) {
    this.y += 1;
    this.render('down');
    if (this.y < dist && this.state !== 'lost') {
      requestAnimationFrame(() => {
        this.moveDown(dist);
      });
    } else if (this.state === 'lost') {
      this.ctx.clearRect(this.x, this.y, this.width, this.height);
    }
  }

  moveUp(dist) {
    this.y -= 1;
    this.render('up');
    if (this.y > dist && this.state !== 'lost') {
      requestAnimationFrame(() => {
        this.moveUp(dist);
      });
    } else if (this.state === 'lost') {
      this.ctx.clearRect(this.x, this.y, this.width, this.height);
    }
  }

  render(direction) {
    if (direction === 'down' && this.y > 25) {
      this.ctx.clearRect(this.x, this.y - 1, this.width, this.height);
    } else if (direction === 'up' && this.y < 115) {
      this.ctx.clearRect(this.x, this.y + 1, this.width, this.height);
    }
    // create new rectangle in new location
    if (this.state === 'usable') { this.ctx.fillStyle = 'blue'; }
    if (this.state === 'ACKed') { this.ctx.fillStyle = 'green'; }
    if (this.state === 'error') { this.ctx.fillStyle = 'red'; }
    if (this.state === 'unusable') { this.ctx.fillStyle = 'black'; }
    if (this.state === 'sent') { this.ctx.fillStyle = 'orange'; }
    this.ctx.beginPath();
    this.ctx.rect(this.x, this.y, this.width, this.height);
    this.ctx.fill();
  }

  setState(state) {
    this.state = state;
    this.render(null);
  }
}
