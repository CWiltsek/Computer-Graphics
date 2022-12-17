// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

mat2 rotate(float angle) {
  return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
}

void main() { 

  float x = vertTexCoord.s;
  float y = vertTexCoord.t;
  vec2 st = vec2(vertTexCoord.s, vertTexCoord.t);
  float d = 0.04; // distance between
  float h = 0.175 / 2; // half width and height
  float m = 0.5; // middle
  
  st -= vec2(0.5);
  st = rotate(0.785398) * st;
  st += vec2(0.5);

  gl_FragColor = vec4(0.2, 1.0, 1.0, 1.0);

  for (int i = -2; i < 3; i++) {
    
    if (st[0] > m - h && st[0] < m + h && st[1] > m - (1 + 2 * i) * h - i * d && st[1] < m + (-2 * i * h) + h - i * d) {
      gl_FragColor = vec4(0.2, 1.0, 1.0, 0);
    }

    if (st[0] > m - (1 + 2 * i) * h - i * d && st[0] < m + (-2 * i * h) + h - i * d && st[1] > m - h && st[1] < m + h) {
      gl_FragColor = vec4(0.2, 1.0, 1.0, 0);
    }
  }

  if (st[0] > m + h + d && st[0] < m + 3 * h + d && st[1] > m - 3 * h - d && st[1] < m - h - d) {
    gl_FragColor = vec4(0.2, 1.0, 1.0, 0);
  }

  if (st[0] > m + h + d && st[0] < m + 3 * h + d && st[1] > m + h + d && st[1] < m + 3 * h + d) {
    gl_FragColor = vec4(0.2, 1.0, 1.0, 0);
  }

  if (st[0] > m - 3 * h - d && st[0] < m - h - d && st[1] > m - 3 * h - d && st[1] < m - h - d) {
    gl_FragColor = vec4(0.2, 1.0, 1.0, 0);
  }

  if (st[0] > m - 3 * h - d && st[0] < m - h - d && st[1] > m + h + d && st[1] < m + 3 * h + d) {
    gl_FragColor = vec4(0.2, 1.0, 1.0, 0);
  }

}