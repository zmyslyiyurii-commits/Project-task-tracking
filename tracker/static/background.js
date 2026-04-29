import { Renderer, Program, Mesh, Color, Triangle } from 'https://cdn.skypack.dev/ogl';

const vertexShader = `
attribute vec2 uv;
attribute vec2 position;
varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = vec4(position, 0, 1);
}`;

const fragmentShader = `
precision highp float;
uniform float uTime;
uniform vec3 uColor;
uniform vec3 uResolution;
uniform vec2 uMouse;
uniform float uAmplitude;
uniform float uSpeed;
varying vec2 vUv;
void main() {
    float mr = min(uResolution.x, uResolution.y);
    vec2 uv = (vUv.xy * 2.0 - 1.0) * uResolution.xy / mr;
    uv += (uMouse - vec2(0.5)) * uAmplitude;
    float d = -uTime * 0.5 * uSpeed;
    float a = 0.0;
    for (float i = 0.0; i < 8.0; ++i) {
        a += cos(i - d - a * uv.x);
        d += sin(uv.y * i + a);
    }
    d += uTime * 0.5 * uSpeed;
    vec3 col = vec3(cos(uv * vec2(d, a)) * 0.6 + 0.4, cos(a + d) * 0.5 + 0.5);
    col = cos(col * cos(vec3(d, a, 2.5)) * 0.5 + 0.5) * uColor;
    gl_FragColor = vec4(col, 1.0);
}`;

function initIridescence() {
    const container = document.getElementById('iridescence-bg');
    if (!container) return;

    const renderer = new Renderer();
    const gl = renderer.gl;
    container.appendChild(gl.canvas);

    const color = [0.5, 0.6, 0.8];
    const speed = 1.0;
    const amplitude = 0.1;
    let program;

    // ВИПРАВЛЕНО: Тепер беремо розміри вікна, а не контейнера
    function resize() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        renderer.setSize(width, height);
        
        if (program) {
            program.uniforms.uResolution.value = new Color(
                width,
                height,
                width / height
            );
        }
    }

    window.addEventListener('resize', resize);
    const geometry = new Triangle(gl);
    program = new Program(gl, {
        vertex: vertexShader,
        fragment: fragmentShader,
        uniforms: {
            uTime: { value: 0 },
            uColor: { value: new Color(...color) },
            uResolution: { value: new Color() },
            uMouse: { value: new Float32Array([0.5, 0.5]) },
            uAmplitude: { value: amplitude },
            uSpeed: { value: speed }
        }
    });

    resize();
    const mesh = new Mesh(gl, { geometry, program });

    function update(t) {
        requestAnimationFrame(update);
        program.uniforms.uTime.value = t * 0.001;
        renderer.render({ scene: mesh });
    }

    window.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = 1.0 - (e.clientY / window.innerHeight);
        program.uniforms.uMouse.value[0] = x;
        program.uniforms.uMouse.value[1] = y;
    });

    requestAnimationFrame(update);
}

// Запускаємо після завантаження всього документа
if (document.readyState === 'complete') {
    initIridescence();
} else {
    document.addEventListener('DOMContentLoaded', initIridescence);
}