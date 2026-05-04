import { Renderer, Program, Mesh, Plane } from 'https://cdn.jsdelivr.net/npm/ogl@0.0.32/dist/ogl.mjs';

const hexToRgb = hex => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!result) return [1, 1, 1];
    return [parseInt(result[1], 16) / 255, parseInt(result[2], 16) / 255, parseInt(result[3], 16) / 255];
};

const vertex = `#version 300 es
in vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }`;

const fragment = `#version 300 es
precision highp float;
uniform vec2 iResolution; uniform float iTime; uniform float uTimeSpeed;
uniform float uColorBalance; uniform float uWarpStrength; uniform float uWarpFrequency;
uniform float uWarpSpeed; uniform float uWarpAmplitude; uniform float uBlendAngle;
uniform float uBlendSoftness; uniform float uRotationAmount; uniform float uNoiseScale;
uniform float uGrainAmount; uniform float uGrainScale; uniform float uGrainAnimated;
uniform float uContrast; uniform float uGamma; uniform float uSaturation;
uniform vec2 uCenterOffset; uniform float uZoom; uniform vec3 uColor1;
uniform vec3 uColor2; uniform vec3 uColor3;
out vec4 fragColor;
#define S(a,b,t) smoothstep(a,b,t)
mat2 Rot(float a){float s=sin(a),c=cos(a);return mat2(c,-s,s,c);}
vec2 hash(vec2 p){p=vec2(dot(p,vec2(2127.1,81.17)),dot(p,vec2(1269.5,283.37)));return fract(sin(p)*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p),u=f*f*(3.0-2.0*f);float n=mix(mix(dot(-1.0+2.0*hash(i+vec2(0.0,0.0)),f-vec2(0.0,0.0)),dot(-1.0+2.0*hash(i+vec2(1.0,0.0)),f-vec2(1.0,0.0)),u.x),mix(dot(-1.0+2.0*hash(i+vec2(0.0,1.0)),f-vec2(0.0,1.0)),dot(-1.0+2.0*hash(i+vec2(1.0,1.0)),f-vec2(1.0,1.0)),u.x),u.y);return 0.5+0.5*n;}
void mainImage(out vec4 o, vec2 C){
    float t=iTime*uTimeSpeed; vec2 uv=C/iResolution.xy; float ratio=iResolution.x/iResolution.y;
    vec2 tuv=uv-0.5+uCenterOffset; tuv/=max(uZoom,0.001);
    float degree=noise(vec2(t*0.1,tuv.x*tuv.y)*uNoiseScale);
    tuv.y*=1.0/ratio; tuv*=Rot(radians((degree-0.5)*uRotationAmount+180.0)); tuv.y*=ratio;
    float frequency=uWarpFrequency; float ws=max(uWarpStrength,0.001); float amplitude=uWarpAmplitude/ws;
    float warpTime=t*uWarpSpeed; tuv.x+=sin(tuv.y*frequency+warpTime)/amplitude; tuv.y+=sin(tuv.x*(frequency*1.5)+warpTime)/(amplitude*0.5);
    float b=uColorBalance; float s=max(uBlendSoftness,0.0); mat2 blendRot=Rot(radians(uBlendAngle));
    float blendX=(tuv*blendRot).x; float edge0=-0.3-b-s; float edge1=0.2-b+s;
    vec3 layer1=mix(uColor3,uColor2,S(edge0,edge1,blendX)); vec3 layer2=mix(uColor2,uColor1,S(edge0,edge1,blendX));
    vec3 col=mix(layer1,layer2,S(0.5-b+s,-0.3-b-s,tuv.y));
    vec2 grainUv=uv*max(uGrainScale,0.001); if(uGrainAnimated>0.5){grainUv+=vec2(iTime*0.05);}
    float grain=fract(sin(dot(grainUv,vec2(12.9898,78.233)))*43758.5453); col+=(grain-0.5)*uGrainAmount;
    col=(col-0.5)*uContrast+0.5; float luma=dot(col,vec3(0.2126,0.7152,0.0722));
    col=mix(vec3(luma),col,uSaturation); col=pow(max(col,0.0),vec3(1.0/max(uGamma,0.001)));
    o=vec4(clamp(col,0.0,1.0),1.0);
}
void main(){ vec4 o; mainImage(o,gl_FragCoord.xy); fragColor=o; }`;

export function initGrainient(container, props = {}) {
    const renderer = new Renderer({ webgl: 2, alpha: true });
    const gl = renderer.gl;
    container.appendChild(gl.canvas);
    const geometry = new Plane(gl, { width: 2, height: 2 });
    const program = new Program(gl, {
        vertex, fragment,
        uniforms: {
            iTime: { value: 0 }, iResolution: { value: new Float32Array([1, 1]) },
            uTimeSpeed: { value: props.timeSpeed || 0.25 },
            uColorBalance: { value: props.colorBalance || 0 },
            uWarpStrength: { value: props.warpStrength || 1 },
            uWarpFrequency: { value: props.warpFrequency || 5 },
            uWarpSpeed: { value: props.warpSpeed || 2 },
            uWarpAmplitude: { value: props.warpAmplitude || 50 },
            uBlendAngle: { value: props.blendAngle || 0 },
            uBlendSoftness: { value: props.blendSoftness || 0.05 },
            uRotationAmount: { value: props.rotationAmount || 500 },
            uNoiseScale: { value: props.noiseScale || 2 },
            uGrainAmount: { value: props.grainAmount || 0.1 },
            uGrainScale: { value: props.grainScale || 2 },
            uGrainAnimated: { value: props.grainAnimated ? 1.0 : 0.0 },
            uContrast: { value: props.contrast || 1.5 },
            uGamma: { value: props.gamma || 1 },
            uSaturation: { value: props.saturation || 1 },
            uCenterOffset: { value: new Float32Array([props.centerX || 0, props.centerY || 0]) },
            uZoom: { value: props.zoom || 0.9 },
            uColor1: { value: new Float32Array(hexToRgb(props.color1 || '#FF9FFC')) },
            uColor2: { value: new Float32Array(hexToRgb(props.color2 || '#5227FF')) },
            uColor3: { value: new Float32Array(hexToRgb(props.color3 || '#B497CF')) }
        }
    });
    const mesh = new Mesh(gl, { geometry, program });
    const resize = () => {
        renderer.setSize(container.offsetWidth, container.offsetHeight);
        program.uniforms.iResolution.value[0] = gl.drawingBufferWidth;
        program.uniforms.iResolution.value[1] = gl.drawingBufferHeight;
    };
    window.addEventListener('resize', resize);
    resize();
    const update = t => {
        program.uniforms.iTime.value = t * 0.001;
        renderer.render({ scene: mesh });
        requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
}