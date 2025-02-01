#version 330 core

uniform sampler2D tex;
uniform float time;
uniform vec2 resolution;
uniform bool gravity;
uniform bool speed;

in vec2 uvs;
out vec4 f_color;

float rand(vec2 n) { 
    return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}

float noise(vec2 p){
    return fract(sin(dot(p, vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    vec2 uv = uvs;

    float shake = (noise(vec2(time)) - 0.5) * 0.0009;
    uv.x += shake;
    uv.y += (noise(vec2(time * 0.5)) - 0.5) * 0.0009;

    vec2 offset = vec2(0.001, 0.001); 
    vec4 r = texture(tex, uv + offset * vec2(-1.0, 0.5) * (1.0 + sin(time)) * 1.1);
    vec4 g = texture(tex, uv + offset * vec2(0.0, -0.5) * (1.0 + cos(time*0.8)) * 1.2);
    vec4 b = texture(tex, uv + offset * vec2(1.0, 0.5) * (1.0 + sin(time*1.2)) * 1.3);

    vec3 color = vec3(r.r, g.g, b.b);

    float scanline = sin(uv.y * 1000.0 + time * 10.0) * 0.1;
    color += scanline;

    color *= 0.9 + 0.1 * rand(uv + time);

    vec2 vig = uv - 0.5;
    color *= 1.0 - dot(vig, vig) * 1.5;

    color += (noise(uv * 50.0 + time) - 0.5) * 0.08;

    // Плавное изменение интенсивности цвета с учетом пропадания
    float intensity = (sin(time * 2.0) * 0.5 + 0.5) * exp(-time * 0.1);  // Добавлено экспоненциальное затухание

    // Добавление фиолетового оттенка при активном gravity
    if (gravity) {
        color.r += 138.0 / 255.0 * intensity * 0.05;  // Снижение насыщенности
        color.g += 43.0 / 255.0 * intensity * 0.05;
        color.b += 226.0 / 255.0 * intensity * 0.05;
    }

    // Добавление желтого оттенка при активном speed
    if (speed) {
        color.r += 1.0 * intensity * 0.05;
        color.g += 1.0 * intensity * 0.05;
        color.b += 0.0 * intensity * 0.05;
    }

    f_color = vec4(color, g.a);
}