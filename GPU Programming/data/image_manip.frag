// Fragment shader
// The fragment shader is run once for every pixel
// It can change the color and transparency of the fragment.

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXLIGHT_SHADER

// Set in Processing
uniform sampler2D my_texture;
uniform sampler2D my_mask;
uniform float blur_flag;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 

  // grab the color values from the texture and the mask
  vec4 diffuse_color = texture2D(my_texture, vertTexCoord.xy);
  vec4 mask_color = texture2D(my_mask, vertTexCoord.xy);

  vec4 newColor = vec4(0);

    if (blur_flag == 1) {
      if (mask_color[0] + mask_color[1] + mask_color[2] < 0.1) {
        for (int i = -3; i <= 3; i++) {
          for (int j = -3; j <= 3; j++) {
            float x = vertTexCoord.x + (i* 0.005);
            float y = vertTexCoord.y + (j * 0.005);
            vec4 diffuse = texture2D(my_texture, vec2(x, y));
            newColor = newColor + diffuse;
            diffuse_color = newColor / 49;
          }
        }
      } else if ((mask_color[0] + mask_color[1] + mask_color[2]) / 3 >= 0.1 && (mask_color[0] + mask_color[1] + mask_color[2]) / 3 <= 0.5) {
        for (int i = -1; i <= 1; i++) {
          for (int j = -1; j <= 1; j++) {
            float x = vertTexCoord.x + (i * 0.005);
            float y = vertTexCoord.y + (j * 0.005);
            vec4 diffuse = texture2D(my_texture, vec2(x, y));
            newColor = newColor + diffuse;
            diffuse_color = newColor / 9;
          }
        }
      } else {
        diffuse_color = texture2D(my_texture, vertTexCoord.xy);
      }
    }

  // simple diffuse shading model
  float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);

  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
}
