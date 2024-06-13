import { ProgressBarLocation } from '../../models/ProgressBarLocation';

export default class ProgressBar {
  private end: number;
  private current: number;
  private source: ProgressBarLocation;
  private contentEl: HTMLDivElement;
  private barEl: HTMLDivElement;
  private bounceDirection = 1;

  constructor({
    current,
    end,
    contentEl,
    source,
  }: {
    current: number;
    end: number;
    contentEl: HTMLDivElement;
    source: ProgressBarLocation;
  }) {
    if (current > end) {
      throw new Error(
        'Current must be less than or equal to end for the progress bar.'
      );
    }

    this.source = source;
    this.current = current;
    this.end = end;
    this.contentEl = contentEl;
    this.bounceDirection = 1;

    this.barEl = this.contentEl.createDiv();
    this.barEl.classList.add('loading-bar');

    this.barEl.style.width = `${(current / end) * 100}%`;

    if (source === ProgressBarLocation.Discovery) {
      this.barEl.style.position = 'absolute';
    }

    if (source === ProgressBarLocation.QGPT) {
      this.barEl.style.alignSelf = 'center';
      this.barEl.style.maxWidth = '95%';
    }
  }

  hide() {
    this.barEl.style.display = 'none';
  }

  show() {
    this.barEl.style.display = 'flex';
  }

  resetEnd(end: number) {
    if (this.current >= end) {
      this.current = end;
    }
    this.end = end;
    this.barEl.style.width = `${(this.current / this.end) * 100}%`;
  }

  update({ value }: { value: number }) {
    this.current = value;
    if (this.current > this.end) {
      this.current = this.end;
    }
    this.barEl.style.width = `${(this.current / this.end) * 100}%`;
    this.barEl.title = `Loaded ${this.current} of ${this.end} ${
      this.source === ProgressBarLocation.QGPT ? 'files' : 'snippets'
    }.`;
  }

  getCurrent() {
    return this.current;
  }

  getEnd() {
    return this.end;
  }

  detach() {
    this.contentEl.remove();
  }

  reset() {
    this.current = 0;
    this.barEl.style.width = `${(this.current / this.end) * 100}%`;
  }

  setFinished(current: number) {
    this.current = current;
    this.barEl.style.width = `${(this.current / this.end) * 100}%`;
  }

  bounce() {
    this.animateBounce();
    this.barEl.style.width = `10%`;
  }

  private animateBounce() {
    const animate = () => {
      this.current += this.bounceDirection;

      if (this.current >= this.end) {
        this.bounceDirection = -1;
      } else if (this.current <= 0) {
        this.bounceDirection = 1;
      }

      this.barEl.style.transform = `translate(${
        (this.current / this.end) * 900
      }%)`;

      requestAnimationFrame(animate);
    };

    animate();
  }
}
