#version 400 core

in vec2 in_Vector;

uniform float in_InvertY;
uniform mat4 in_ObjPos;

out vec2 pass_TexVec;

void main(void){
    // Position
    //gl_Position = in_ObjPos * vec4(in_Vector, 0.0, 1.0);        // The position of the current vertex on the screen
    gl_Position = vec4(in_Vector, 0.0, 1.0);

    // Texture
    if(in_InvertY > 0.5)pass_TexVec = vec2(in_Vector.x + 0.5, 0.5 - in_Vector.y);
    else pass_TexVec = vec2(in_Vector.x + 0.5, in_Vector.y + 0.5);
}