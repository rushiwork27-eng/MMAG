/* =====================================================================
   MMAG website: Three.js scenes (unminified)
   One shared WebGL renderer draws every [data-scene] element into its
   on-screen rectangle (scissor rendering). All geometry is generated in
   code: no image files, no textures from disk.
   Scenes: momentum · ribbons · helix · pillars · pointsText · globe ·
           wave · shards · stack · knot · rings · confetti · tunnel
   ===================================================================== */
(function () {
  "use strict";

  var CFG = window.MMAG_CONFIG || {};
  var elements = Array.prototype.slice.call(document.querySelectorAll("[data-scene]"));
  var canvas = document.getElementById("gl");
  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!elements.length || !canvas) return;

  function hasWebGL() {
    try {
      var c = document.createElement("canvas");
      return !!(c.getContext("webgl2") || c.getContext("webgl"));
    } catch (e) {
      return false;
    }
  }

  if (!hasWebGL()) {
    root.classList.add("no-webgl");
    return;
  }

  var fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();

  Promise.all([import(CFG.threeUrl), fontsReady])
    .then(function (result) { start(result[0]); })
    .catch(function (error) {
      console.warn("[MMAG] 3D disabled:", error);
      root.classList.add("no-webgl");
    });

  /* ------------------------------------------------------------------ */
  /* helpers                                                             */
  /* ------------------------------------------------------------------ */
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function smooth(a, b, v) { var t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); }
  function rng(seed) {
    var s = seed >>> 0;
    return function () {
      s += 0x6D2B79F5;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function themeOf(el) {
    var node = el;
    while (node && node !== document.body) {
      var m = (node.className && typeof node.className === "string") ? node.className.match(/\bt-(light|paper2|dark|purple|deep|yellow)\b/) : null;
      if (m) return m[1];
      node = node.parentElement;
    }
    return "dark";
  }
  var PALETTES = {
    dark:   { a: "#54078B", b: "#B98CE8", c: "#F3C01F", d: "#FFFFFF" },
    deep:   { a: "#54078B", b: "#C9A2EE", c: "#F3C01F", d: "#FFFFFF" },
    purple: { a: "#2A0548", b: "#D6B8F5", c: "#F3C01F", d: "#FFFFFF" },
    light:  { a: "#54078B", b: "#9B4FDB", c: "#F3C01F", d: "#171717" },
    paper2: { a: "#54078B", b: "#9B4FDB", c: "#F3C01F", d: "#171717" },
    yellow: { a: "#54078B", b: "#2A0548", c: "#FFFFFF", d: "#171717" }
  };
  function fibonacciSphere(n, r) {
    var out = new Float32Array(n * 3);
    var golden = Math.PI * (3 - Math.sqrt(5));
    for (var i = 0; i < n; i++) {
      var y = 1 - (i / (n - 1)) * 2;
      var rad = Math.sqrt(1 - y * y);
      var th = golden * i;
      out[i * 3] = Math.cos(th) * rad * r;
      out[i * 3 + 1] = y * r;
      out[i * 3 + 2] = Math.sin(th) * rad * r;
    }
    return out;
  }

  /* simplex noise (Ashima Arts, MIT) */
  var NOISE = [
    "vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}",
    "vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}",
    "vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}",
    "vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}",
    "float snoise(vec3 v){",
    "  const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0);",
    "  vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);",
    "  vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);",
    "  vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy;",
    "  i=mod289(i);",
    "  vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));",
    "  float n_=0.142857142857; vec3 ns=n_*D.wyz-D.xzx;",
    "  vec4 j=p-49.0*floor(p*ns.z*ns.z); vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_);",
    "  vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y);",
    "  vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);",
    "  vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0));",
    "  vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;",
    "  vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);",
    "  vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));",
    "  p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;",
    "  vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m;",
    "  return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));",
    "}"
  ].join("\n");

  /* ------------------------------------------------------------------ */
  /* materials                                                           */
  /* ------------------------------------------------------------------ */
  function iridMaterial(THREE, colors, opts) {
    opts = opts || {};
    return new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uDisp: { value: opts.disp || 0 },
        uFreq: { value: opts.freq || 1.1 },
        uA: { value: new THREE.Color(colors.a) },
        uB: { value: new THREE.Color(colors.b) },
        uC: { value: new THREE.Color(colors.c) },
        uAlpha: { value: opts.alpha == null ? 1 : opts.alpha }
      },
      vertexShader: NOISE + [
        "uniform float uTime; uniform float uDisp; uniform float uFreq;",
        "varying vec3 vN; varying vec3 vV; varying float vNoise;",
        "void main(){",
        "  vec3 p = position; float n = 0.0;",
        "  if (uDisp > 0.0) { n = snoise(p * uFreq + vec3(0.0, uTime * 0.35, uTime * 0.21)); p += normal * n * uDisp; }",
        "  vNoise = n;",
        "  vec4 mv = modelViewMatrix * vec4(p, 1.0);",
        "  vN = normalize(normalMatrix * normal);",
        "  vV = normalize(-mv.xyz);",
        "  gl_Position = projectionMatrix * mv;",
        "}"
      ].join("\n"),
      fragmentShader: [
        "uniform vec3 uA; uniform vec3 uB; uniform vec3 uC; uniform float uAlpha;",
        "varying vec3 vN; varying vec3 vV; varying float vNoise;",
        "void main(){",
        "  vec3 n = normalize(vN);",
        "  float fres = pow(1.0 - max(dot(n, vV), 0.0), 2.4);",
        "  float t = smoothstep(-0.95, 0.95, n.y * 0.65 + n.x * 0.35 + vNoise * 0.7);",
        "  vec3 col = mix(uA, uB, t);",
        "  vec3 L = normalize(vec3(0.55, 0.8, 0.65));",
        "  float diff = max(dot(n, L), 0.0);",
        "  col *= 0.5 + diff * 0.7;",
        "  vec3 H = normalize(L + vV);",
        "  col += pow(max(dot(n, H), 0.0), 56.0) * 0.6;",
        "  col = mix(col, uC, fres * 0.9);",
        "  gl_FragColor = vec4(col, uAlpha);",
        "  #include <colorspace_fragment>",
        "}"
      ].join("\n"),
      transparent: (opts.alpha != null && opts.alpha < 1),
      side: opts.side || THREE.FrontSide
    });
  }

  function addLights(THREE, scene, pal) {
    scene.add(new THREE.AmbientLight(0xffffff, 0.75));
    var key = new THREE.DirectionalLight(0xffffff, 1.6);
    key.position.set(3, 5, 6);
    scene.add(key);
    var tint = new THREE.PointLight(new THREE.Color(pal.c), 18, 30);
    tint.position.set(-4, -2, 4);
    scene.add(tint);
    var rim = new THREE.PointLight(new THREE.Color(pal.b), 14, 30);
    rim.position.set(4, 3, -3);
    scene.add(rim);
  }

  function makeCamera(THREE, fov, z) {
    var cam = new THREE.PerspectiveCamera(fov || 35, 1, 0.1, 200);
    cam.position.set(0, 0, z || 9);
    return cam;
  }

  /* camera distance so an object of radius r fits whatever the aspect */
  function fitZ(camera, aspect, r, margin) {
    var vFov = camera.fov * Math.PI / 180;
    var hFov = 2 * Math.atan(Math.tan(vFov / 2) * aspect);
    var fov = Math.min(vFov, hFov);
    return (r * (margin || 1.25)) / Math.sin(fov / 2);
  }

  /* ------------------------------------------------------------------ */
  /* scenes                                                              */
  /* ------------------------------------------------------------------ */
  var SCENES = {};

  /* Home hero: a noise-displaced "momentum" blob with an orbiting yellow ball */
  SCENES.momentum = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 9);
    var group = new THREE.Group();
    scene.add(group);

    var blobMat = iridMaterial(THREE, { a: pal.a, b: pal.b, c: pal.c }, { disp: 0.42, freq: 0.85 });
    var blob = new THREE.Mesh(new THREE.IcosahedronGeometry(1.75, 48), blobMat);
    group.add(blob);

    var ballMat = iridMaterial(THREE, { a: pal.c, b: "#FFF1B8", c: "#FFFFFF" });
    var ball = new THREE.Mesh(new THREE.SphereGeometry(0.2, 48, 48), ballMat);
    group.add(ball);

    var tilt = 1.15;
    var ring = new THREE.Mesh(
      new THREE.TorusGeometry(2.75, 0.008, 8, 220),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(pal.b), transparent: true, opacity: 0.55 })
    );
    ring.rotation.x = tilt;
    group.add(ring);

    var N = 1100, pos = new Float32Array(N * 3), rand = rng(7);
    for (var i = 0; i < N; i++) {
      var r = 2.6 + rand() * 2.2, th = rand() * Math.PI * 2, ph = Math.acos(2 * rand() - 1);
      pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
      pos[i * 3 + 1] = r * Math.cos(ph);
      pos[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
    }
    var g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    var halo = new THREE.Points(g, new THREE.PointsMaterial({ color: new THREE.Color(pal.b), size: 0.028, transparent: true, opacity: 0.75, depthWrite: false }));
    group.add(halo);

    var offX = o.x == null ? 1.7 : o.x;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        var wide = aspect > 1.15;
        group.position.x = wide ? offX : 0;
        group.position.y = wide ? 0.15 : 1.1;
        camera.position.z = wide ? 9 : fitZ(camera, aspect, 3.3, 1.1);
        var out = smooth(0.5, 1, p);
        blobMat.uniforms.uTime.value = t;
        blob.rotation.y = t * 0.12 + m.x * 0.45;
        blob.rotation.x = -m.y * 0.35;
        group.scale.setScalar(1 - out * 0.35);
        group.rotation.z = out * 0.6;
        var a = t * 0.55;
        ball.position.set(Math.cos(a) * 2.75, Math.sin(a) * 2.75 * Math.cos(tilt), Math.sin(a) * 2.75 * Math.sin(tilt));
        ring.rotation.z = t * 0.05;
        halo.rotation.y = t * 0.03 + m.x * 0.15;
        halo.rotation.x = m.y * 0.1;
      }
    };
  };

  /* Flowing ribbons built from shader-displaced strips */
  SCENES.ribbons = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 11);
    var group = new THREE.Group();
    scene.add(group);
    var count = o.count || 6;
    var colors = [pal.a, pal.b, pal.c, pal.b, pal.a, pal.c, pal.b];
    var mats = [];
    var geo = new THREE.PlaneGeometry(22, 1, 360, 1);
    for (var i = 0; i < count; i++) {
      var mat = new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 }, uPhase: { value: i * 1.37 }, uAmp: { value: 0.7 + (i % 3) * 0.28 },
          uWidth: { value: 0.1 + (i % 3) * 0.07 }, uCol: { value: new THREE.Color(colors[i % colors.length]) },
          uCol2: { value: new THREE.Color(colors[(i + 1) % colors.length]) }, uOpacity: { value: o.opacity || 0.85 }
        },
        vertexShader: [
          "uniform float uTime; uniform float uPhase; uniform float uAmp; uniform float uWidth;",
          "varying vec2 vUv;",
          "void main(){",
          "  vUv = uv; vec3 p = position; float x = p.x;",
          "  float taper = 0.35 + 0.65 * sin(uv.x * 3.14159);",
          "  float twist = sin(x * 0.25 + uTime * 0.4 + uPhase) * 1.2;",
          "  vec3 q = vec3(x, 0.0, 0.0);",
          "  q.y = sin(x * 0.42 + uTime * 0.55 + uPhase) * uAmp + sin(x * 0.95 - uTime * 0.35 + uPhase * 2.0) * uAmp * 0.3;",
          "  q.z = cos(x * 0.33 + uTime * 0.45 + uPhase) * 1.4;",
          "  float w = p.y * uWidth * taper;",
          "  q.y += cos(twist) * w; q.z += sin(twist) * w;",
          "  gl_Position = projectionMatrix * modelViewMatrix * vec4(q, 1.0);",
          "}"
        ].join("\n"),
        fragmentShader: [
          "uniform vec3 uCol; uniform vec3 uCol2; uniform float uOpacity; varying vec2 vUv;",
          "void main(){",
          "  float edge = smoothstep(0.0, 0.08, vUv.x) * smoothstep(1.0, 0.92, vUv.x);",
          "  vec3 col = mix(uCol, uCol2, vUv.x);",
          "  gl_FragColor = vec4(col, uOpacity * edge);",
          "  #include <colorspace_fragment>",
          "}"
        ].join("\n"),
        transparent: true, side: THREE.DoubleSide, depthWrite: false
      });
      mats.push(mat);
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.y = (i - (count - 1) / 2) * 0.42;
      mesh.position.z = -i * 0.25;
      group.add(mesh);
    }
    group.rotation.z = o.angle == null ? -0.14 : o.angle;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        camera.position.z = aspect < 1 ? 14 : 11;
        for (var k = 0; k < mats.length; k++) mats[k].uniforms.uTime.value = t;
        group.rotation.x = m.y * 0.18;
        group.rotation.y = m.x * 0.12;
        group.position.x = (0.5 - p) * 3;
        group.position.y = (o.y || 0);
      }
    };
  };

  /* Double helix of spheres; highlights the active step */
  SCENES.helix = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 12);
    addLights(THREE, scene, pal);
    var group = new THREE.Group();
    scene.add(group);
    var N = 44, height = 9.5, radius = 1.25;
    var sphereMat = new THREE.MeshStandardMaterial({ roughness: 0.28, metalness: 0.2 });
    var spheres = new THREE.InstancedMesh(new THREE.SphereGeometry(0.17, 24, 24), sphereMat, N * 2);
    var rodMat = new THREE.MeshStandardMaterial({ color: new THREE.Color(pal.b), roughness: 0.5, transparent: true, opacity: 0.55 });
    var rods = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.022, 0.022, 1, 8), rodMat, N);
    group.add(spheres);
    group.add(rods);
    var steps = o.steps || 4;
    var active = 0;
    var scales = new Float32Array(N * 2).fill(1);
    var dummy = new THREE.Object3D();
    var cA = new THREE.Color(pal.a), cB = new THREE.Color(pal.c), cHot = new THREE.Color(pal.d);
    var A = [], B = [];
    for (var i = 0; i < N; i++) {
      var y = (i / (N - 1) - 0.5) * height;
      var ang = i * 0.43;
      A.push(new THREE.Vector3(Math.cos(ang) * radius, y, Math.sin(ang) * radius));
      B.push(new THREE.Vector3(-Math.cos(ang) * radius, y, -Math.sin(ang) * radius));
      var mid = A[i].clone().add(B[i]).multiplyScalar(0.5);
      var dir = B[i].clone().sub(A[i]);
      dummy.position.copy(mid);
      dummy.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
      dummy.scale.set(1, dir.length(), 1);
      dummy.updateMatrix();
      rods.setMatrixAt(i, dummy.matrix);
    }
    function paint() {
      for (var i = 0; i < N; i++) {
        var seg = Math.floor((1 - i / N) * steps);
        var hot = seg === active;
        spheres.setColorAt(i, hot ? cHot : cA);
        spheres.setColorAt(N + i, hot ? cB : cA.clone().lerp(cB, 0.35));
      }
      spheres.instanceColor.needsUpdate = true;
    }
    for (var j = 0; j < N * 2; j++) spheres.setColorAt(j, cA);
    paint();
    return {
      scene: scene, camera: camera,
      setIndex: function (i) { active = i; paint(); },
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        camera.position.z = aspect < 0.8 ? 16 : 12;
        group.rotation.y = t * 0.22 + p * Math.PI * 1.5 + m.x * 0.3;
        group.rotation.z = 0.32 + m.y * 0.08;
        for (var i = 0; i < N; i++) {
          var seg = Math.floor((1 - i / N) * steps);
          var target = seg === active ? 1.55 : 0.85;
          scales[i] = lerp(scales[i], target, 0.08);
          scales[N + i] = lerp(scales[N + i], target, 0.08);
          dummy.quaternion.identity();
          dummy.position.copy(A[i]); dummy.scale.setScalar(scales[i]); dummy.updateMatrix(); spheres.setMatrixAt(i, dummy.matrix);
          dummy.position.copy(B[i]); dummy.scale.setScalar(scales[N + i]); dummy.updateMatrix(); spheres.setMatrixAt(N + i, dummy.matrix);
        }
        spheres.instanceMatrix.needsUpdate = true;
      }
    };
  };

  /* One object per service; morphs to the active service */
  SCENES.pillars = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 8);
    addLights(THREE, scene, pal);
    var root3 = new THREE.Group();
    scene.add(root3);
    var mat = function (disp) { return iridMaterial(THREE, { a: pal.a, b: pal.b, c: pal.c }, { disp: disp || 0 }); };
    var mats = [];
    var objs = [];

    // 0 branding: faceted dodecahedron inside a wire shell
    var g0 = new THREE.Group();
    var m0 = mat(); mats.push(m0);
    g0.add(new THREE.Mesh(new THREE.DodecahedronGeometry(1.35, 0), m0));
    g0.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(1.9, 1)), new THREE.LineBasicMaterial({ color: new THREE.Color(pal.b), transparent: true, opacity: 0.5 })));
    objs.push(g0);

    // 1 websites: a screen with floating blocks
    var g1 = new THREE.Group();
    var m1 = mat(); mats.push(m1);
    g1.add(new THREE.Mesh(new THREE.BoxGeometry(2.9, 1.9, 0.12), m1));
    var gridLines = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(2.6, 1.6, 6, 4)), new THREE.LineBasicMaterial({ color: new THREE.Color(pal.d), transparent: true, opacity: 0.25 }));
    gridLines.position.z = 0.07;
    g1.add(gridLines);
    var blockMat = mat(); mats.push(blockMat);
    [[-0.8, 0.35, 0.9, 0.5], [0.55, 0.35, 1.1, 0.5], [-0.25, -0.45, 2.0, 0.35]].forEach(function (b, k) {
      var blk = new THREE.Mesh(new THREE.BoxGeometry(b[2], b[3], 0.1), blockMat);
      blk.position.set(b[0], b[1], 0.35 + k * 0.18);
      blk.userData.baseZ = blk.position.z;
      g1.add(blk);
    });
    objs.push(g1);

    // 2 SEO: magnifying glass
    var g2 = new THREE.Group();
    var m2 = mat(); mats.push(m2);
    var lensRing = new THREE.Mesh(new THREE.TorusGeometry(0.95, 0.16, 32, 96), m2);
    g2.add(lensRing);
    var handle = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, 1.4, 32), m2);
    handle.position.set(1.05, -1.05, 0);
    handle.rotation.z = Math.PI / 4;
    g2.add(handle);
    var glass = new THREE.Mesh(new THREE.CircleGeometry(0.82, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color(pal.c), transparent: true, opacity: 0.18 }));
    g2.add(glass);
    g2.position.set(-0.2, 0.25, 0);
    objs.push(g2);

    // 3 social: cluster of bubbles
    var g3 = new THREE.Group();
    var m3 = mat(0.05); mats.push(m3);
    var bubbleRand = rng(33);
    for (var i = 0; i < 9; i++) {
      var r = 0.25 + bubbleRand() * 0.5;
      var bub = new THREE.Mesh(new THREE.SphereGeometry(r, 40, 40), m3);
      bub.position.set((bubbleRand() - 0.5) * 2.8, (bubbleRand() - 0.5) * 2.2, (bubbleRand() - 0.5) * 1.5);
      bub.userData.seed = bubbleRand() * 6.28;
      bub.userData.baseY = bub.position.y;
      g3.add(bub);
    }
    objs.push(g3);

    // 4 performance: rising bars + arrow
    var g4 = new THREE.Group();
    var m4 = mat(); mats.push(m4);
    var bars = [];
    for (var b = 0; b < 5; b++) {
      var h = 0.6 + b * 0.45;
      var bar = new THREE.Mesh(new THREE.BoxGeometry(0.42, 1, 0.42), m4);
      bar.geometry.translate(0, 0.5, 0);
      bar.position.set(-1.25 + b * 0.62, -1.3, 0);
      bar.scale.y = h;
      bar.userData.h = h;
      bars.push(bar);
      g4.add(bar);
    }
    var arrow = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.6, 32), iridMaterial(THREE, { a: pal.c, b: "#FFF1B8", c: "#FFFFFF" }));
    arrow.position.set(1.35, 1.75, 0);
    arrow.rotation.z = -0.5;
    g4.add(arrow);
    objs.push(g4);

    var only = o.only;
    var active = only == null ? (o.index || 0) : only;
    var scales = objs.map(function (_, k) { return k === active ? 1 : 0.001; });
    objs.forEach(function (obj, k) { obj.scale.setScalar(scales[k]); root3.add(obj); });
    var autoCycle = !!o.cycle && only == null;
    var lastSwitch = 0;

    return {
      scene: scene, camera: camera,
      setIndex: function (i) { if (only == null) active = clamp(i, 0, objs.length - 1); },
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        camera.position.z = fitZ(camera, aspect, 2.2, 1.15);
        if (autoCycle && t - lastSwitch > 2.6) { active = (active + 1) % objs.length; lastSwitch = t; }
        for (var k = 0; k < objs.length; k++) {
          scales[k] = lerp(scales[k], k === active ? 1 : 0.001, 0.09);
          objs[k].scale.setScalar(Math.max(scales[k], 0.001));
          objs[k].visible = scales[k] > 0.01;
        }
        for (var q = 0; q < mats.length; q++) mats[q].uniforms.uTime.value = t;
        root3.rotation.y = Math.sin(t * 0.4) * 0.5 + m.x * 0.5;
        root3.rotation.x = Math.sin(t * 0.3) * 0.15 - m.y * 0.3;
        g0.rotation.y = t * 0.3;
        g0.children[1].rotation.x = t * 0.15;
        g1.children.forEach(function (c) { if (c.userData.baseZ != null) c.position.z = c.userData.baseZ + Math.sin(t * 1.4 + c.userData.baseZ * 6) * 0.12; });
        g3.children.forEach(function (c) { c.position.y = c.userData.baseY + Math.sin(t * 1.1 + c.userData.seed) * 0.15; });
        bars.forEach(function (bar, k) { bar.scale.y = bar.userData.h * (0.85 + 0.15 * Math.sin(t * 1.6 + k)); });
        arrow.position.y = 1.75 + Math.sin(t * 1.6) * 0.1;
      }
    };
  };

  /* A number or word rendered as thousands of particles that assemble in view */
  SCENES.pointsText = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 10);
    var text = String(o.text || "MMAG");
    var W = 1400, H = 520;
    var c = document.createElement("canvas");
    c.width = W; c.height = H;
    var g = c.getContext("2d");
    var size = 420;
    g.font = "800 " + size + "px 'Plus Jakarta Sans', 'Segoe UI', sans-serif";
    while (g.measureText(text).width > W * 0.94 && size > 60) {
      size -= 10;
      g.font = "800 " + size + "px 'Plus Jakarta Sans', 'Segoe UI', sans-serif";
    }
    g.fillStyle = "#fff";
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.fillText(text, W / 2, H / 2 + size * 0.04);
    var data = g.getImageData(0, 0, W, H).data;
    var step = o.step || 5;
    var targets = [];
    var worldW = o.width || 9;
    for (var y = 0; y < H; y += step) {
      for (var x = 0; x < W; x += step) {
        if (data[(y * W + x) * 4 + 3] > 140) targets.push((x - W / 2) / W * worldW, -(y - H / 2) / W * worldW);
      }
    }
    var n = targets.length / 2;
    var aTarget = new Float32Array(n * 3), aStart = new Float32Array(n * 3), aRand = new Float32Array(n);
    var rand = rng(text.length * 991 + 17);
    for (var i = 0; i < n; i++) {
      aTarget[i * 3] = targets[i * 2];
      aTarget[i * 3 + 1] = targets[i * 2 + 1];
      aTarget[i * 3 + 2] = (rand() - 0.5) * 0.25;
      var r = 4 + rand() * 6, th = rand() * Math.PI * 2, ph = Math.acos(2 * rand() - 1);
      aStart[i * 3] = r * Math.sin(ph) * Math.cos(th);
      aStart[i * 3 + 1] = r * Math.cos(ph) * 0.7;
      aStart[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th) - 2;
      aRand[i] = rand();
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(aTarget, 3));
    geo.setAttribute("aStart", new THREE.BufferAttribute(aStart, 3));
    geo.setAttribute("aRand", new THREE.BufferAttribute(aRand, 1));
    var mat = new THREE.ShaderMaterial({
      uniforms: {
        uMix: { value: 0 }, uTime: { value: 0 }, uSize: { value: 2.6 * Math.min(window.devicePixelRatio || 1, 2) },
        uMouse: { value: new THREE.Vector2(99, 99) }, uA: { value: new THREE.Color(pal.c) }, uB: { value: new THREE.Color(pal.b) },
        uW: { value: worldW }
      },
      vertexShader: [
        "attribute vec3 aStart; attribute float aRand;",
        "uniform float uMix; uniform float uTime; uniform float uSize; uniform vec2 uMouse; uniform vec3 uA; uniform vec3 uB; uniform float uW;",
        "varying vec3 vCol; varying float vAlpha;",
        "void main(){",
        "  float m = clamp(uMix * 1.7 - aRand * 0.7, 0.0, 1.0);",
        "  m = m * m * (3.0 - 2.0 * m);",
        "  vec3 p = mix(aStart, position, m);",
        "  p.z += sin(uTime * 1.3 + aRand * 6.2831) * 0.06;",
        "  vec2 d = p.xy - uMouse; float dist = length(d);",
        "  p.xy += normalize(d + 0.0001) * smoothstep(1.1, 0.0, dist) * 0.55 * m;",
        "  vec4 mv = modelViewMatrix * vec4(p, 1.0);",
        "  gl_PointSize = uSize * (0.65 + aRand * 0.7) * (10.0 / -mv.z);",
        "  gl_Position = projectionMatrix * mv;",
        "  vCol = mix(uA, uB, clamp(position.x / uW + 0.5, 0.0, 1.0));",
        "  vAlpha = 0.35 + 0.65 * m;",
        "}"
      ].join("\n"),
      fragmentShader: [
        "varying vec3 vCol; varying float vAlpha;",
        "void main(){",
        "  vec2 c = gl_PointCoord - 0.5; if (dot(c, c) > 0.25) discard;",
        "  gl_FragColor = vec4(vCol, vAlpha);",
        "  #include <colorspace_fragment>",
        "}"
      ].join("\n"),
      transparent: true, depthWrite: false
    });
    var points = new THREE.Points(geo, mat);
    scene.add(points);
    var mixNow = 0;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect, vis) {
        var aspect = rect.width / rect.height;
        camera.position.z = fitZ(camera, aspect, worldW * 0.52, 1.02);
        var target = o.always ? 1 : smooth(0.25, 0.8, vis);
        mixNow = lerp(mixNow, target, 0.045);
        mat.uniforms.uMix.value = mixNow;
        mat.uniforms.uTime.value = t;
        var vFov = camera.fov * Math.PI / 180;
        var halfH = Math.tan(vFov / 2) * camera.position.z;
        mat.uniforms.uMouse.value.set(m.x * halfH * aspect, m.y * halfH);
        points.rotation.y = m.x * 0.18;
        points.rotation.x = -m.y * 0.12;
      }
    };
  };

  /* Dotted globe with arcs from Pune to the USA */
  SCENES.globe = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 9);
    var group = new THREE.Group();
    scene.add(group);
    var R = 2;
    var n = 2600;
    var pts = fibonacciSphere(n, R);
    var geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(pts, 3));
    var dotMat = new THREE.ShaderMaterial({
      uniforms: { uCol: { value: new THREE.Color(pal.b) }, uSize: { value: 2.2 * Math.min(window.devicePixelRatio || 1, 2) } },
      vertexShader: [
        "uniform float uSize; varying float vA;",
        "void main(){",
        "  vec4 mv = modelViewMatrix * vec4(position, 1.0);",
        "  vec3 nrm = normalize(normalMatrix * position);",
        "  vA = smoothstep(-0.5, 0.7, nrm.z) * 0.85 + 0.08;",
        "  gl_PointSize = uSize * (9.0 / -mv.z);",
        "  gl_Position = projectionMatrix * mv;",
        "}"
      ].join("\n"),
      fragmentShader: [
        "uniform vec3 uCol; varying float vA;",
        "void main(){ vec2 c = gl_PointCoord - 0.5; if (dot(c,c) > 0.25) discard; gl_FragColor = vec4(uCol, vA);",
        "  #include <colorspace_fragment>",
        "}"
      ].join("\n"),
      transparent: true, depthWrite: false
    });
    group.add(new THREE.Points(geo, dotMat));

    function ll(lat, lon, r) {
      var phi = (90 - lat) * Math.PI / 180, th = (lon + 180) * Math.PI / 180;
      return new THREE.Vector3(-r * Math.sin(phi) * Math.cos(th), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(th));
    }
    var pune = ll(18.52, 73.86, R);
    var targets = [ll(40.71, -74.0, R), ll(37.77, -122.42, R), ll(41.88, -87.63, R)];
    var arcMats = [];
    targets.forEach(function (end, k) {
      var mid = pune.clone().add(end).multiplyScalar(0.5);
      mid.setLength(R * 1.75);
      var curve = new THREE.QuadraticBezierCurve3(pune, mid, end);
      var cp = curve.getPoints(120);
      var g2 = new THREE.BufferGeometry().setFromPoints(cp);
      var tt = new Float32Array(cp.length);
      for (var i = 0; i < cp.length; i++) tt[i] = i / (cp.length - 1);
      g2.setAttribute("aT", new THREE.BufferAttribute(tt, 1));
      var am = new THREE.ShaderMaterial({
        uniforms: { uHead: { value: 0 }, uCol: { value: new THREE.Color(pal.c) } },
        vertexShader: "attribute float aT; varying float vT; void main(){ vT = aT; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
        fragmentShader: [
          "uniform float uHead; uniform vec3 uCol; varying float vT;",
          "void main(){ float a = smoothstep(uHead - 0.45, uHead, vT) * step(vT, uHead); if (a < 0.01) discard; gl_FragColor = vec4(uCol, a);",
          "  #include <colorspace_fragment>",
          "}"
        ].join("\n"),
        transparent: true, depthWrite: false
      });
      am.userData.offset = k * 0.33;
      arcMats.push(am);
      group.add(new THREE.Line(g2, am));
    });
    var marker = new THREE.Mesh(new THREE.SphereGeometry(0.07, 24, 24), new THREE.MeshBasicMaterial({ color: new THREE.Color(pal.c) }));
    marker.position.copy(pune);
    group.add(marker);
    var pulse = new THREE.Mesh(new THREE.RingGeometry(0.08, 0.11, 48), new THREE.MeshBasicMaterial({ color: new THREE.Color(pal.c), transparent: true, side: THREE.DoubleSide }));
    pulse.position.copy(pune.clone().multiplyScalar(1.01));
    pulse.lookAt(pune.clone().multiplyScalar(2));
    group.add(pulse);
    targets.forEach(function (end) {
      var mk = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 16), new THREE.MeshBasicMaterial({ color: new THREE.Color(pal.d) }));
      mk.position.copy(end);
      group.add(mk);
    });
    var baseY = -Math.atan2(pune.x, pune.z);
    group.rotation.x = 0.35;
    var offX = o.x || 0;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        camera.position.z = fitZ(camera, aspect, R, 1.25);
        group.position.x = aspect > 1.3 ? offX : 0;
        group.rotation.y = baseY + t * 0.1 + p * 1.2 + m.x * 0.3;
        group.rotation.x = 0.35 - m.y * 0.15;
        arcMats.forEach(function (am) { am.uniforms.uHead.value = ((t * 0.22 + am.userData.offset) % 1) * 1.45; });
        var s = 1 + (t * 0.9 % 1) * 2.4;
        pulse.scale.setScalar(s);
        pulse.material.opacity = 1 - (t * 0.9 % 1);
      }
    };
  };

  /* Point-cloud terrain that ripples under the cursor */
  SCENES.wave = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 40, 12);
    camera.position.set(0, 2.6, 11);
    camera.lookAt(0, 0, 0);
    var plane = new THREE.PlaneGeometry(30, 18, o.dense ? 200 : 150, o.dense ? 120 : 90);
    var mat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 }, uMouse: { value: new THREE.Vector2(0, 0) }, uA: { value: new THREE.Color(pal.a) },
        uB: { value: new THREE.Color(pal.c) }, uSize: { value: 2.0 * Math.min(window.devicePixelRatio || 1, 2) }, uAmp: { value: o.amp || 1 }
      },
      vertexShader: NOISE + [
        "uniform float uTime; uniform vec2 uMouse; uniform float uSize; uniform float uAmp; varying float vH;",
        "void main(){",
        "  vec3 p = position;",
        "  float h = snoise(vec3(p.x * 0.14, p.y * 0.14, uTime * 0.12)) * 1.1 + sin(p.x * 0.35 + uTime * 0.7) * 0.25;",
        "  float d = distance(p.xy, uMouse);",
        "  h += sin(d * 2.6 - uTime * 3.5) * exp(-d * 0.45) * 0.55;",
        "  p.z = h * uAmp;",
        "  vH = h;",
        "  vec4 mv = modelViewMatrix * vec4(p, 1.0);",
        "  gl_PointSize = uSize * (12.0 / -mv.z);",
        "  gl_Position = projectionMatrix * mv;",
        "}"
      ].join("\n"),
      fragmentShader: [
        "uniform vec3 uA; uniform vec3 uB; varying float vH;",
        "void main(){ vec2 c = gl_PointCoord - 0.5; if (dot(c,c) > 0.25) discard;",
        "  vec3 col = mix(uA, uB, smoothstep(-0.6, 1.2, vH));",
        "  gl_FragColor = vec4(col, 0.55 + smoothstep(-0.5, 1.0, vH) * 0.45);",
        "  #include <colorspace_fragment>",
        "}"
      ].join("\n"),
      transparent: true, depthWrite: false
    });
    var points = new THREE.Points(plane, mat);
    points.rotation.x = -Math.PI / 2.35;
    points.position.y = o.y == null ? -1.2 : o.y;
    scene.add(points);
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        mat.uniforms.uTime.value = t;
        mat.uniforms.uMouse.value.set(m.x * 12, -m.y * 7 + 2);
        points.rotation.z = m.x * 0.05;
      }
    };
  };

  /* Hundreds of tetrahedra that assemble into a sphere in view */
  SCENES.shards = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 9);
    addLights(THREE, scene, pal);
    var N = o.count || 340;
    var mesh = new THREE.InstancedMesh(new THREE.TetrahedronGeometry(0.2, 0), new THREE.MeshStandardMaterial({ roughness: 0.3, metalness: 0.25, flatShading: true }), N);
    scene.add(mesh);
    var R = o.radius || 2.3;
    var target = fibonacciSphere(N, R);
    var rand = rng(N * 7 + 3);
    var scatter = new Float32Array(N * 3), spin = new Float32Array(N * 3);
    var cols = [new THREE.Color(pal.a), new THREE.Color(pal.b), new THREE.Color(pal.c), new THREE.Color(pal.d)];
    for (var i = 0; i < N; i++) {
      var k = 2.2 + rand() * 2.8;
      scatter[i * 3] = target[i * 3] * k + (rand() - 0.5) * 3;
      scatter[i * 3 + 1] = target[i * 3 + 1] * k + (rand() - 0.5) * 3;
      scatter[i * 3 + 2] = target[i * 3 + 2] * k + (rand() - 0.5) * 3;
      spin[i * 3] = rand() * 2; spin[i * 3 + 1] = rand() * 2; spin[i * 3 + 2] = rand() * 6.28;
      var pick = rand();
      mesh.setColorAt(i, cols[pick < 0.45 ? 0 : pick < 0.75 ? 1 : pick < 0.93 ? 2 : 3]);
    }
    mesh.instanceColor.needsUpdate = true;
    var dummy = new THREE.Object3D();
    var asm = 0;
    var offX = o.x || 0;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect, vis) {
        var aspect = rect.width / rect.height;
        camera.position.z = fitZ(camera, aspect, R, 1.35);
        var wide = aspect > 1.3;
        var goal = o.hero ? (1 - smooth(0.5, 0.95, p)) : smooth(0.2, 0.75, vis);
        asm = lerp(asm, goal, 0.05);
        for (var i = 0; i < N; i++) {
          var e = clamp(asm * 1.4 - (i % 17) / 17 * 0.4, 0, 1);
          e = e * e * (3 - 2 * e);
          dummy.position.set(
            lerp(scatter[i * 3], target[i * 3], e) + (wide ? offX : 0),
            lerp(scatter[i * 3 + 1], target[i * 3 + 1], e),
            lerp(scatter[i * 3 + 2], target[i * 3 + 2], e)
          );
          dummy.rotation.set(t * spin[i * 3] + spin[i * 3 + 2], t * spin[i * 3 + 1], 0);
          dummy.scale.setScalar(0.6 + e * 0.6);
          dummy.updateMatrix();
          mesh.setMatrixAt(i, dummy.matrix);
        }
        mesh.instanceMatrix.needsUpdate = true;
        mesh.rotation.y = t * 0.12 + m.x * 0.4;
        mesh.rotation.x = -m.y * 0.25;
      }
    };
  };

  /* A field of bars rising like a growth chart */
  SCENES.stack = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 32, 14);
    camera.position.set(8, 7.5, 10);
    camera.lookAt(0, 0.8, 0);
    addLights(THREE, scene, pal);
    var G = o.grid || 12, gap = 0.48;
    var geo = new THREE.BoxGeometry(0.36, 1, 0.36);
    geo.translate(0, 0.5, 0);
    var mesh = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.15 }), G * G);
    var group = new THREE.Group();
    group.add(mesh);
    scene.add(group);
    var dummy = new THREE.Object3D();
    var cLow = new THREE.Color(pal.a), cHigh = new THREE.Color(pal.c), tmp = new THREE.Color();
    for (var j = 0; j < G * G; j++) mesh.setColorAt(j, cLow);
    var grow = 0;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect, vis) {
        grow = lerp(grow, smooth(0.15, 0.7, vis), 0.05);
        var i = 0;
        for (var x = 0; x < G; x++) {
          for (var z = 0; z < G; z++) {
            var px = (x - (G - 1) / 2) * gap, pz = (z - (G - 1) / 2) * gap;
            var wave = 0.5 + 0.5 * Math.sin(x * 0.55 + t * 0.9) * Math.cos(z * 0.45 + t * 0.7);
            var diag = (x + z) / (2 * G);
            var h = 0.08 + (wave * 1.6 + diag * 1.8) * grow;
            dummy.position.set(px, 0, pz);
            dummy.scale.set(1, h, 1);
            dummy.updateMatrix();
            mesh.setMatrixAt(i, dummy.matrix);
            tmp.copy(cLow).lerp(cHigh, clamp(h / 3.2, 0, 1));
            mesh.setColorAt(i, tmp);
            i++;
          }
        }
        mesh.instanceMatrix.needsUpdate = true;
        mesh.instanceColor.needsUpdate = true;
        group.rotation.y = t * 0.08 + m.x * 0.35;
      }
    };
  };

  /* Glossy torus knot inside a ring of particles */
  SCENES.knot = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 9);
    var group = new THREE.Group();
    scene.add(group);
    var mat = iridMaterial(THREE, { a: pal.a, b: pal.b, c: pal.c }, { disp: 0.05, freq: 1.6 });
    var knot = new THREE.Mesh(new THREE.TorusKnotGeometry(1.15, 0.36, 260, 40, 2, 3), mat);
    group.add(knot);
    var N = 900, pos = new Float32Array(N * 3), rand = rng(91);
    for (var i = 0; i < N; i++) {
      var a = rand() * Math.PI * 2, r = 2.5 + (rand() - 0.5) * 0.6;
      pos[i * 3] = Math.cos(a) * r; pos[i * 3 + 1] = (rand() - 0.5) * 0.35; pos[i * 3 + 2] = Math.sin(a) * r;
    }
    var g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    var belt = new THREE.Points(g, new THREE.PointsMaterial({ color: new THREE.Color(pal.d), size: 0.03, transparent: true, opacity: 0.7, depthWrite: false }));
    belt.rotation.x = 0.4;
    group.add(belt);
    var offX = o.x || 0;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        camera.position.z = fitZ(camera, aspect, 2.4, 1.15);
        group.position.x = aspect > 1.3 ? offX : 0;
        mat.uniforms.uTime.value = t;
        knot.rotation.x = t * 0.25 - m.y * 0.4;
        knot.rotation.y = t * 0.32 + m.x * 0.5;
        belt.rotation.y = -t * 0.15;
        group.scale.setScalar(0.85 + smooth(0, 0.6, p) * 0.15);
      }
    };
  };

  /* Gyroscope rings around a yellow core */
  SCENES.rings = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 35, 9);
    var group = new THREE.Group();
    scene.add(group);
    var rings = [];
    var mats = [];
    [1.35, 1.75, 2.15, 2.55].forEach(function (r, k) {
      var mt = iridMaterial(THREE, { a: k % 2 ? pal.a : pal.b, b: k % 2 ? pal.b : pal.a, c: pal.c });
      mats.push(mt);
      var ring = new THREE.Mesh(new THREE.TorusGeometry(r, 0.045 + k * 0.012, 24, 200), mt);
      ring.userData.axis = new THREE.Vector3(Math.sin(k * 1.7), Math.cos(k * 1.3), Math.sin(k * 0.9)).normalize();
      ring.userData.speed = 0.25 + k * 0.12;
      rings.push(ring);
      group.add(ring);
    });
    var coreMat = iridMaterial(THREE, { a: pal.c, b: "#FFF1B8", c: "#FFFFFF" }, { disp: 0.12, freq: 2 });
    mats.push(coreMat);
    var core = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 24), coreMat);
    group.add(core);
    var offX = o.x || 0;
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        var aspect = rect.width / rect.height;
        camera.position.z = fitZ(camera, aspect, 2.7, 1.15);
        group.position.x = aspect > 1.3 ? offX : 0;
        for (var k = 0; k < mats.length; k++) mats[k].uniforms.uTime.value = t;
        rings.forEach(function (ring) {
          ring.rotation.x = Math.sin(t * ring.userData.speed) * 1.4 * ring.userData.axis.x + t * 0.2 * ring.userData.axis.y;
          ring.rotation.y = t * ring.userData.speed * ring.userData.axis.z + 0.6;
        });
        group.rotation.y = m.x * 0.5;
        group.rotation.x = -m.y * 0.35;
        core.scale.setScalar(1 + Math.sin(t * 2) * 0.05);
      }
    };
  };

  /* Brand-coloured confetti, falling forever */
  SCENES.confetti = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 40, 10);
    var N = o.count || 260;
    var mesh = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.2, 0.11), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }), N);
    scene.add(mesh);
    var rand = rng(5);
    var data = [];
    var cols = [new THREE.Color(pal.a), new THREE.Color(pal.b), new THREE.Color(pal.c), new THREE.Color(pal.d)];
    for (var i = 0; i < N; i++) {
      data.push({ x: (rand() - 0.5) * 16, z: (rand() - 0.5) * 6, off: rand() * 10, sp: 0.5 + rand() * 0.8, rx: rand() * 3, ry: rand() * 3, sw: rand() * 6.28 });
      mesh.setColorAt(i, cols[Math.floor(rand() * cols.length)]);
    }
    mesh.instanceColor.needsUpdate = true;
    var dummy = new THREE.Object3D();
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m, rect) {
        for (var i = 0; i < N; i++) {
          var d = data[i];
          var y = 6 - ((t * d.sp + d.off) % 12);
          dummy.position.set(d.x + Math.sin(t * 0.8 + d.sw) * 0.4 + m.x * 0.6, y, d.z);
          dummy.rotation.set(t * d.rx, t * d.ry, d.sw);
          dummy.updateMatrix();
          mesh.setMatrixAt(i, dummy.matrix);
        }
        mesh.instanceMatrix.needsUpdate = true;
      }
    };
  };

  /* Particle tunnel (404) */
  SCENES.tunnel = function (THREE, pal, o) {
    var scene = new THREE.Scene();
    var camera = makeCamera(THREE, 70, 4);
    var RINGS = 48, PER = 96, DEPTH = 48;
    var pos = new Float32Array(RINGS * PER * 3), z0 = new Float32Array(RINGS * PER);
    var rand = rng(404);
    for (var r = 0; r < RINGS; r++) {
      for (var k = 0; k < PER; k++) {
        var i = r * PER + k, a = k / PER * Math.PI * 2, rad = 2.4 + (rand() - 0.5) * 0.5;
        pos[i * 3] = Math.cos(a) * rad; pos[i * 3 + 1] = Math.sin(a) * rad; pos[i * 3 + 2] = 0;
        z0[i] = -r / RINGS * DEPTH;
      }
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    geo.setAttribute("aZ", new THREE.BufferAttribute(z0, 1));
    var mat = new THREE.ShaderMaterial({
      uniforms: { uTime: { value: 0 }, uA: { value: new THREE.Color(pal.b) }, uB: { value: new THREE.Color(pal.c) }, uSize: { value: 2.4 * Math.min(window.devicePixelRatio || 1, 2) }, uDepth: { value: DEPTH } },
      vertexShader: [
        "attribute float aZ; uniform float uTime; uniform float uSize; uniform float uDepth; varying float vF;",
        "void main(){",
        "  float z = mod(aZ + uTime * 6.0, uDepth) - uDepth + 3.0;",
        "  vec3 p = vec3(position.xy * (1.0 + sin(z * 0.15 + uTime) * 0.08), z);",
        "  vF = smoothstep(-uDepth + 3.0, 1.0, z);",
        "  vec4 mv = modelViewMatrix * vec4(p, 1.0);",
        "  gl_PointSize = uSize * (6.0 / -mv.z);",
        "  gl_Position = projectionMatrix * mv;",
        "}"
      ].join("\n"),
      fragmentShader: [
        "uniform vec3 uA; uniform vec3 uB; varying float vF;",
        "void main(){ vec2 c = gl_PointCoord - 0.5; if (dot(c,c) > 0.25) discard; gl_FragColor = vec4(mix(uA, uB, vF), vF);",
        "  #include <colorspace_fragment>",
        "}"
      ].join("\n"),
      transparent: true, depthWrite: false
    });
    scene.add(new THREE.Points(geo, mat));
    return {
      scene: scene, camera: camera,
      update: function (t, dt, p, m) {
        mat.uniforms.uTime.value = t;
        camera.position.x = m.x * 0.8;
        camera.position.y = m.y * 0.6;
        camera.lookAt(0, 0, -20);
      }
    };
  };

  /* ------------------------------------------------------------------ */
  /* engine                                                              */
  /* ------------------------------------------------------------------ */
  function start(THREE) {
    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
    } catch (e) {
      root.classList.add("no-webgl");
      return;
    }
    renderer.setClearColor(0x000000, 0);
    renderer.autoClear = false;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    var maxDpr = window.innerWidth < 900 ? 1.5 : 1.75;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, maxDpr));

    function resize() {
      renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
    }
    resize();
    window.addEventListener("resize", resize);

    var items = [];
    elements.forEach(function (el) {
      var factory = SCENES[el.getAttribute("data-scene")];
      if (!factory) return;
      var opts = {};
      try { opts = JSON.parse(el.getAttribute("data-opts") || "{}"); } catch (e) { opts = {}; }
      var pal = PALETTES[themeOf(el)] || PALETTES.dark;
      try {
        var s = factory(THREE, pal, opts, el);
        s.el = el;
        s.mouse = new THREE.Vector2();
        s.smouse = new THREE.Vector2();
        el.addEventListener("scene:index", function (ev) { if (s.setIndex) s.setIndex(ev.detail); });
        items.push(s);
      } catch (e) {
        console.warn("[MMAG] scene failed:", el.getAttribute("data-scene"), e);
      }
    });

    var px = -9999, py = -9999;
    window.addEventListener("pointermove", function (e) { px = e.clientX; py = e.clientY; }, { passive: true });

    var last = performance.now();
    var running = true;
    var time = 0;
    document.addEventListener("visibilitychange", function () {
      running = !document.hidden;
      last = performance.now();
    });

    function frame() {
      requestAnimationFrame(frame);
      if (!running) return;
      var now = performance.now();
      var dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      time += dt * (reduced ? 0.12 : 1);
      var W = canvas.clientWidth, H = canvas.clientHeight;
      var pr = renderer.getPixelRatio();
      if (canvas.width !== Math.floor(W * pr) || canvas.height !== Math.floor(H * pr)) resize();

      renderer.setScissorTest(false);
      renderer.clear(true, true, true);
      renderer.setScissorTest(true);

      for (var i = 0; i < items.length; i++) {
        var s = items[i];
        var r = s.el.getBoundingClientRect();
        if (r.bottom <= 0 || r.top >= H || r.right <= 0 || r.left >= W || r.width < 2 || r.height < 2) continue;
        var progress = clamp((H - r.top) / (H + r.height), 0, 1);
        var visW = Math.max(0, Math.min(r.right, W) - Math.max(r.left, 0));
        var visH = Math.max(0, Math.min(r.bottom, H) - Math.max(r.top, 0));
        var vis = (visW * visH) / Math.max(1, Math.min(r.width * r.height, W * H));
        var mx = ((px - r.left) / r.width) * 2 - 1;
        var my = -(((py - r.top) / r.height) * 2 - 1);
        if (px < -9000) { mx = 0; my = 0; }
        s.mouse.set(clamp(mx, -1.5, 1.5), clamp(my, -1.5, 1.5));
        s.smouse.lerp(s.mouse, 1 - Math.pow(0.002, dt));
        s.camera.aspect = r.width / r.height;
        s.camera.updateProjectionMatrix();
        s.update(time, dt, progress, s.smouse, r, clamp(vis, 0, 1));
        var left = r.left, bottom = H - r.bottom;
        renderer.setViewport(left, bottom, r.width, r.height);
        var sx = Math.max(0, left), sy = Math.max(0, bottom);
        var sw = Math.min(W, r.right) - sx, sh = Math.min(H, H - r.top) - sy;
        if (sw <= 0 || sh <= 0) continue;
        renderer.setScissor(sx, sy, sw, sh);
        renderer.clearDepth();
        renderer.render(s.scene, s.camera);
      }
    }
    requestAnimationFrame(frame);
    root.classList.add("webgl-ready");
  }
})();
