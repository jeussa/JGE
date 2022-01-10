#version 400 core

in vec2 pass_TexVec;

uniform sampler2D in_Texture;

out vec4 gl_FragColor;

void main(void){
    // Texture
    //out_Color = texture2D(in_Texture, pass_TexVec);
    //if(out_Color.a < 0.5)discard;
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}