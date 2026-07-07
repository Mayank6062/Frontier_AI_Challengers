require('@testing-library/jest-dom');

// Provide a minimal canvas getContext implementation for axe-core in jsdom
try {
  HTMLCanvasElement.prototype.getContext = function () {
    return {
      fillRect: () => {},
      clearRect: () => {},
      getImageData: (x, y, w, h) => ({ data: new Array(w * h * 4) }),
      putImageData: () => {},
      createImageData: () => [],
      setTransform: () => {},
      drawImage: () => {},
      save: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      closePath: () => {},
      stroke: () => {},
      translate: () => {},
      scale: () => {},
      rotate: () => {},
      arc: () => {},
      fillText: () => {},
      measureText: () => ({ width: 0 }),
    };
    };
} catch (e) {
  // ignore if HTMLCanvasElement is not available in this environment
}

// silence jsdom missing features warnings in tests
global.HTMLElement.prototype.scrollIntoView = function(){};
