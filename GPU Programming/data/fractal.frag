// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

uniform float cx;
uniform float cy;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 

  // vec4 diffuse_color = vec4 (1.0, 0.0, 0.0, 1.0);
  // float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);
  // gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);

  float z_re = vertTexCoord.x * 6.28 - 3.14;
  float z_im = vertTexCoord.y * 6.28 - 3.14;

  gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);

  for (int i = 0; i < 20; i++) {
    float sinz_re = sin(z_re) * cosh(z_im);
    float sinz_im = cos(z_re) * sinh(z_im);
    float re_new = cx * sinz_re - cy * sinz_im;
    float im_new = cx * sinz_im + cy * sinz_re;
    z_re = re_new;
    z_im = im_new;

    if (distance(vec2(0, 0), vec2(z_re, z_im)) > 50) {
      gl_FragColor = vec4(1.0, 0, 0, 1.0);
    }
  }

}