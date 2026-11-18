// Render a view into an equirectangular image without flattening the panorama.
const vertexSource = `
attribute vec2 position;
varying vec2 screen;
void main() {
  screen = position;
  gl_Position = vec4(position, 0., 1.);
}`;

const fragmentSource = `
precision mediump float;
uniform sampler2D panorama;
uniform vec3 forward;
uniform vec3 right;
uniform vec3 up;
uniform vec2 spread;
varying vec2 screen;
const float PI = 3.14159265359;
void main() {
  vec3 ray = normalize(forward + screen.x * spread.x * right + screen.y * spread.y * up);
  float u = fract(atan(ray.x, ray.z) / (2. * PI) + .5);
  float v = .5 - asin(clamp(ray.y, -1., 1.)) / PI;
  gl_FragColor = texture2D(panorama, vec2(u, v));
}`;

export function createPanorama(canvas) {
  const gl = canvas.getContext('webgl', { alpha: false, antialias: false });
  if (!gl) return null;

  const program = gl.createProgram();
  for (const [kind, source] of [[gl.VERTEX_SHADER, vertexSource], [gl.FRAGMENT_SHADER, fragmentSource]]) {
    const shader = gl.createShader(kind);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) return null;
    gl.attachShader(program, shader);
    gl.deleteShader(shader);
  }
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return null;
  gl.useProgram(program);

  const vertices = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vertices);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const position = gl.getAttribLocation(program, 'position');
  gl.enableVertexAttribArray(position);
  gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

  const texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  const uniforms = Object.fromEntries(['forward', 'right', 'up', 'spread']
    .map(name => [name, gl.getUniformLocation(program, name)]));

  function draw(yaw, pitch) {
    const scale = Math.min(devicePixelRatio || 1, 2);
    const width = Math.round(canvas.clientWidth * scale);
    const height = Math.round(canvas.clientHeight * scale);
    if (!width || !height) return null;
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      gl.viewport(0, 0, width, height);
    }
    const sy = Math.sin(yaw), cy = Math.cos(yaw);
    const sp = Math.sin(pitch), cp = Math.cos(pitch);
    const forward = [sy * cp, sp, cy * cp];
    const right = [cy, 0, -sy];
    const up = [-sy * sp, cp, -cy * sp];
    const halfHeight = .69;
    const halfWidth = halfHeight * width / height;
    gl.uniform3fv(uniforms.forward, forward);
    gl.uniform3fv(uniforms.right, right);
    gl.uniform3fv(uniforms.up, up);
    gl.uniform2f(uniforms.spread, halfWidth, halfHeight);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    return { forward, right, up, halfWidth, halfHeight };
  }

  return {
    draw,
    load(image) {
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
    },
  };
}
